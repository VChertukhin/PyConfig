# django-vars
## Used to load variables to settings.py from environment or .env file
especially useful for Heroku users


### usage example:
put this file in the same folder with settings.py
put .env file in the same folder with settings.py or manage.py,
django-vars will find it automatically and export those variables to environment, if there is no .env file
django-vars will skip it and try to load vars directly from environment
```
from .django_vars import django_vars
...
SECRET_KEY = django_vars()['SECRET_KEY']
...
DATABASES = {'default': django_vars()['DATABASE_DATA']}
```
