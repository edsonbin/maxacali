"""
Django settings for Mayan EDMS project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

_file_path = os.path.abspath(os.path.dirname(__file__)).split('/')

BASE_DIR = '/'.join(_file_path[0:-2])

MEDIA_ROOT = os.path.join(BASE_DIR, 'mayan', 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'om^a(i8^6&h+umbd2%pt91cj!qu_@oztw117rgxmn(n2lp^*c!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    #Django
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    # 3rd party
    'djcelery',
    'compressor',
    'corsheaders',
    'filetransfers',
    'kombu.transport.django',
    'mptt',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'solo',
    'south',
    'taggit',
    # Base generic
    'acls',
    'common',
    'converter',
    'django_gpg',
    'dynamic_search',
    'lock_manager',
    'mimetype',
    'navigation',
    'pagination',
    'permissions',
    'project_setup',
    'project_tools',
    'smart_settings',
    'user_management',
    # Mayan EDMS
    'app_registry',
    'bootstrap',
    'checkouts',
    'document_acls',
    'document_comments',
    'document_indexing',
    'document_signatures',
    'documents',
    'folders',
    'history',
    'installation',
    'linking',
    'mailer',
    'main',
    'metadata',
    'ocr',
    'registration',
    'rest_api',
    'sources',
    'statistics',
    'storage',
    'tags',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'common.middleware.strip_spaces_widdleware.SpacelessMiddleware',
    'common.middleware.login_required_middleware.LoginRequiredMiddleware',
    'permissions.middleware.permission_denied_middleware.PermissionDeniedMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'mayan.urls'

WSGI_APPLICATION = 'mayan.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(MEDIA_ROOT, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Custom settings section

PROJECT_TITLE = 'Mayan EDMS'
PROJECT_NAME = 'mayan'

ugettext = lambda s: s

LANGUAGES = (
    ('ar', ugettext('Arabic')),
    ('bg', ugettext('Bulgarian')),
    ('bs', ugettext('Bosnian (Bosnia and Herzegovina)')),
    ('da', ugettext('Danish')),
    ('de', ugettext('German (Germany)')),
    ('en', ugettext('English')),
    ('es', ugettext('Spanish')),
    ('fa', ugettext('Persian')),
    ('fr', ugettext('French')),
    ('hu', ugettext('Hungarian')),
    ('hr', ugettext('Croatian')),
    ('id', ugettext('Indonesian')),
    ('it', ugettext('Italian')),
    ('nl', ugettext('Dutch (Nethherlands)')),
    ('pl', ugettext('Polish')),
    ('pt', ugettext('Portuguese')),
    ('pt-br', ugettext('Portuguese (Brazil)')),
    ('ro', ugettext('Romanian (Romania)')),
    ('ru', ugettext('Russian')),
    ('sl', ugettext('Slovenian')),
    ('tr', ugettext('Turkish')),
    ('vi', ugettext('Vietnamese (Viet Nam)')),
    ('zh-cn', ugettext('Chinese (China)')),
)

SITE_ID = 1

STATIC_URL = '/static/'

# Custom settings section

sys.path.append(os.path.join(BASE_DIR, 'mayan', 'apps'))

STATIC_ROOT = os.path.join(BASE_DIR, 'mayan', 'media', 'static')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# --------- Django compressor -------------
COMPRESS_PARSER = 'compressor.parser.HtmlParser'
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']
COMPRESS_ENABLED = False
# ---------- Django sendfile --------------
SENDFILE_BACKEND = 'sendfile.backends.simple'
# --------- Web theme ---------------
WEB_THEME_ENABLE_SCROLL_JS = False
# --------- Django -------------------
LOGIN_URL = 'common:login_view'
LOGIN_REDIRECT_URL = 'main:home'
# -------- LoginRequiredMiddleware ----------
LOGIN_EXEMPT_URLS = (
    r'^favicon\.ico$',
    r'^about\.html$',
    r'^legal/',  # allow the entire /legal/* subsection
    r'^%s-static/' % PROJECT_NAME,

    r'^accounts/register/$',
    r'^accounts/register/complete/$',
    r'^accounts/register/closed/$',

    r'^accounts/activate/complete/',
    r'^accounts/activate/(?P<activation_key>\w+)/$',

    r'^password/reset/$',
    r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
    r'^password/reset/complete/$',
    r'^password/reset/done/$',

    r'^api/',
)
# --------- Pagination ----------------
PAGINATION_INVALID_PAGE_RAISES_404 = True
# ---------- Search ------------------
SEARCH_SHOW_OBJECT_TYPE = False

SERIALIZATION_MODULES = {
    'better_yaml': 'common.serializers.better_yaml',
}
# --------- Taggit ------------
SOUTH_MIGRATION_MODULES = {
    'taggit': 'taggit.south_migrations',
}
# ---------- Django REST framework -----------
REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 100,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}
# ----------- Celery ----------
BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True
#------------ CORS ------------
CORS_ORIGIN_ALLOW_ALL = True
