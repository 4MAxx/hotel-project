import os
from server.settings import BASE_DIR

DEBUG = True

ALLOWED_HOSTS = []

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]