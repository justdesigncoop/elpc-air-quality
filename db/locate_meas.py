import sqlalchemy as sa
import pandas as pd
import logging
import sys
import shapely

if __name__ == '__main__':
    # generate error log
    logging.basicConfig(
        filename='db_test_%s.log' % (pd.Timestamp.now().strftime('%Y%m%d%H%M%S')),
        filemode='w',
        format = '%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG)
    
    logging.info('locate meas started')
    
    # create engine
    try:
        engine = sa.create_engine('mysql+mysqlconnector://elpcjd:Elpc1234@home.danwahl.net/elpc_air_quality')
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
    
    # get measurements
    try:
        measurements = pd.read_sql_query('SELECT * FROM measurements', engine, index_col='id')
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    # iterate through measurements
    for im, rm in measurements.iterrows():
        #p = shapely.geometry.Point(-87.61, 41.81)
        p = shapely.geometry.Point(rm['longitude'], rm['latitude'])
        #print p
        
        # check census
        if not rm['tract']:
            for ig, rg in census.iterrows():      
                if p.within(rg['g']):
                    try:
                        pd.read_sql_query('UPDATE measurements SET tract = %d WHERE id = %d and stream_id = %d' % (ig, im, rm['stream_id']), engine)
                    except sa.exc.ResourceClosedError as e:
                        logging.warning(e)
                    except sa.exc.SQLAlchemyError as e:
                        logging.error(e)
                        sys.exit(1)
                    break
        
        # check neighborhoods
        if not rm['neighborhood_id']:
            for ig, rg in neighborhoods.iterrows():      
                if p.within(rg['g']):
                    try:
                        pd.read_sql_query('UPDATE measurements SET neighborhood_id = %d WHERE id = %d and stream_id = %d' % (ig, im, rm['stream_id']), engine)
                    except sa.exc.ResourceClosedError as e:
                        logging.warning(e)
                    except sa.exc.SQLAlchemyError as e:
                        logging.error(e)
                        sys.exit(1)
                    break
        
        # check wards
        if not rm['ward']:
            for ig, rg in wards.iterrows():      
                if p.within(rg['g']):
                    try:
                        pd.read_sql_query('UPDATE measurements SET ward = %d WHERE id = %d and stream_id = %d' % (ig, im, rm['stream_id']), engine)
                    except sa.exc.ResourceClosedError as e:
                        logging.warning(e)
                    except sa.exc.SQLAlchemyError as e:
                        logging.error(e)
                        sys.exit(1)
                    break
    
    logging.info('locate meas finished')