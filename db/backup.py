import sqlalchemy as sa
import pandas as pd
import logging
import sys
import shutil
import os
import glob

if __name__ == '__main__':
    # generate error log
    logging.basicConfig(
        filename='logs/backup_%s.log' % (pd.Timestamp.now().strftime('%Y%m%d%H%M%S')),
        filemode='w',
        format = '%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)
    
    logging.info('backup started')
    
    # create engine
    try:
        engine = sa.create_engine('mysql+mysqlconnector://elpcjd:Elpc1234@127.0.0.1/elpc_air_quality')
    except sa.exc.SQLAlchemyError as e:
        logging.error(e)
        sys.exit(1)
    
    # tables to back up
    tables = ['users', 'sessions', 'streams', 'notes', 'measurements', 'neighborhoods', 'tracts', 'wards']
    
    # back up each table
    for table in tables:
        try:
            df = pd.read_sql_query('SELECT * FROM %s' % (table), engine)
        except sa.exc.SQLAlchemyError as e:
            logging.error(e)
            sys.exit(1)
        
        try:
            df.to_csv('backups/tables/%s.csv' % table, index=False, encoding='utf-8')
        except:
            e = sys.exc_info()[0]
            logging.error(e)
            sys.exit(1)
    
    # create zip file
    try:
        name = 'backups/backup_%s' % (pd.Timestamp.now().strftime('%Y%m%d%H%M%S'))
        shutil.make_archive(name, 'zip', 'backups/tables')
    except:
        e = sys.exc_info()[0]
        logging.error(e)
        sys.exit(1)
    
    # remove old zip files
    try:
        files = glob.glob('backups/*.zip')
        files.remove(name + '.zip')
        for file in files:
            os.remove(file)
    except:
        e = sys.exc_info()[0]
        logging.error(e)
        sys.exit(1)
    
    logging.info('backup finished')