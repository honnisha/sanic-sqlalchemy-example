import os

SECRET_KEY = "8e06922f-b52e-4203-ba61-66d54594e49e"

DATABASES = {}

HOST_IP = os.environ.get('BACKEND_IP', '0.0.0.0')
HOST_PORT = os.environ.get('BACKEND_PORT', '8000')

DEBUG = os.environ.get('DEBUG', 'True')

MONGO_COLLECTION_LOGGER = 'logger'

LOGGER_SETTINGS = {
    'version': 1,
    'formatters': {
        'default': {
             'format': '%(asctime)s %(levelname)s - %(message)s',
         }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default',
            'level': 'DEBUG',
         },
    },
    'loggers': {
        'statistics': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    },
}

try:
    from local_settings import *
except ImportError:
    pass
