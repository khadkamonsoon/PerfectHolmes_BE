from .base import *


def read_secret(secret_name):
    file = open("/run/secrets/" + secret_name)
    secret = file.read()
    secret = secret.rstrip().lstrip()
    file.close()
    return secret


DEBUG = False

SECRET_KEY = read_secret("SECRET_KEY")

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "django",
        "USER": "django",
        "PASSWORD": read_secret("MYSQL_PASSWORD"),
        "HOST": "mariadb",
        "PORT": "3306",
    }
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "timestamp": {
            "format": "{asctime} {levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "timestamp"},
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "log.django",
            "formatter": "timestamp",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    },
}

KAKAO_API_KEY = read_secret("KAKAO_API_KEY")
OPEN_AI_KEY = read_secret("OPEN_AI_KEY")
OPEN_AI_PROMPT = read_secret("OPEN_AI_PROMPT")
GPT_MODEL = read_secret("GPT_MODEL")
