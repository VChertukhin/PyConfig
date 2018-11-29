import os
import sys
import logging


# TODO: add more comments
def set_env_vars_from_file() -> bool:
    '''
    exports vars from .env to environment if exists
    returns True if file was loaded and vars were exported, othe way False
    '''
    def find_env_file_path():
        '''looks for .env file in working and upper folders'''
        dotenv = '.env'
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        upper_dir = os.path.dirname(cur_dir)
        search_dirs = [cur_dir, upper_dir]
        for _dir in search_dirs:
            env_file_path = os.path.join(_dir, dotenv)
            if os.path.isfile(env_file_path):
                return env_file_path
        raise FileNotFoundError

    try:
        env_file = open(find_env_file_path(), mode='r')
    except FileNotFoundError:
        return False
    else:
        for var in env_file:
            try:
                # cut \n in the end of line, then split by =
                var_name, value = var.rstrip('\n').split('=', 1)
            except ValueError:
                # not enough values to unpack (expected 2, got 1) - url error
                raise Exception('mistake in .env you should check it')
            else:
                os.environ[var_name] = value
                print(os.environ[var_name])
        return True


def read_vars_from_environment() -> dict:
    '''takes vars from environment and returns them as dicrionary'''
    vars = {'SECRET_KEY': str(),
            'DATABASE_URL': str()}
    try:
        vars['SECRET_KEY'] = os.environ['SECRET_KEY']
        vars['DATABASE_URL'] = os.environ['DATABASE_URL']
    except KeyError as err:
        logging.error('Variable is unset, caught exception: ' + str(err))
        # FIXME: process the exception
    finally:
        return vars


def db_url_parser(db_url: str) -> dict:
    '''splits db url in parts and returns as a dictionary'''
    try:
        db_url_part, name = db_url.rsplit('/', 1)
        db_url_part, port = db_url_part.rsplit(':', 1)
        db_url_part, host = db_url_part.rsplit('@', 1)
        db_url_part, password = db_url_part.rsplit(':', 1)
        database, user = db_url_part.rsplit('://', 1)
    except ValueError:  # not enough values to unpack (expected 2, got 1) - url error
        raise Exception('mistake in DATABASE_URL you should check it')
    else:
        # TODO: add bigger variety of DB's
        engine = str()
        if database == 'postgres':
            engine = 'django.db.backends.postgresql_psycopg2'
        if database == 'mysql':
            pass
        db_data = {'ENGINE': engine,
                   'NAME': name,
                   'USER': user,
                   'PASSWORD': password,
                   'HOST': host,
                   'PORT': port}
        return db_data


def django_vars(stopdotenv: bool=False) -> dict:
    ''' '''
    # FIXME: stop calling set_env_vars_from_file if already was called and vars are set
    if not stopdotenv:
        set_env_vars_from_file()
    env_vars = read_vars_from_environment()
    django_vars = {'DATABASE_DATA': dict(),
                   'REDIS': dict(),
                   'SECRET_KEY': str()}
    if not env_vars:
        raise Exception('No needed environment variables found')
    if 'DATABASE_URL' in env_vars.keys():
        db_vars = db_url_parser(env_vars['DATABASE_URL'])
        django_vars['DATABASE_DATA'] = {'ENGINE': db_vars['ENGINE'],
                                        'NAME': db_vars['NAME'],
                                        'USER': db_vars['USER'],
                                        'PASSWORD': db_vars['PASSWORD'],
                                        'HOST': db_vars['HOST'],
                                        'PORT': db_vars['PORT']}
    if 'SECRET_KEY' in env_vars.keys():
        django_vars['SECRET_KEY'] = env_vars['SECRET_KEY']
    if 'REDIS' in env_vars.keys():
        pass  # TODO: add redis case later
    return django_vars


if __name__ == '__main__':
    print(django_vars())
