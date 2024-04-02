from pathlib import Path
import dj_database_url

from environ import Env
env = Env()
Env.read_env()

ENVIRONMENT = env('ENVIRONMENT', default='production')
print('Entorno: ',ENVIRONMENT )
print('Deberia ige: ')
print('Base: ',env('DATABASE_URL') )

DATABASE_URL=env('DATABASE_URL')

# Configuraciones base de la aplicación
#SECRET_KEY = env('SECRET_KEY')
if ENVIRONMENT == 'development':
    DEBUG = True
    ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')
else:
    DEBUG = False
    ALLOWED_HOSTS = ['*']



# Configuraciones de la base de datos (se sobreescribirán en producción)

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Configuración de la base de datos
DATABASES = {
        'default': {
        }
    }
    
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

if ENVIRONMENT == 'production':
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
