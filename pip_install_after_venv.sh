#!/bin/bash
# для установки зависимостей для проекта, а также gunicorn
# запускать после активации venv
pip install -U wheel
pip install mysqlclient
pip install -r requirements.txt
pip install gunicorn
