#!/bin/bash

NAME="celery_worker_start"

PROJECT_DIR=/home/john/hotel-project/
ENV_DIR=/home/john/venv/

#echo "Starting $NAME as `celery`"

# Activate the virtual environment
cd "${PROJECT_DIR}"

if [ -d "${ENV_DIR}" ]
then
    . "${ENV_DIR}bin/activate"
fi
    celery -A server worker --loglevel='INFO'