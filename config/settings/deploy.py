from .base import *


SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = [
    "*",
]

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE"),
        "NAME": os.environ.get("DB_NAME"),
        "HOST": os.environ.get("RDS_HOST"),
        "PORT": os.environ.get("RDS_PORT"),
        "USER": os.environ.get("RDS_USER"),
        "PASSWORD": os.environ.get("RDS_PASSWORD"),
    }
}