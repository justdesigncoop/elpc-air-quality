import sqlalchemy as sa
import pandas as pd
import logging
import sys

CENSUS_FILE = 'CensusTractsTIGER2010.csv'
NEIGHBORHOODS_FILE = 'Neighborhoods_2012b.csv'
WARDS_FILE = 'WARDS_2015.csv'

if __name__ == '__main__':
    # generate error log
    logging.basicConfig(
        filename='db_test_%s.log' % (pd.Timestamp.now().strftime('%Y%m%d%H%M%S')),
        filemode='w',
        format = '%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG)
    
    logging.info('import geo started')
    
    # create engine
    try:
        engine = sa.create_engine('mysql+mysqlconnector://elpcjd:Elpc1234@127.0.0.1/elpc_air_quality')
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    # process census file
    census = pd.read_csv(CENSUS_FILE, usecols=['GEOID10', 'the_geom'])
    census.rename(index=str, columns={'GEOID10': 'tract', 'the_geom': 'geo'}, inplace=True)
    
    # insert into sql
    try:
        census.to_sql('census', engine, index=False, if_exists='append')
    # duplicate entry
    except sa.exc.IntegrityError as e:
        logging.warning(e)
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)

    # process neighborhoods file
    neighborhoods = pd.read_csv(NEIGHBORHOODS_FILE, usecols=['PRI_NEIGH', 'the_geom'])
    neighborhoods.rename(index=str, columns={'PRI_NEIGH': 'neighborhood', 'the_geom': 'geo'}, inplace=True)
    
    # insert into sql
    try:
        neighborhoods.to_sql('neighborhoods', engine, index=False, if_exists='append')
    # duplicate entry
    except sa.exc.IntegrityError as e:
        logging.warning(e)
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    # process wards file
    wards = pd.read_csv(WARDS_FILE, usecols=['WARD', 'the_geom'])
    wards.rename(index=str, columns={'WARD': 'ward', 'the_geom': 'geo'}, inplace=True)
    
    # insert into sql
    try:
        wards.to_sql('wards', engine, index=False, if_exists='append')
    # duplicate entry
    except sa.exc.IntegrityError as e:
        logging.warning(e)
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)

    logging.info('import geo finished')
    