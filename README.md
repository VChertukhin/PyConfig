# PyConfig
## Simple universal configuration tool for python projects

especially useful for Heroku users


#### usage example:
### Installation:
Clone the repository into your environment and run:
```
python setup.py install
```
### Django:
Put .env file in the same folder with settings.py or manage.py,
QuickConf will find it automatically and export those variables to environment, if there is no .env file
django-vars will skip it and try to load vars directly from environment
```
import pyconfig
...
SECRET_KEY = pyconfig.django.djangovars['SECRET_KEY']
...
DATABASES = {'default': pyconfig.django.djangovars['DATABASE_DATA']}
```