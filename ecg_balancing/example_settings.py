# -*- coding: utf-8- -*-

from __future__ import unicode_literals
from .default_settings import *

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.mysql',
        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

ADMINS = (
    #('Name', 'name@example.com')
)
MANAGERS = ADMINS

DEBUG = False  # <<<<< SET TO `False` ON staging AND production


#TEMPLATE_DEBUG = DEBUG


### !!! WARNING !!!
###
### CHANGE THIS IN THE PRODUCTION ENVIRONMENT
SECRET_KEY = None  # <<<<< SET A SECRET KEY
###
### !!! WARNING !!!