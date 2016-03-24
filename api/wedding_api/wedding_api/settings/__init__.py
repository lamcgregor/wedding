import os
import importlib

environment = os.environ.get('DJANGO_ENVIRONMENT', 'development')
globals().update(importlib.import_module('.{}'.format(environment), package=__name__).__dict__)
