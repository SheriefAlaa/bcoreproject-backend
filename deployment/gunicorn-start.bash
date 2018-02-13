#!/bin/bash

NAME="bcoreprojectbackend"                                 # Name of the application
DJANGODIR=/root/bcoreproject/bcoreproject-backend-src   # Django project directory
SOCKFILE=/var/log/gunicorn/gunicorn.sock  		# we will communicte using this unix socket
USER=root                                        	# the user to run as
GROUP=www-data                                     	# the group to run as
NUM_WORKERS=3                                     	# how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE="bcoreproject.settings"		# which settings file should Django use
DJANGO_WSGI_MODULE=bcoreproject.wsgi                       # WSGI module name

mkdir /root/bcoreproject/bcoreproject-backend-src/logs/

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-