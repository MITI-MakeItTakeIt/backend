from .base import *


env = environ.Env(
    DEBUG=(bool, False)
)

environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, 'settings', 'deploy.env')
)

ALLOWED_HOSTS = [
    "*",
]

SECRET_KEY = env("DJANGO_SECRET_KEY")

KAKAO_REST_API_KEY = env("KAKAO_REST_API_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": env("DATABASE_HOST"),
        "PORT": "3306",
        "NAME": env("MYSQL_DATABASE"),
        "USER": "root",
        "PASSWORD": env("MYSQL_ROOT_PASSWORD"),
    }
}

STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR.parent, 'staticfiles')