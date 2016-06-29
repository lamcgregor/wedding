import os
import importlib

ENVIRONMENT = os.environ.get('DJANGO_ENVIRONMENT', 'development')
globals().update(importlib.import_module('.{}'.format(ENVIRONMENT), package=__name__).__dict__)
