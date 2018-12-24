# QuickConf
## Simple universal configuration tools for python projects
especially useful for Heroku users


#### usage example:
### Django:
Simply clone this folder in the same directory with settings.py
put .env file in the same folder with settings.py or manage.py,
QuickConf will find it automatically and export those variables to environment, if there is no .env file
django-vars will skip it and try to load vars directly from environment
```
import quickconf
...
SECRET_KEY = quickconf.django.djangovars['SECRET_KEY']
...
DATABASES = {'default': quickconf.django.djangovars['DATABASE_DATA']}
```
