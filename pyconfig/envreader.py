import os


class EnvReader:

    def __init__(self, path: str='.env', find_dotenv=False, no_dotenv=False):
        if find_dotenv:
            self.find_path()
        self.path = path
        self.vars = {}  # type: Dict[str, str]
        if no_dotenv:
            self.read()
        else:
            self.read_dotenv()

    def __call__(self, key: str):
        return self.vars[key]

    def read(self, dotenv=True):
        if dotenv:
            self.vars = self.read_dotenv()
        else:
            self.vars = os.environ
        return self.vars

    def read_dotenv(self, var_to_read: str=''):
        # TODO: add "export VAR_NAME=value" syntaxis
        with open(self.path, mode='r') as dotenv:
            for line in dotenv:
                try:
                    # cut \n in the end of line, then split by =
                    (var, val) = line.rstrip('\n').split('=')
                    if var_to_read and (var == var_to_read):
                        return val
                    self.vars.update({var: val})
                except ValueError:
                    # not enough values to unpack
                    # (expected 2, got 1) - url error
                    print('Line: \'%s\' has syntax mistake. '
                          'Skipping it.' % line)
                    continue
            return self.vars
        return

    def find_path(self):
        # TODO: make more intellegent search
        '''looks for .env file in working and upper folders'''
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        upper_dir = os.path.dirname(cur_dir)
        search_dirs = [cur_dir, upper_dir]
        for _dir in search_dirs:
            env_file_path = os.path.join(_dir, '.env')
            if os.path.isfile(env_file_path):
                self.path = env_file_path
        # raise FileNotFoundError('.env file is missing')
