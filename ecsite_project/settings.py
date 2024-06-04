"""
Django settings for ecsite_project project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5sa#k)_$+51ks968@0xtlm6_67h21p!8+-q1py8bs^==acne-o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'django.contrib.sites',
    'allauth', 
    'allauth.account', 
    'allauth.socialaccount', 
    'allauth.socialaccount.providers.google',   # 今回はgooglを利用するからgoogleを入れてる

    'accounts',
    'stores',
]

AUTH_USER_MODEL = 'accounts.Users'  # 作成したモデルを指定のモデルに指定する
# AUTHは認証っていう意味

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # これも追加しないとマイグレーションできなかった
]

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",   # デフォルトの認証
    "allauth.account.auth_backends.AuthenticationBackend",   # allauthの認証
)

ROOT_URLCONF = 'ecsite_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
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

WSGI_APPLICATION = 'ecsite_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/accounts/user_login'
LOGIN_REDIRECT_URL = '/accounts/home'
LOGOUT_REDIRECT_URL = '/accounts/user_login'  # ログアウトした後にリダイレクトするURLを指定できる

# SESSION_COOKIE_AGE = 5


SITE_ID = 1  # django_siteテーブル上のどのサイトを認証に用いるか（基本は1）
ACCOUNT_EMAIL_REQUIRED = True  # 認証にメアドが必要か(デフォルトはFalse)
ACCOUNT_UNIQUE_EMAIL = True  # 認証にユーザ名が必要か(デフォルトはTrue)
ACCOUNT_USERNAME_REQUIRED = False

# プロバイダーごとの設定を記述する
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [  # Googleでログインした際に取得できる情報。Google APIで何を取得するか
            'profile',  # ユーザ名
            'email'
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',  # offlineでアクセスをする場合はofflineに設定する(offlineとは、ユーザーがいない状態(バッチなど)のこと)(ネットに繋がっていないことではない)
        },
    }
}


from dotenv import load_dotenv

load_dotenv()

        
DJANGO_SOCIAL_GOOGLE_OAUTH2_KEY = os.getenv("DJANGO_SOCIAL_GOOGLE_OAUTH2_KEY"),
DJANGO_SOCIAL_GOOGLE_OAUTH2_SECRET = os.getenv("DJANGO_SOCIAL_GOOGLE_OAUTH2_SECRET")
