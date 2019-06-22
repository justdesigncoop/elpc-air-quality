import sqlalchemy as sa
import pandas as pd
import logging
import sys

SENSOR_NAMES = ['AirBeam-PM', 'AirBeam2-PM2.5']

HARMFUL_LEVEL = 35.0

GOOD_LEVEL = 12.0

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
    
    # get sensor names    
    sensor_names = ','.join(['\'' + sensor + '\'' for sensor in SENSOR_NAMES])
    
    '''
    # get hexagons
    try:
        hexagons = pd.read_sql_query('SELECT id, geo FROM hexagons', engine, index_col=['id'])
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    '''
    
    # get sessions
    try:
        sessions = pd.read_sql_query('SELECT id FROM sessions WHERE user_id in (SELECT id FROM users WHERE private is FALSE)', engine, index_col=['id'])
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    # get session ids
    session_ids = ','.join([str(session_id) for session_id in sessions.index])
    
    # get counts
    try:
        counts = pd.read_sql_query('SELECT hexagon_id, COUNT(value) AS counts FROM measurements WHERE stream_id in (SELECT id FROM streams WHERE sensor_name IN (%s) AND session_id in (%s)) AND hexagon_id IS NOT NULL GROUP BY hexagon_id' % \
            (sensor_names, session_ids), engine, index_col=['hexagon_id'])
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)    
        
    # get harmful
    try:
        harmful = pd.read_sql_query('SELECT hexagon_id, COUNT(value) AS harmful FROM measurements WHERE value >= %f AND stream_id in (SELECT id FROM streams WHERE sensor_name IN (%s) AND session_id in (%s)) AND hexagon_id IS NOT NULL GROUP BY hexagon_id' % \
            (HARMFUL_LEVEL, sensor_names, session_ids), engine, index_col=['hexagon_id'])
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    # fill na with 0
    harmful = harmful.reindex(counts.index).fillna(0)
        
    # get good
    try:
        good = pd.read_sql_query('SELECT hexagon_id, COUNT(value) AS good FROM measurements WHERE value <= %f AND stream_id in (SELECT id FROM streams WHERE sensor_name IN (%s) AND session_id in (%s)) AND hexagon_id IS NOT NULL GROUP BY hexagon_id' % \
            (GOOD_LEVEL, sensor_names, session_ids), engine, index_col=['hexagon_id'])
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)  
    
    # fill na with 0   
    good = good.reindex(counts.index).fillna(0)
    
    # get average
    try:
        average = pd.read_sql_query('SELECT hexagon_id, AVG(value) AS average FROM measurements WHERE stream_id in (SELECT id FROM streams WHERE sensor_name IN (%s) AND session_id in (%s)) AND hexagon_id IS NOT NULL GROUP BY hexagon_id' % \
            (sensor_names, session_ids), engine, index_col=['hexagon_id'])
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    '''
    # get health score
    health_score = pd.read_csv('health_score.csv', index_col=['hexagon_id'])
    
    # average across duplicate indices
    health_score = health_score.groupby(health_score.index).mean()
    
    data = pd.concat([hexagons, average, counts, harmful, good, health_score], axis=1, join='inner')
    '''
    data = pd.concat([counts, harmful, good, average], axis=1, join='inner')
    
    # update rows
    conn = engine.connect()
    
    # empty columns in hexagons
    query = 'UPDATE hexagons SET counts = NULL, average = NULL, harmful = NULL, good = NULL'
    try:
        conn.execute(query)
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    # update with new data
    for ind, row in data.iterrows():
        #query = 'UPDATE hexagons SET counts = %d, average = %f, harmful = %f, good = %f, health_score = %f WHERE id = %d' % (row['counts'], row['average'], row['harmful'], row['good'], row['health_score'], ind)
        query = 'UPDATE hexagons SET counts = %d, average = %f, harmful = %f, good = %f WHERE id = %d' % (row['counts'], row['average'], row['harmful'], row['good'], ind)
        try:
            conn.execute(query)
        except sa.exc.SQLAlchemyError as e:
            logging.error(e)
            sys.exit(1)
    conn.close()
    
    #data.to_json('../app/static/dashboard/data.json');
    
    logging.info('update data finished')
