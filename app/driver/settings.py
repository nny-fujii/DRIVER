"""
Django settings for driver project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEVELOP = True if os.environ.get('DJANGO_ENV', 'development') == 'development' else False
STAGING = True if os.environ.get('DJANGO_ENV', 'staging') == 'staging' else False
PRODUCTION = not DEVELOP and not STAGING

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEVELOP

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',

    'django_extensions',
    'djangooidc',

    'ashlar',

    'driver_auth',
    'data',
    'user_filters',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

ROOT_URLCONF = 'driver.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'driver.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DRIVER_DB_NAME', 'postgres'),
        'HOST': os.environ.get('DRIVER_DB_HOST', 'localhost'),
        'PORT': os.environ.get('DRIVER_DB_PORT', 5432),
        'USER': os.environ.get('DRIVER_DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DRIVER_DB_PASSWORD', 'postgres'),
        'CONN_MAX_AGE': 3600,  # in seconds
        'OPTIONS': {
            'sslmode': 'require'
        }
    }
}

POSTGIS_VERSION = tuple(
    map(int, os.environ.get('DJANGO_POSTGIS_VERSION', '2.1.3').split("."))
)

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = os.environ.get("DRIVER_LOCAL_TIME_ZONE", 'Asia/Manila')

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.environ['DJANGO_STATIC_ROOT']

# Media files (uploaded via API)
# https://docs.djangoproject.com/en/1.8/topics/files/

MEDIA_ROOT = os.environ['DJANGO_MEDIA_ROOT']
MEDIA_URL = '/media/'

# use cookie-based sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'ashlar': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'driver_auth': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'data': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'user_filters': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'oic': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'djangooidc': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# user and group settings
DEFAULT_ADMIN_EMAIL = os.environ.get("DRIVER_ADMIN_EMAIL", 'systems+driver@azavea.com')
DEFAULT_ADMIN_USERNAME = os.environ.get("DRIVER_ADMIN_USERNAME", 'admin')
DEFAULT_ADMIN_PASSWORD = os.environ.get("DRIVER_ADMIN_PASSWORD", 'admin')
# the client keeps these group names in the editor's config.js
DRIVER_GROUPS = {'READ_ONLY': 'public', 'READ_WRITE': 'analyst', 'ADMIN': 'admin'}

# Django Rest Framework
# http://www.django-rest-framework.org/

# TODO: Switch to CORS_ORIGIN_REGEX_WHITELIST when we have a domain in place
CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}

# django-redis cache configuration
# https://niwinz.github.io/django-redis/latest/
# https://docs.djangoproject.com/en/1.8/topics/cache/#cache-arguments

REDIS_HOST = os.environ.get('DRIVER_REDIS_HOST', '127.0.0.1')
REDIS_PORT = os.environ.get('DRIVER_REDIS_PORT', '6379')

CACHES = {
    "default": {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/1',
        'TIMEOUT': None, # never expire
        'KEY_PREFIX': 'DJANGO',
        'VERSION': 1,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5, # seconds
            'SOCKET_TIMEOUT': 5, # seconds
            'MAX_ENTRIES': 900, # defaults to 300
            'CULL_FREQUENCY': 4, # fraction culled when max reached (1 / CULL_FREQ); default: 3
            # 'COMPRESS_MIN_LEN': 0, # set to value > 0 to enable compression
        }
    }
}

ASHLAR = {
    # It is suggested to change this if you know that your data will be limited to
    # a certain part of the world, for example to a UTM Grid projection or a state
    # plane.
    'SRID': 4326,
}

## django-oidc settings
HOST_URL = os.environ.get('DRIVER_APP_HOST', os.environ.get('HOSTNAME'))

# TODO: conditionally set for GLUU in production
GOOGLE_OAUTH_CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID', '')
GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get('OAUTH_CLIENT_SECRET', '')

# Forecast.io settings
FORECAST_IO_API_KEY = os.environ.get('FORECAST_IO_API_KEY', '')

AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

if GOOGLE_OAUTH_CLIENT_ID:
    AUTHENTICATION_BACKENDS += ('djangooidc.backends.OpenIdConnectBackend',)

LOGIN_URL = 'openid'

OIDC_ALLOW_DYNAMIC_OP = False
OIDC_CREATE_UNKNOWN_USER = True
OIDC_VERIFY_SSL = True

# Information used when registering the client, this may be the same for all OPs
# Ignored if auto registration is not used.
OIDC_DYNAMIC_CLIENT_REGISTRATION_DATA = {
    "application_type": "web",
    "contacts": ["info@azavea.com", "kkillebrew@azavea.com"],
    "redirect_uris": [HOST_URL + "/openid/callback/login/", ],
    "post_logout_redirect_uris": [HOST_URL + "/openid/callback/logout/", ]
}

# Default is using the 'code' workflow, which requires direct connectivity from your website to the OP.
OIDC_DEFAULT_BEHAVIOUR = {
    "response_type": "code",
    "scope": ["openid", "email"],
}

OIDC_PROVIDERS = { }

if len(GOOGLE_OAUTH_CLIENT_ID) > 0:
    # see: https://developers.google.com/identity/protocols/OpenIDConnect?hl=en
    # example config towards bottom of page
    OIDC_PROVIDERS['google.com'] = {
        "provider_info": {
            "issuer": "https://accounts.google.com",
            "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_endpoint": "https://www.googleapis.com/oauth2/v4/token",
            "userinfo_endpoint": "https://www.googleapis.com/oauth2/v3/userinfo",
            "revocation_endpoint": "https://accounts.google.com/o/oauth2/revoke",
            "jwks_uri": "https://www.googleapis.com/oauth2/v3/certs",
            "response_types_supported": [
                "code",
                "token",
                "id_token",
                "code token",
                "code id_token",
                "token id_token",
                "code token id_token",
                "none"
            ], "subject_types_supported": [
                "public"
            ], "id_token_signing_alg_values_supported": [
                "RS256"
            ], "scopes_supported": [
                "openid",
                "email",
                "profile"
            ], "token_endpoint_auth_methods_supported": [
                "client_secret_post",
                "client_secret_basic"
            ], "claims_supported": [
                "aud",
                "email",
                "email_verified",
                "exp",
                "family_name",
                "given_name",
                "iat",
                "iss",
                "locale",
                "name",
                "picture",
                "sub"
            ]
        },
        "behaviour": OIDC_DEFAULT_BEHAVIOUR,
        "client_registration": {
            "client_id": GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uris": [HOST_URL + "/openid/callback/login/"],
            "post_logout_redirect_uris": [HOST_URL + "/openid/callback/logout/"],
        }
    }

## Tweak settings depending on deployment target
if DEVELOP:
    # Disable session auth on production, this is for the browseable API only.
    # NB: session auth must appear before token auth for both to work.
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
