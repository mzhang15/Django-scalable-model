# Database sepecific settings.
DATABASES = {
  'default': { },
  'auth_db': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'scalica',
    'USER': 'appserver',
    'PASSWORD': 'foobarzoot',
    'HOST': '127.0.0.1',
    'PORT': '3306',
  },
  'db1': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'scalica',
    'USER': 'appserver',
    'PASSWORD': 'foobarzoot',
    'HOST': '127.0.0.1',
    'PORT': '3307',
  },
  'db2': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'scalica',
    'USER': 'appserver',
    'PASSWORD': 'foobarzoot',
    'HOST': '127.0.0.1',
    'PORT': '3308',
  },
}

# Database routers go here:
DATABASE_ROUTERS = ['micro.routers.UserRouter']
