from pathlib import Path
import os
import sys

from . import get_env_variable


BASE_DIR = str(Path(__file__).resolve().parent.parent)
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'apps'))

SECRET_KEY = get_env_variable("SECRET_KEY")

DEBUG = get_env_variable("DEBUG")

ADMIN_SITE_URL = get_env_variable("ADMIN_SITE_URL")

BOT_API = get_env_variable("BOT_API")

# CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOWED_ORIGINS = [
#     'http://52.59.208.159:8000'
# ]
# CORS_ALLOWED_ORIGIN_REGEXES = [
#     'http://52.59.208.159:8000'
# ]

ALLOWED_HOSTS = [
    "52.59.208.159",
    "172.31.17.173"
]

ROOT_URLCONF = 'settings.urls'

WSGI_APPLICATION = 'deploy.wsgi.application'

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'auths.CustomUser'