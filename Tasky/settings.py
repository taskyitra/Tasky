from urllib.parse import urlparse
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b%0@jbsu89&9x-$^&@0di*674eqiso997qoah4gjx6c@4@bw08'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'psycopg2',
    'registration',
    'social.apps.django_app.default',
    'task',
    'comments',
    'ratings',
    'django_markdown',
    'user_account',
    'haystack',
    'django_nose',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
   '--with-coverage',  # activate coverage report
    '--with-doctest',  # activate doctest: find and run docstests
    '--verbosity=2',   # verbose output
    '--with-xunit',    # enable XUnit plugin
    '--xunit-file=xunittest.xml',  # the XUnit report file
    '--cover-xml',     # produle XML coverage info
    '--cover-xml-file=coverage.xml',  # the coverage info file
    # '--cover-package=task.models'
    # '--cover-package=task.views'
    # '--cover-package=user_account.models'
    # '--cover-package=user_account.views'
    # '--cover-package=comments.models'
    # '--cover-package=comments.views'
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'Tasky.middleware.FrontendLanguageMiddleware',
)

ROOT_URLCONF = 'Tasky.urls'

WSGI_APPLICATION = 'Tasky.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tasky',
        'USER': 'postgres',
        'PASSWORD': '1596192350bbn',
        'HOST': 'localhost',  # Set to empty string for localhost.
        'PORT': '5432',  # Set to empty string for default.
    }
}

# Templates files
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Parse database configuration from $DATABASE_URL
# DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.github.GithubOAuth2',
    'social.backends.vk.VKOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SOCIAL_AUTH_FACEBOOK_KEY = '1457489431225626'
SOCIAL_AUTH_FACEBOOK_SECRET = '8f3e786e0d9e62bf44b0eaa3a98f85c9'
SOCIAL_AUTH_TWITTER_KEY = 'wrOBuHhZxAbei6l4FwKnUnJ9U'
SOCIAL_AUTH_TWITTER_SECRET = '2vkvkePqYtxd9iUzJ6qIftcOcMKTwraMWpObZtLs2HFVMsSzyl'
SOCIAL_AUTH_GITHUB_KEY = 'd3ba3a18726c5adb9156'
SOCIAL_AUTH_GITHUB_SECRET = '828e9be4558e38f4d75cf6e0fbe9ef21d1ef72e0'
SOCIAL_AUTH_VK_OAUTH2_KEY = '5036633'
SOCIAL_AUTH_VK_OAUTH2_SECRET = 'jcrYvcyU2Iap6mgQdvGC'

ACCOUNT_ACTIVATION_DAYS = 2
REGISTRATION_FORM = 'registration.forms.RegistrationFormUniqueEmail'
AUTH_USER_EMAIL_UNIQUE = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tasky.itra@gmail.com'
EMAIL_HOST_PASSWORD = 'Itransition'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/'
LOGIN_URL = 'auth_login'

MARKDOWN_EDITOR_SKIN = 'simple'

es = urlparse(os.environ.get('SEARCHBOX_URL') or 'http://127.0.0.1:9200/')

port = es.port or 80


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': es.scheme + '://' + es.hostname + ':' + str(port),
        'INDEX_NAME': 'documents',
    },
}

if es.username:
    HAYSTACK_CONNECTIONS['default']['KWARGS'] = {"http_auth": es.username + ':' + es.password}

# http://django-haystack.readthedocs.org/en/latest/signal_processors.html
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# increase the default number of results (from 20)
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
