import sqlalchemy as sa
import pandas as pd
import requests

if __name__ == '__main__':
    # create engine
    engine = sa.create_engine('mysql+mysqlconnector://root:dd00ww@home.danwahl.net/elpc_air_quality')
    
    # get users
    users = pd.read_sql_query('SELECT * FROM users', engine, index_col='id')
    
    # iterate through usernames
    for ui, ur in users.iterrows():
        # api quiery for session list
        params = (('q[usernames]', ur['username']),)
        response = requests.get('http://aircasting.org/api/sessions.json', params=params)
        
        # sessions dataframe
        sessions = pd.DataFrame(response.json())
        
        # streams and measurements processing
        for si, sr in sessions.iterrows():
            # api query for session
            response = requests.get('http://aircasting.org/api/sessions/%s.json' % (sr['id']))
            
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
                pd.read_sql_query('UPDATE users SET id = %d WHERE username = \'%s\'' % (session['user_id'], ur['username']), engine)
            
            # insert into sql
            pd.DataFrame().append(session, ignore_index=True).to_sql('sessions', engine, index=False, if_exists='append')
                
            # process streams
            streams = pd.DataFrame(response.json()['streams']).transpose()
            streams['session_id'] = sr['id']
            streams.drop('measurements', axis=1, inplace=True)
            streams.drop('size', axis=1, inplace=True)
            
            # insert into sql
            streams.to_sql('streams', engine, index=False, if_exists='append')
            
            # iterate through streams
            for s in response.json()['streams']:
                # get stream
                stream = response.json()['streams'][s]
                
                # process measurements
                measurements = pd.DataFrame(stream['measurements'])
                measurements['time'] = pd.to_datetime(measurements['time'])
                measurements['stream_id'] = stream['id']
                
                # insert into sql
                measurements.to_sql('measurements', engine, index='id', if_exists='append')
    
    # get sessions
    #sessions = pd.read_sql_query('SELECT * FROM sessions', engine, index_col='id', parse_dates=['start_time_local', 'end_time_local'])