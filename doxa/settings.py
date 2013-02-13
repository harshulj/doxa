# Django settings for doxa project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 3

ADMINS = (
	('Harshul Jain', 'harshulj@gmail.com'),
)

import os
PROJECT_PATH = os.path.abspath(os.path.join( os.path.dirname(os.path.realpath(__file__)), '..'))

MANAGERS = ADMINS

LOGIN_REDIRECT_URL = '/'

# Profile Model profile can be accessed via user.get_profile()
AUTH_PROFILE_MODULE = "userprofile.UserProfile"

# Haystack settings
HAYSTACK_SITECONF = 'doxa.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_PATH,'woosh_index')

# django-registration settings
ACCOUNT_ACTIVATION_DAYS=7
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = ''

# Django invitation settings
ACCOUNT_INVITATION_DAYS = 7
INVITATIONS_PER_USER = 10
INVITE_MODE = True

# Django private beta settings.

PRIVATEBETA_ALWAYS_ALLOW_MODULES = [
		'django.contrib.auth.views',
        'django.contrib.admin.views.decorators',
        'django.contrib.admin.views.main',
        'django.contrib.admin.views.template',
        'django.contrib.admin.sites',
        'django.contrib.admindocs.views',
        'django.views.static',
	]

# easy_thumbnails setting
THUMBNAIL_ALIASES = {
	'': {
		'profile_pic': {'size': (150, 150), 'crop': True},
    },
}
THUMBNAIL_DEBUG = True

# Django debuug toolbar settings
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'HIDE_DJANGO_SQL': False,
    'TAG': 'div',
}

# Social Auth Settings
SOCIAL_AUTH_CREATE_USERS = True  # To disable user creating using social auth
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'django.contrib.auth.backends.ModelBackend',
    )

LOGIN_URL          = '/accounts/login/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/profile/edit/'

# for twitter
TWITTER_CONSUMER_KEY         = 'qcHPSRCbBR6VGtn0jQlBJw'
TWITTER_CONSUMER_SECRET      = 'tPNM5tAr057ozA7MHaGmVGMLF54BfnUbrXw0IA1Lc'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'doxa',                      # Or path to database file if using sqlite3.
        'USER': 'doxa',                      # Not used with sqlite3.
        'PASSWORD': 'doxa',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# settings for 3rd party apps migrations
SOUTH_MIGRATION_MODULES = {
    'tagging': 'migrations_other_apps.tagging',
    'djangoratings': 'migrations_other_apps.djangoratings',
    #'recommends': 'migration_other_apps.recommends',
    #'recommends.storages.djangoorm': 'migration_other_apps.recommends_storages_djangoorm',
    'social-auth': 'migrations_other_apps.social_auth',
}


INTERNAL_IPS = ('127.0.0.1',)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Kolkata'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH,'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH,'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'assets'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bf6j+&amp;e2d1kfn^id)z$g=^nr5i1%un(!v41y+#8s!(e93m2mz8'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"django.core.context_processors.static",
	"django.core.context_processors.tz",
	"django.contrib.messages.context_processors.messages",
	'django.contrib.auth.context_processors.auth',
	'django.core.context_processors.request',
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #'privatebeta.middleware.PrivateBetaMiddleware',
)

ROOT_URLCONF = 'doxa.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'doxa.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH,'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'south',
    'registration',
    'debug_toolbar',
    'invitation',
    'privatebeta',
    'easy_thumbnails',
    'haystack',
    'social_auth',
    'relationships',
    'account',
    'userprofile',
    'polls_and_opinions',
    'tagging',
    'djangoratings',
    'follow',
    'recommends',
    'recommends.storages.djangoorm',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config(default='mysql://doxa:doxa@localhost:3306/doxa')
