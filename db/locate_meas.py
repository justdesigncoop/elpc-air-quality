import sqlalchemy as sa
import pandas as pd
import logging
import sys
import shapely.wkt

#from memory_profiler import profile

DEFAULT_LOC = 0
CHUNKSIZE = 10000

#@profile
def locate_meas(im, rm, p, prev, name, geo, engine):
    # check to see if already located
    if pd.isnull(rm[name]):
        # check previuos (most likely to be in the same boundary)
        if p.within(geo.loc[prev]['g']):
            try:
                pd.read_sql_query('UPDATE measurements SET %s = %d WHERE id = %d and stream_id = %d' % (name, prev, im, rm['stream_id']), engine)
            except sa.exc.ResourceClosedError as e:
                #logging.warning(e)
                pass
            except sa.exc.SQLAlchemyError as e:
                logging.error(e)
                sys.exit(1)
            # return geo boundary
            return prev
    
        # iterate through all geo boundaries
        for ig, rg in geo.iterrows(): 
            # update measurement and return if within boundary
            if p.within(rg['g']):
                try:
                    pd.read_sql_query('UPDATE measurements SET %s = %d WHERE id = %d and stream_id = %d' % (name, ig, im, rm['stream_id']), engine)
                except sa.exc.ResourceClosedError as e:
                    #logging.warning(e)
                    pass
                except sa.exc.SQLAlchemyError as e:
                    logging.error(e)
                    sys.exit(1)
                # return geo boundary
                return ig
        
        # if not found, set to default
        try:
            pd.read_sql_query('UPDATE measurements SET %s = %d WHERE id = %d and stream_id = %d' % (name, DEFAULT_LOC, im, rm['stream_id']), engine)
        except sa.exc.ResourceClosedError as e:
            #logging.warning(e)
            pass
        except sa.exc.SQLAlchemyError as e:
            logging.error(e)
            sys.exit(1)
    
    # return default lox
    return DEFAULT_LOC

if __name__ == '__main__':
    # generate error log
    logging.basicConfig(
        filename='locate_meas_%s.log' % (pd.Timestamp.now().strftime('%Y%m%d%H%M%S')),
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
        {'table': 'census', 'index': 'tract', 'column': 'tract_id'},
        {'table': 'neighborhoods', 'index': 'id', 'column': 'neighborhood_id'},
        {'table': 'wards', 'index': 'ward', 'column': 'ward_id'},
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
        
        num = 0
        while True:
			# get reaining measurements (chunksize limit)
			try:
				measurements = pd.read_sql_query('SELECT * FROM measurements WHERE %s IS NULL ORDER BY stream_id, id LIMIT %d' % (t['column'], CHUNKSIZE), engine, index_col='id')
			except sa.exc.SQLAlchemyError as e:
				logging.error(e)
				sys.exit(1)
			
			# check for any remaining measurements
			if len(measurements):
				num += len(measurements)
				# iterate through measurements
				prev = DEFAULT_LOC
				for im, rm in measurements.iterrows():
					# create point
					p = shapely.geometry.Point(rm['longitude'], rm['latitude'])
							
					# locate point, store previous location for next loop
					prev = locate_meas(im, rm, p, prev, t['column'], geo, engine)
			# otherwise exit
			else:
				logging.info('found %d measurements to locate in %s' % (num, t['table']))
				break
    
    logging.info('locate meas finished')
