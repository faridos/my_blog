from .settings import *

ALLOWED_HOSTS = ['app', 'farid-blog.le-5ra.de']
DEBUG = True
PRODUCTION = True
SECRET_KEY = os.environ.get('SECRET_KEY')
CSRF_TRUSTED_ORIGINS = ['http://localhost']  # on prod:the app runs behind nginx proxy,so localhost should be in Trusted
MONITORING_SERVICE_URL = 'http://monitoring_service:5000/' # in case changed in production
