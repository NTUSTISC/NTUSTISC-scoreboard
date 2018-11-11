# Of course, these configs will be different from the real one :)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'scoreboard',
        'USER': 'root',
        'PASSWORD': "S3CR3T_P@55W0RD",
        'HOST': '0.0.0.0',
        'PORT': '5432',
    }
}

SECRET_KEY = '00000000000000000000000000000000000000000000000000'

DEBUG = False