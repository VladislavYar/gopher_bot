from datetime import timezone
from pathlib import Path
from encodings import utf_8
import os

from apscheduler.jobstores.redis import RedisJobStore
from dotenv import load_dotenv
from django.core.management.utils import get_random_secret_key


BASE_DIR = Path(__file__).resolve().parent.parent

ENV_DIR = os.path.join(BASE_DIR, '..', 'infra', '.env')

load_dotenv(ENV_DIR)

SECRET_KEY = os.getenv('SECRET_KEY', default=get_random_secret_key())

LOCAL, DEV, PRODUCTION = 'local', 'dev', 'prod'

SERVER_ENVIRONMENT = os.environ.get('SERVER_ENVIRONMENT', LOCAL)

DEBUG = True
if SERVER_ENVIRONMENT == PRODUCTION:
    DEBUG = False

MEDIA_ROOT = os.getenv(
    'MEDIA_ROOT',
    default=os.path.join(BASE_DIR, 'media'),
)
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.getenv(
        'STATICFILES_DIR',
        default=os.path.join(BASE_DIR, 'static'),
    ),
)

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv(
    'CSRF_TRUSTED_ORIGINS',
    default='http://127.0.0.1,http://localhost',
).split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'admin_extra_buttons',
    'contents.apps.ContentsConfig',
    'user.apps.UserConfig',
    'bot.apps.BotConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_asgi_lifespan.middleware.LifespanStateMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (os.path.join(BASE_DIR, 'templates'),),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', default='django.db.backends.postgresql'),
        'NAME': os.getenv('POSTGRES_DB', default='postgres'),
        'USER': os.getenv('POSTGRES_USER', default='postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
        'HOST': os.getenv('DB_HOST', default='localhost'),
        'PORT': os.getenv('DB_PORT', default='5432'),
    },
}

REDIS_HOST = os.getenv('REDIS_HOST', default='localhost')
REDIS_PORT = os.getenv('REDIS_PORT', default='6379')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', default='redis')
REDIS_LOCATION = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'{REDIS_LOCATION}/0',
        'TIMEOUT': 3600,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}

SCHEDULER_JOBSTORES = {
    'default': RedisJobStore(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
    ),
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CKEDITOR_UPLOAD_PATH = '/uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'allowedContent': {
            'strong em u s a': {
                'attributes': True,
                'styles': False,
                'classes': False,
            }
        },
        'autoParagraph': False,
        'basicEntities': False,
        'enterMode': 2,
        'extraPlugins': ['autocomplete', 'emoji', 'textmatch', 'textwatcher'],
        'forcePasteAsPlainText': True,
        'height': 300,
        'ignoreEmptyParagraph': True,
        'language': 'ru',
        'removePlugins': 'stylesheetparser',
        'resize_enabled': False,
        'toolbar': 'Custom',
        'toolbarCanCollapse': False,
        'toolbar_Custom': (
            {
                'items': (
                    'NewPage',
                    'Preview',
                    '-',
                    'Undo',
                    'Redo',
                    '-',
                    'Copy',
                    'Paste',
                    'Cut',
                    '-',
                    'Find',
                    'Replace',
                    '-',
                    'Maximize',
                    '-',
                    'About',
                    'SelectAll',
                    '-',
                    'Bold',
                    'Italic',
                    'Underline',
                    'Strike',
                    'RemoveFormat',
                    '-',
                    'Link',
                    'Unlink',
                    '-',
                    'SpecialChar',
                    'EmojiPanel',
                ),
            },
        ),
    },
}

ENCODING = os.environ.get('ENCODING', utf_8.getregentry().name)

LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', 'ru-RU')

TIME_ZONE = os.environ.get('TIME_ZONE', str(timezone.utc))

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BOT_TOKEN = os.environ.get('BOT_TOKEN')

BOT_CHANNEL = os.environ.get('BOT_CHANNEL')

BOT_CHAT = os.environ.get('BOT_CHAT')

DEEPSEEK_TOKEN = os.environ.get('DEEPSEEK_TOKEN')

DEEPSEEK_URL = os.environ.get('DEEPSEEK_URL')

DEEPSEEK_SYSTEM_PROMPT_PRAIRIE_DOG = os.environ.get('DEEPSEEK_SYSTEM_PROMPT_PRAIRIE_DOG')

DEEPSEEK_TEMPERATURE_PRAIRIE_DOG = float(os.environ.get('DEEPSEEK_TEMPERATURE_PRAIRIE_DOG'))

DEEPSEEK_MAX_TOKENS_PRAIRIE_DOG = int(os.environ.get('DEEPSEEK_MAX_TOKENS_PRAIRIE_DOG'))
