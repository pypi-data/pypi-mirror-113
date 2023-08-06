#!/usr/bin/env python3

import os

from dotenv import load_dotenv


def load_env_var(filepath: str) -> (str, str):
    projectroot = os.path.dirname(os.path.dirname(os.path.realpath(filepath)))

    envloaded = os.environ.get('ENV_LOADED', False)
    if envloaded:
        dotenv_path = os.path.join(PROJECT_ROOT, '.env')
        load_dotenv(dotenv_path)
        envtype = os.environ.get('ENV_TYPE', default='local')
        load_dotenv(dotenv_path + '.' + ENV_TYPE)
    else:
        envtype = os.environ.get('ENV_TYPE', default='local')

    return projectroot, envtype
