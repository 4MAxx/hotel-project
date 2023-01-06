#!/bin/bash
# для установки библиотеки mysqlclient for Django на системе Ubuntu 20.04
# запускать перед установкой зависимостей проекта, после установки питона python3.
sudo apt-get install python3-distutils
sudo apt-get install python-dev
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install -U wheel
pip install mysqlclient
