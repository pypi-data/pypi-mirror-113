import logging.config

__all__ = ['set_log_conf']

_LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(message)s',
            'datefmt': "%H:%M:%S",
        },
        'debug': {
            'format': '[%(levelname)s] %(module)s:%(funcName)s %(name)s: %(message)s',
            'datefmt': "%H:%M:%S",
        },
    },
    'handlers': {
        'standard': {
            'level': 'WARNING',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'debug': {
            'level': 'DEBUG',
            'formatter': 'debug',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {},
    },
}

_STANDARD_LOGGER = {
    'handlers': ['standard'],
    'level': 'INFO',
    'propagate': False,
}

_DEBUG_LOGGER = {
    'handlers': ['standard'],
    'level': 'INFO',
    'propagate': False,
}


def set_log_conf(debug: bool = False):
    if debug:
        _LOG_CONFIG['loggers'][''] = _DEBUG_LOGGER
    else:
        _LOG_CONFIG['loggers'][''] = _STANDARD_LOGGER
    logging.config.dictConfig(_LOG_CONFIG)
