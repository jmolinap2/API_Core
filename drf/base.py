from pathlib import Path
import dj_database_url
from environ import Env

env = Env()
Env.read_env()
ENVIRONMENT = env('ENVIRONMENT', default='production')

# Configuraciones base de la aplicación
SECRET_KEY = env('SECRET_KEY')
if ENVIRONMENT == 'development':
    DEBUG = True
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
else:
    DEBUG = False
    ALLOWED_HOSTS = ['*']

# Configuración de la base de datos
if ENVIRONMENT == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_PASSWORD'),
            'PORT': env('DATABASE_PORT'),
        }
    }
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']
    print('Entorno:', ENVIRONMENT)
    print('Configuración de la base de datos:', DATABASES['default'])
    print('ALLOWED_HOSTS:', ALLOWED_HOSTS)

if ENVIRONMENT == 'production':
    DATABASES['default'] = dj_database_url.parse(env('DATABASE_URL'))




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
