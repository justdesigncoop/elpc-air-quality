#! /bin/bash    

# setup for virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME
source /usr/local/bin/virtualenvwrapper.sh

# activate workspace
workon elpcjd

# get script location (from argument)
#SCRIPT_HOME=${1:-/home/elpcjd/elpc-air-quality/db}
SCRIPT_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $SCRIPT_HOME

# run scripts
python db_test.py
python locate_meas.py

# deactivate workspace
deactivate
