import sqlalchemy as sa
import pandas as pd
import logging
import sys
import shapely.wkt

def locate_meas(im, rm, p, name, geo, engine):
    # check to see if already located
    if pd.isnull(rm[name]):
        # iterate through geo boundaries
        found = False
        for ig, rg in geo.iterrows(): 
            # update measurement and break if within boundary
            if p.within(rg['g']):
                found = True
                try:
                    pd.read_sql_query('UPDATE measurements SET %s = %d WHERE id = %d and stream_id = %d' % (name, ig, im, rm['stream_id']), engine)
                except sa.exc.ResourceClosedError as e:
                    #logging.warning(e)
                    pass
                except sa.exc.SQLAlchemyError as e:
                    logging.error(e)
                    sys.exit(1)
                break
        
        # if not found, set to 0
        if not found:
            try:
                pd.read_sql_query('UPDATE measurements SET %s = %d WHERE id = %d and stream_id = %d' % (name, 0, im, rm['stream_id']), engine)
            except sa.exc.ResourceClosedError as e:
                #logging.warning(e)
                pass
            except sa.exc.SQLAlchemyError as e:
                logging.error(e)
                sys.exit(1)

if __name__ == '__main__':
    # generate error log
    logging.basicConfig(
        filename='locate_meas_%s.log' % (pd.Timestamp.now().strftime('%Y%m%d%H%M%S')),
        filemode='w',
        format = '%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG)
    
    logging.info('locate meas started')
    
    # create engine
    try:
        engine = sa.create_engine('mysql+mysqlconnector://elpcjd:Elpc1234@127.0.0.1/elpc_air_quality')
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    # get census
    try:
        census = pd.read_sql_query('SELECT * FROM census', engine, index_col='tract')
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)

    # get neighborhoods
    try:
        neighborhoods = pd.read_sql_query('SELECT * FROM neighborhoods', engine, index_col='id')
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)

    # get wards
    try:
        wards = pd.read_sql_query('SELECT * FROM wards', engine, index_col='ward')
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)

    # create shape objects
    census['g'] = census['geo'].apply(shapely.wkt.loads)
    neighborhoods['g'] = neighborhoods['geo'].apply(shapely.wkt.loads)
    wards['g'] = wards['geo'].apply(shapely.wkt.loads)
    
    # get reaining measurements
    try:
        measurements = pd.read_sql_query('SELECT * FROM measurements WHERE (tract IS NULL OR neighborhood IS NULL OR ward IS NULL)', engine, index_col='id')
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    # iterate through measurements
    logging.info('found %d measurements to locate' % len(measurements))
    for im, rm in measurements.iterrows():
        #p = shapely.geometry.Point(-87.61, 41.81)
        p = shapely.geometry.Point(rm['longitude'], rm['latitude'])
        #print rm
                
        # check census
        locate_meas(im, rm, p, 'tract', census, engine)
        
        # check neighborhoods
        locate_meas(im, rm, p, 'neighborhood', neighborhoods, engine)
        
        # check wards
        locate_meas(im, rm, p, 'ward', wards, engine)
    
    '''
    # delete rows that have no valid neighborhood, tract, or census
    try:
        pd.read_sql_query('DELETE FROM measurements WHERE (tract IS NULL AND neighborhood IS NULL AND ward IS NULL)', engine, index_col='id')
    except sa.exc.ResourceClosedError as e:
        #logging.warning(e)
        pass
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    '''
    
    logging.info('locate meas finished')
