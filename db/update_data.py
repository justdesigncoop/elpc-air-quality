import sqlalchemy as sa
import pandas as pd
import logging

sensor_names = ['AirBeam-PM', 'AirBeam2-PM2.5']

if __name__ == '__main__':
    # generate error log
    logging.basicConfig(
        filename='logs/update_data_%s.log' % (pd.Timestamp.now().strftime('%Y%m%d%H%M%S')),
        filemode='w',
        format = '%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)
    
    logging.info('update data started')
    
    # create engine
    try:
        engine = sa.create_engine('mysql+mysqlconnector://elpcjd:Elpc1234@127.0.0.1/elpc_air_quality')
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    # get sensors    
    sensors = ','.join(['\'' + sensor + '\'' for sensor in sensor_names])
    
    # get averages
    try:
        averages = pd.read_sql_query('SELECT hexagon_id, AVG(value) AS averages FROM measurements WHERE stream_id in (SELECT id FROM streams WHERE sensor_name IN (%s)) AND hexagon_id IS NOT NULL GROUP BY hexagon_id' % \
            sensors, engine, index_col=['hexagon_id'])
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    # get counts
    try:
        counts = pd.read_sql_query('SELECT hexagon_id, COUNT(value) AS counts FROM measurements WHERE stream_id in (SELECT id FROM streams WHERE sensor_name IN (%s)) AND hexagon_id IS NOT NULL GROUP BY hexagon_id' % \
            sensors, engine, index_col=['hexagon_id'])
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    # get hexagons
    try:
        hexagons = pd.read_sql_query('SELECT id, geo FROM hexagons', engine, index_col=['id'])
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    data = pd.concat([hexagons, averages, counts], axis=1, join='inner')
    
    data.to_json('../app/static/dashboard/data.json');
    
    logging.info('update data finished')
