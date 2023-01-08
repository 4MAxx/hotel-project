import os
from server.settings import BASE_DIR

DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "64.225.72.86", "hotel.manicbrand.com"]
CSRF_TRUSTED_ORIGINS = ["http://hotel.manicbrand.com"]

# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')