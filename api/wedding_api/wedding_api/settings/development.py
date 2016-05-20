import importlib
globals().update(importlib.import_module('.shared', package=__package__).__dict__)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$%cnuj4v*6bm4zjbkgi)v&hmpr*+c6td4ud(&z+9p1d(&%$oua'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
