"""
local settings
"""

from .base import *  # noqa


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY
# your site host
ALLOWED_HOSTS = ['*']

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s : %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './log/app.log',  # 日志输出文件
            'maxBytes': 1024*1024*5,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'verbose',  # 使用哪种formatters日志格式
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
