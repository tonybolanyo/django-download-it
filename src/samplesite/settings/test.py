import sys
from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

EMAIL_BACKEND = 'django.core.email.backends.locmem.EmailBackend'

if sys.platform.startswith('win32'):
    MAGIC_FILE = 'c:\windows\system32\magic.mgc'
