# -*- coding: utf-8 -*-
import os
from urlparse import urlparse

if os.environ.get('container') == 'lxc':
    MONGO_ENV_NAME = 'MONGODB_PORT'
else:
    MONGO_ENV_NAME = 'MONGO_DATABASE_HOST'

MONGODB_SETTINGS = {
    'DB': os.environ.get('MONGO_DATABASE_NAME', 'apollo'),
    'HOST': urlparse(os.environ.get(MONGO_ENV_NAME, 'mongodb://localhost')).netloc
}
SECURITY_URL_PREFIX = '/accounts'
SECURITY_LOGIN_USER_TEMPLATE = 'frontend/login_user.html'

LANGUAGES = {
    'en': 'English',
    'es': 'Español',
    'fr': 'Français',
    'az': 'Azərbaycanca',
    'ar': 'العربية',
    'de': 'Deutsch',
}

SECRET_KEY = os.environ.get('SECRET_KEY', 'SOMETHING_SECURE')
DEBUG = os.environ.get('DEBUG', False)
