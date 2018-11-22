import sqlalchemy as sa
import pandas as pd
import logging
import sys

TRACTS_FILE = 'CensusTractsTIGER2010.csv'
NEIGHBORHOODS_FILE = 'Neighborhoods_2012b.csv'
WARDS_FILE = 'WARDS_2015.csv'
HEXAGONS_FILE = 'hex.csv'

DEFAULT_LOC = 0

# https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
#ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])

if __name__ == '__main__':
    # generate error log
    logging.basicConfig(
        filename='import_geo_%s.log' % (pd.Timestamp.now().strftime('%Y%m%d%H%M%S')),
        filemode='w',
        format = '%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)
    
    logging.info('import geo started')
    
    # create engine
    try:
        engine = sa.create_engine('mysql+mysqlconnector://elpcjd:Elpc1234@home.danwahl.net/elpc_air_quality')
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    # process tracts file
    tracts = pd.read_csv(TRACTS_FILE, usecols=['GEOID10', 'the_geom'])
    tracts.rename(index=str, columns={'GEOID10': 'id', 'the_geom': 'geo'}, inplace=True)
    tracts['display'] = tracts['id'].astype(str)
    tracts = tracts.append(pd.Series({'id': DEFAULT_LOC, 'display': 'None', 'geo': 'MULTIPOLYGON EMPTY'}), ignore_index=True)
    
    print tracts
    
    '''
    # insert into sql
    try:
        tracts.to_sql('tracts', engine, index=False, if_exists='append')
    # duplicate entry
    except sa.exc.IntegrityError as e:
        logging.warning(e)
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    '''

    # process neighborhoods file
    neighborhoods = pd.read_csv(NEIGHBORHOODS_FILE, usecols=['PRI_NEIGH', 'the_geom'])
    neighborhoods.rename(index=str, columns={'PRI_NEIGH': 'display', 'the_geom': 'geo'}, inplace=True)
    neighborhoods['id'] = range(1, len(neighborhoods) + 1);
    neighborhoods = neighborhoods.append(pd.Series({'id': DEFAULT_LOC, 'display': 'None', 'geo': 'MULTIPOLYGON EMPTY'}), ignore_index=True)
    
    print neighborhoods
    
    '''
    # insert into sql
    try:
        neighborhoods.to_sql('neighborhoods', engine, index=False, if_exists='append')
    # duplicate entry
    except sa.exc.IntegrityError as e:
        logging.warning(e)
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    '''
    
    # process wards file
    wards = pd.read_csv(WARDS_FILE, usecols=['WARD', 'the_geom'])
    wards.rename(index=str, columns={'WARD': 'id', 'the_geom': 'geo'}, inplace=True)
    wards['display'] = wards['id'].astype(str)
    #wards['display'] = [str(ordinal(id)) + ' Ward' for id in wards['id'].tolist()];
    wards = wards.append(pd.Series({'id': DEFAULT_LOC, 'display': 'None', 'geo': 'MULTIPOLYGON EMPTY'}), ignore_index=True)
    
    print wards
    
    '''
    # insert into sql
    try:
        wards.to_sql('wards', engine, index=False, if_exists='append')
    # duplicate entry
    except sa.exc.IntegrityError as e:
        logging.warning(e)
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    '''
    
    # process hexagons file
    hexagons = pd.read_csv(HEXAGONS_FILE)
    hexagons['display'] = hexagons['id'].astype(str)
    hexagons = hexagons.append(pd.Series({'id': DEFAULT_LOC, 'display': 'None', 'geo': 'MULTIPOLYGON EMPTY'}), ignore_index=True)
    
    print hexagons
    
    # insert into sql
    try:
        hexagons.to_sql('hexagons', engine, index=False, if_exists='append')
    # duplicate entry
    except sa.exc.IntegrityError as e:
        logging.warning(e)
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
	
    logging.info('import geo finished')
    