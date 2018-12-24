import os
import sys
import logging

from envreader import EnvReader


class DjangoVars:

    def __init__(self):
        self.envreader = EnvReader(no_dotenv=True)
        '''takes vars from environment and returns them as dicrionary'''
        self.djangovars = {'SECRET_KEY': str(),
                           'DATABASE_URL': str(),
                           'DATABASE_DATA': dict()}
        self.django_db_credits = dict()
        try:
            self.djangovars['SECRET_KEY'] = self.envreader.vars['SECRET_KEY']
            self.djangovars['DATABASE_URL'] = self.envreader.vars['DATABASE_URL']
        except KeyError as err:
            logging.error('Variable is unset, caught exception: ' + str(err))
            # FIXME: process the exception
        finally:
            if 'DATABASE_URL' in self.djangovars.keys:
                self.db_url_parser()

    def db_url_parser(self) -> dict:
        '''splits db url in parts and returns as a dictionary'''
        db_url = self.djangovars['DATABASE_URL']
        try:
            db_url_part, name = db_url.rsplit('/', 1)
            db_url_part, port = db_url_part.rsplit(':', 1)
            db_url_part, host = db_url_part.rsplit('@', 1)
            db_url_part, password = db_url_part.rsplit(':', 1)
            database, user = db_url_part.rsplit('://', 1)
        except ValueError:  # not enough values to unpack
                            # (expected 2, got 1) - url error
            raise Exception('mistake in DATABASE_URL you should check it')
        else:
            # TODO: add bigger variety of DB's
            engine = str()
            if database == 'postgres':
                engine = 'django.db.backends.postgresql_psycopg2'
            if database == 'mysql':
                pass
            self.django_db_credits = {'ENGINE': engine,
                                      'NAME': name,
                                      'USER': user,
                                      'PASSWORD': password,
                                      'HOST': host,
                                      'PORT': port}
            return self.django_db_credits
