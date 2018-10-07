import sqlalchemy as sa
import pandas as pd
import logging
import sys
import shutil
import os
import glob

CHUNKSIZE = 10000

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
        logging.info('geting data from table %s' % table)
        i = 0
        files = []
        while True:
            try:
                df = pd.read_sql_query('SELECT * FROM %s ORDER BY id ASC LIMIT %d OFFSET %d' % (table, CHUNKSIZE, i*CHUNKSIZE), engine)
            except sa.exc.SQLAlchemyError as e:
                logging.error(e)
                sys.exit(1)
            
            # check for empty df
            if df.size == 0:
                break
            
            # break into multiple files as necessary
            try:
                name = 'backups/tables/%s_%d.csv'% (table, i)
                logging.info('creating file %s' % name)
                header = False if i else True
                df.to_csv(name, index=False, header=header, encoding='utf-8')   
            except:
                e = sys.exc_info()
                logging.error(str(e))
                sys.exit(1)
            
            i += 1
            files.append(name)
        
        # delete destination file, if exists
        try:
            destination = 'backups/tables/%s.csv' % table
            os.remove(destination)
            os.system('touch %s' % destination)
        except OSError:
            pass
        
        # combine files
        try:
            logging.info('combining files into %s' % destination)
            for f in files:
                os.system('cat %s >> %s' % (f, destination))
                os.remove(f)
        except:
            e = sys.exc_info()
            logging.error(str(e))
            sys.exit(1)

    # create zip file
    try:
        name = 'backups/backup_%s' % (pd.Timestamp.now().strftime('%Y%m%d%H%M%S'))
        logging.info('creating archive %s' % name)
        shutil.make_archive(name, 'zip', 'backups/tables')
    except:
        e = sys.exc_info()
        logging.error(str(e))
        sys.exit(1)
    
    # remove old zip files
    logging.info('removing old archives')
    try:
        files = glob.glob('backups/*.zip')
        files.remove(name + '.zip')
        for f in files:
            os.remove(f)
    except:
        e = sys.exc_info()
        logging.error(str(e))
        sys.exit(1)
    
    logging.info('backup finished')