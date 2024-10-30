from pathlib import Path
import dj_database_url
import environ
import os

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


SECRET_KEY = env('SECRET_KEY')


DEBUG = env.bool('DEBUG', default=False)


ALLOWED_HOSTS = ['milestone-project-4-jp-01c67f637dac.herokuapp.com', 'localhost', '127.0.0.1', '.herokuapp.com']


# Apps
INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',
    'checkout',
    'accounts',
    'cart',  
    'django_countries',
    'phonenumber_field',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'myshop.urls'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'products.views.category_list',
                'myshop.context_processors.categories_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'myshop.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASE_URL')
    )
}
# ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'



# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# Phone number region
PHONENUMBER_DEFAULT_REGION = 'GB'

# Stripe
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY')

# Google Maps API Key
GOOGLE_MAPS_API_KEY = env('GOOGLE_MAPS_API_KEY')

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/checkout/'

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'





