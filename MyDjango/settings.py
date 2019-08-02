"""
Django settings for MyDjango project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8at8(*vw3v$&rggqxlg+s%p#-jfhr!t$i5%n943ibp5!paa_p&'

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
]

MIDDLEWARE = [
    # SecurityMiddleware： 内置的安全机制，保护用户与网站的通信安全
    'django.middleware.security.SecurityMiddleware',
    # SessionMiddleware： 会话Session功能
    'django.contrib.sessions.middleware.SessionMiddleware',
    # LocaleMiddleware： 使用中文
    'django.middleware.locale.LocaleMiddleware',
    # CommonMiddleware： 处理请求信息，规范化请求内容
    'django.middleware.common.CommonMiddleware',
    # CsrfViewMiddleware： 开启CSRF防护功能
    'django.middleware.csrf.CsrfViewMiddleware',
    # AuthenticationMiddleware： 开启内置的用户认证系统
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # MessageMiddleware 开启内置的信息提示功能
    'django.contrib.messages.middleware.MessageMiddleware',
    # XFrameOptionsMiddleware 防止恶意程序点击劫持
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MyDjango.urls'

TEMPLATES = [
    {
        # 定义模板引擎，用于识别模板里面的变量和指令
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 设置模板所在路径
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'index/templates')],
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

WSGI_APPLICATION = 'MyDjango.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    # 第一个数据库
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_db',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'POST': '3306'
    },
    # 第二个数据库
    'MyDjango': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'MyDjango_db',
        'USER': 'root',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'POST': '3306'
    },
    # 第三个数据库
    'my_sqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# 设置根目录的静态资源文件夹public_static
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'public_static'),
# 设置APP(index) 的静态资源文件夹index_static
os.path.join(BASE_DIR, 'index/index_static')]