from .settings import *

ALLOWED_HOSTS = ['app']
DEBUG = True
PRODUCTION = True
SECRET_KEY = os.environ.get('SECRET_KEY')
CSRF_TRUSTED_ORIGINS = ['http://localhost']  # on prod:the app runs behind nginx proxy,so localhost should be in Trusted
