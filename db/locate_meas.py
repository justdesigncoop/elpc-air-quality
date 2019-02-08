import sqlalchemy as sa
import pandas as pd
import logging
import sys
import shapely.wkt
import geopandas as gpd

#from memory_profiler import profile

DEFAULT_LOC = 0
CHUNKSIZE = 10000

# update measurements to loc
def update_loc(column, loc, ind, engine):
    conn = engine.connect()
    query = 'UPDATE measurements SET %s = %d WHERE id = %d AND stream_id = %d' % (column, loc, ind[0], ind[1])
    try:
        conn.execute(query)
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    conn.close()

if __name__ == '__main__':
    # generate error log
    logging.basicConfig(
        filename='logs/locate_meas_%s.log' % (pd.Timestamp.now().strftime('%Y%m%d%H%M%S')),
        filemode='w',
        format = '%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)

    logging.info('locate meas started')

    # create engine
    try:
        engine = sa.create_engine('mysql+mysqlconnector://elpcjd:Elpc1234@127.0.0.1/elpc_air_quality')
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)

    # array of database tables
    tables = [
        {'table': 'tracts', 'index': 'id', 'column': 'tract_id'},
        {'table': 'neighborhoods', 'index': 'id', 'column': 'neighborhood_id'},
        {'table': 'wards', 'index': 'id', 'column': 'ward_id'},
        {'table': 'hexagons', 'index': 'id', 'column': 'hexagon_id'},
        {'table': 'zipcodes', 'index': 'id', 'column': 'zipcode_id'},
    ]

    # iterate through array of tables
    for t in tables:
        # get geo boundaries
        try:
            geo = pd.read_sql_query('SELECT * FROM %s' % (t['table']), engine, index_col=t['index'])
        except sa.exc.SQLAlchemyError as e:
            logging.error(e)
            sys.exit(1)
        
        # create shape objects
        geo['g'] = geo['geo'].apply(shapely.wkt.loads)
        
        # create geodataframe
        geo = gpd.GeoDataFrame(geo, geometry='g')
        
        # create rtree index
        sindex = geo['g'].sindex
        
        num = 0
        while True:
            # get remaining measurements (chunksize limit)
            try:
                measurements = pd.read_sql_query('SELECT * FROM measurements WHERE %s IS NULL ORDER BY stream_id, id LIMIT %d' % (t['column'], CHUNKSIZE), engine, index_col=['id', 'stream_id'])
            except sa.exc.SQLAlchemyError as e:
                logging.error(e)
                sys.exit(1)
        
            # check for any remaining measurements
            if len(measurements):
                num += len(measurements)
            
                # create shape objects
                measurements['g'] = measurements.apply(lambda x: shapely.geometry.Point(x['longitude'], x['latitude']), axis=1)

                # create geodataframe
                measurements = gpd.GeoDataFrame(measurements, geometry='g')
            
                # iterate through geo, find intersection with points                
                res = pd.Series()
                for i, r in measurements.iterrows():
                    # use spatial index to get approximate matches for testing
                    ind = list(sindex.intersection(r['g'].bounds))
                    
                    # set to default loc if no matches
                    if not ind:
                        update_loc(t['column'], DEFAULT_LOC, i, engine)
                    else:   
                        # locations to test
                        tests = geo.iloc[ind]
                        
                        # get actual locations
                        matches = tests[tests.contains(r['g'])]
                        
                        # add to database if any matches
                        if not matches.empty:
                            # update loc
                            update_loc(t['column'], matches.iloc[0].name, i, engine)
                            
                            # warn if multiple matches (overlapping geo?)
                            if matches.shape[0] > 1:
                                logging.warn('found multiple %s for measurement = (%d, %d)' % (t['table'], i[0], i[1]))
                        # set to default loc if no matches
                        else:
                            update_loc(t['column'], DEFAULT_LOC, i, engine)
            
            # otherwise exit
            else:
                logging.info('found %d measurements to locate in %s' % (num, t['table']))
                break

    logging.info('locate meas finished')
