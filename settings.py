DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('John Doe', 'foo@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
  'default': {
    'ENGINE':'mysql',  
    'NAME':'visodea',         
    'USER':'visodea',         
    'PASSWORD':'YOUR_PASSWORD',
  }
}

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = True

MEDIA_ROOT = '/home/open/sites/visodea/media'

MEDIA_URL = '/media/' 

ADMIN_MEDIA_PREFIX = '/media/admin/'

SECRET_KEY = 'TYPE_LOTS_OF_RANDOM_GARBAGE_HERE'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'accounts.context_processors.login_form', 
    )

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
		'/home/open/sites/visodea/apps/pages/templates',
		'/home/open/sites/visodea/apps/accounts/templates',
		'/home/open/sites/visodea/apps/projects/templates',
		'/home/open/sites/visodea/apps/uploads/templates',
		'/home/open/sites/visodea/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
	'django.contrib.comments',
	'django.contrib.markup',
    'django_extensions',
    'ratings',
    'tagging',
    'accounts',
    'pages',
    'projects',
    'uploads',
    'contact',
)

AUTH_PROFILE_MODULE='accounts.UserProfile'

LOGIN_REDIRECT_URL = '/account/overview/'

MARKITUP_FILTER = ('django.contrib.markup.templatetags.markup.textile', {})
MARKITUP_SET = 'markitup/sets/textile'

DEFAULT_FROM_EMAIL = 'support@example.com'
