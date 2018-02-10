import sys
import os
import glob
import pandas as pd
from StringIO import StringIO

DELIM = 'sensor:model,sensor:package,sensor:capability,sensor:units\n'

if __name__ == '__main__':
    # get path
    if len(sys.argv) > 1:
        path = sys.argv[1]
        
        # check for valid path
        if not os.path.exists(path):
            print 'invalid path to folder'
            sys.exit()   
    else:
        print 'please supply path to folder, e.g.:'
        print '  > python elpc_test.py C:\\path\\to\\sessions\\folder'
        sys.exit()
    
    # get csv files
    os.chdir(path)
    files = [i for i in glob.glob('*.{}'.format('csv'))]
    
    # create analysis dataframe
    cols = ['name', 'sensor', 'max', 'min', 'mean', 'median']
    data = pd.DataFrame(columns=cols)
    
    # iterate through files
    for n in files:
        # open file
        with open(n, 'r') as f:
            # read data, split by delim
            raw = f.read()
            logs = filter(None, raw.split(DELIM))
            
            # get session id
            tags = n.split('_')
            session = int(tags[1])
            name = tags[2]
            
            # parse each sensor log
            for log in logs:
                # split first line
                l = log.split('\n', 1)
                
                # get sensor type
                sensor = l[0].split(',')[2]
                
                # create directory for sensor
                if not os.path.exists(sensor):
                    os.makedirs(sensor)
                
                # create log dataframe
                df = pd.read_csv(StringIO(l[1]), parse_dates=[0])
                df.to_csv(sensor + '\\' + str(session) + '_' + name + '.csv')
                
                # add to data
                val = df['Value']
                data = data.append(pd.Series([name, sensor, val.max(), val.min(), \
                    val.mean(), val.median()], index=cols, name=session))
    
    # save analysis for each sensor type
    for sensor in data['sensor'].unique():
        data[data['sensor'] == sensor].to_csv(sensor + '\\Analysis.csv')
