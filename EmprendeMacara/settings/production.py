import dj_database_url

DEBUG = True

ALLOWED_HOSTS = ["https://emprendemacara.herokuapp.com/"]

from decouple import config
DATABASES = {
    'default' : dj_database_url.config(
        default=config('DATABASE_URL')
    )
}