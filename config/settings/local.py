"""
local settings
"""
from .base import *  # noqa


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ------------------------------------------------------------------------------
INSTALLED_APPS += ["django_extensions"]  # noqa F405
