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
    
    # back up each table, beaking breaking into multiple files as necessary
    for table in tables:     
        try:
            gen = pd.read_sql_query('SELECT * FROM %s' % (table), engine, chunksize=CHUNKSIZE)
        except sa.exc.SQLAlchemyError as e:
            logging.error(e)
            sys.exit(1)
        
        i = 0
        files = []
        for df in gen:
            try:
                name = 'backups/tables/%s_%d.csv'% (table, i)
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
        shutil.make_archive(name, 'zip', 'backups/tables')
    except:
        e = sys.exc_info()
        logging.error(str(e))
        sys.exit(1)
    
    # remove old zip files
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