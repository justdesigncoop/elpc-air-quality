import sqlalchemy as sa
import pandas as pd
import requests
import logging
import sys

if __name__ == '__main__':
    # generate error log
    logging.basicConfig(
        filename='db_test_%s.log' % (pd.Timestamp.now().strftime('%Y%m%d%H%M%S')),
        filemode='w',
        format = '%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)
    
    logging.info('db test started')
    
    # create engine
    try:
        engine = sa.create_engine('mysql+mysqlconnector://elpcjd:Elpc1234@127.0.0.1/elpc_air_quality')
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    # get users
    try:
        users = pd.read_sql_query('SELECT * FROM users', engine, index_col='id')
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
        
    # iterate through usernames
    for ui, ur in users.iterrows():
        # check for user's previous sessions (so we don't double process)
        prev_sessions = pd.Series()      
        if pd.notnull(ui):
            # get latest session id from db
            prev_sessions = pd.read_sql_query('SELECT id FROM sessions WHERE user_id = %d' % (int(ui)), engine)['id']

        # api quiery for session list
        params = (('q[usernames]', ur['username']),)
        try:
            response = requests.get('http://aircasting.org/api/sessions.json', params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(e)
            sys.exit(1)
            
        # [s for s in sessions['id'] if s not in prev_sessions]
        
        # sessions dataframe, remove old sessions before processing
        sessions = pd.DataFrame(response.json())
        sessions = sessions[~sessions['id'].isin(prev_sessions)]
        logging.info('adding %d sessions for user %s' % (len(sessions), ur['username']))
        
        # streams and measurements processing
        for si, sr in sessions.iterrows():
            # api query for session
            try:
                response = requests.get('http://aircasting.org/api/sessions/%s.json' % (sr['id']))
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                logging.error(e)
                sys.exit(1)
            
            # process session
            session = pd.Series(response.json())
            session['created_at'] = pd.to_datetime(session['created_at'])
            session['updated_at'] = pd.to_datetime(session['updated_at'])
            session['start_time'] = pd.to_datetime(session['start_time'])
            session['end_time'] = pd.to_datetime(session['end_time'])
            session['start_time_local'] = pd.to_datetime(session['start_time_local'])
            session['end_time_local'] = pd.to_datetime(session['end_time_local'])
            session['last_measurement_at'] = pd.to_datetime(session['last_measurement_at'])
            session.drop('streams', inplace=True)
            session.drop('notes', inplace=True)
            session.drop('measurements_received_count', inplace=True)
            
            # update user id if not in users table
            if pd.isnull(ui):
                try:
                    pd.read_sql_query('UPDATE users SET id = %d WHERE username = \'%s\'' % (session['user_id'], ur['username']), engine)
                    response.raise_for_status()
                except sa.exc.ResourceClosedError as e:
                    #logging.warning(e)
                    pass
                except sa.exc.SQLAlchemyError as e:
                    logging.error(e)
                    sys.exit(1)
            
            # insert into sql
            try:
                pd.DataFrame().append(session, ignore_index=True).to_sql('sessions', engine, index=False, if_exists='append')
            # duplicate entry            
            except sa.exc.IntegrityError as e:
                logging.warning(e)
            except sa.exc.SQLAlchemyError as e:
                logging.error(e)
                sys.exit(1)
                
            # process notes
            if response.json()['notes']:
                notes = pd.DataFrame(response.json()['notes'])
                notes['created_at'] = pd.to_datetime(notes['created_at'])
                notes['updated_at'] = pd.to_datetime(notes['updated_at'])
                notes['date'] = pd.to_datetime(notes['date'])
                notes['photo_updated_at'] = pd.to_datetime(notes['photo_updated_at'])     
                
                # insert into sql
                try:
                    notes.to_sql('notes', engine, index=False, if_exists='append')
                # duplicate entry
                except sa.exc.IntegrityError as e:
                    logging.warning(e)
                except sa.exc.SQLAlchemyError as e:
                    logging.error(e)
                    sys.exit(1)
            
            # process streams
            streams = pd.DataFrame(response.json()['streams']).transpose()
            streams['session_id'] = sr['id']
            streams.drop('measurements', axis=1, inplace=True)
            streams.drop('size', axis=1, inplace=True)
            
            # insert into sql
            try:
                streams.to_sql('streams', engine, index=False, if_exists='append')
            # duplicate entry
            except sa.exc.IntegrityError as e:
                logging.warning(e)
            except sa.exc.SQLAlchemyError as e:
                logging.error(e)
                sys.exit(1)
            
            # iterate through streams
            for s in response.json()['streams']:
                # get stream
                stream = response.json()['streams'][s]
                
                # process measurements
                measurements = pd.DataFrame(stream['measurements'])
                measurements['time'] = pd.to_datetime(measurements['time'])
                measurements['stream_id'] = stream['id']
                
                # insert into sql
                try:
                    measurements.to_sql('measurements', engine, index='id', if_exists='append')
                # duplicate entry
                except sa.exc.IntegrityError as e:
                    logging.warning(e)
                except sa.exc.SQLAlchemyError as e:
                    logging.error(e)
                    sys.exit(1)
    
    logging.info('db test finished')

