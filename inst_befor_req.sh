#!/bin/bash
# для установки библиотеки mysqlclient for Django на системе Ubuntu 20.04
# а также установка nginx, git, supervisor, venv
sudo apt-get install python3-distutils
sudo apt-get install python-dev
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
sudo apt install nginx git supervisor
sudo apt install python3-virtualenv