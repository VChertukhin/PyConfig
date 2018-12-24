import os

from envreader import EnvReader


class QuickConfig:

    def __init__(self, path: str='.env',
                 find_dotenv: bool=False, dotenv: bool=True):
        self.envreader = EnvReader(path=path, find_dotenv=find_dotenv)
        if dotenv:
            self.vars = self.envreader.read(dotenv=True)
        else:
            self.vars = self.envreader.read(dotenv=False)

    def set_env_vars(self, vars: dict=None, setall: bool=False) -> bool:

        def set_vars(vars: dict):
            for key in vars:
                var_name = key
                value = vars[key]
                os.environ[var_name] = value

        if setall:
            set_vars(self.vars)
        else:
            set_vars(vars)
