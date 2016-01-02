#!/bin/bash

source $WRIST_HOME/bin/activate
pip install -r $WRIST_HOME/bin/requirements.txt
python $WRIST_HOME/src/wrist/manage.py collectstatic
nohup uwsgi --ini $WRIST_HOME/bin/wrist.ini &
echo "success"
