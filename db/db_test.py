import sqlalchemy as sa
import pandas as pd
import requests

if __name__ == '__main__':
    # create engine
    engine = sa.create_engine('mysql+mysqlconnector://root:dd00ww@home.danwahl.net/elpc_air_quality')
    
    # api quiery
    params = (
        ('q[usernames]', 'JustDesign'),
    )
    response = requests.get('http://aircasting.org/api/sessions.json', params=params)
    
    # sessions dataframe
    sessions = pd.DataFrame(response.json())
    sessions['start_time_local'] = pd.to_datetime(sessions['start_time_local'])
    sessions['end_time_local'] = pd.to_datetime(sessions['end_time_local'])
    sessions.drop('streams', axis=1, inplace=1)
    
    # insert sessions
    sessions.to_sql('sessions', engine, index=False, if_exists='append')
    
    # get sessions
    sessions = pd.read_sql_query('SELECT * FROM sessions', engine, index_col='id', parse_dates=['start_time_local', 'end_time_local'])