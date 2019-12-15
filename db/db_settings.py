# Database sepecific settings.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/etc/mysql/my.cnf',
        },
    },
  'auth_db': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'scalica',
    'USER': 'appserver',
    'PASSWORD': 'foobarzoot',
    'HOST': '172.17.0.2',
    'PORT': '3306',
  },
  'db1': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'scalica',
    'USER': 'appserver',
    'PASSWORD': 'foobarzoot',
    'HOST': '172.17.0.3',
    'PORT': '3306',
  },
  'db2': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'scalica',
    'USER': 'appserver',
    'PASSWORD': 'foobarzoot',
    'HOST': '172.17.0.4',
    'PORT': '3306',
  },
}

# Database routers go here:
DATABASE_ROUTERS = ['micro.routers.UserRouter']
