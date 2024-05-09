import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

ALLOWED_HOSTS = [
	"localhost",
	"api.klswe.com",
		os.environ["BACKEND_IP"],
		os.environ["BACKEND_IPV4_DNS"]
]

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
	},
	{
		"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
	},
	{
		"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
	},
	{
		"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
	},
]

BASE_DIR = Path(__file__).resolve().parent.parent

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
	"http://localhost",
	"https://www.klswe.com",
	"https://klswe.com",
	"https://" + os.environ["FRONTEND_IP"],
]

CORS_TRUSTED_ORIGINS = [
	"http://localhost",
	"https://www.klswe.com",
	"https://klswe.com",
	"https://" + os.environ["FRONTEND_IP"],
]

CSRF_COOKIE_DOMAIN = ".klswe.com"

CSRF_COOKIE_HTTPONLY = False

CSRF_COOKIE_PATH = "/"

CSRF_COOKIE_SAMESITE = "None"

CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = ["https://klswe.com", "https://www.klswe.com"]

# Application definition
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.sqlite3",
		"NAME": BASE_DIR / "db.sqlite3",
	}
}

DEBUG = os.environ["DEBUG"] == "True"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
	"debug_toolbar",
	"corsheaders",
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.messages",
	"django.contrib.sessions",
	"django.contrib.staticfiles",
	"translate.apps.TranslateConfig",
	"store_code.apps.StoreCodeConfig",
]

INTERNAL_IPS = [
	"localhost",
]

LANGUAGE_CODE = "en-us"

MIDDLEWARE = [
	"debug_toolbar.middleware.DebugToolbarMiddleware",
	"corsheaders.middleware.CorsMiddleware",
	"django.middleware.security.SecurityMiddleware",
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"

SECRET_KEY = os.environ["SECRET_KEY"]

SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

SECURE_HSTS_SECONDS = 60

SECURE_SSL_REDIRECT = True 

SESSION_COOKIE_SECURE = True

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = "static/"

TEMPLATES = [{
	"BACKEND": "django.template.backends.django.DjangoTemplates",
	"DIRS": [BASE_DIR / "templates"],
	"APP_DIRS": True,
	"OPTIONS": {
		"context_processors": [
			"django.template.context_processors.debug",
			"django.template.context_processors.request",
			"django.contrib.auth.context_processors.auth",
			"django.contrib.messages.context_processors.messages",
		],
	},
}]

TIME_ZONE = "America/Los_Angeles"

USE_I18N = True

USE_TZ = True

WSGI_APPLICATION = "mysite.wsgi.application"
