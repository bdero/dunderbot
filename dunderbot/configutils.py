import ast
import os

import yaml


CONFIG_PATHS = [
    os.environ.get('DUNDERBOT_CONFIG', ''),
    os.path.join(os.getcwd(), 'dunderbot.yml'),
    os.path.join(os.path.expanduser('~'), 'dunderbot.yml'),
    os.path.join(os.path.expanduser('~'), '.dunderbot'),
    '/etc/dunderbot.yml',
]

def load_fallback():
    """Load optional yaml config"""
    fallback_config = {}
    config_file_path = None
    for config_path in CONFIG_PATHS:
        if os.path.isfile(config_path):
            config_file_path = config_path
            break
    if config_file_path is not None:
        with open(config_file_path) as config_file:
            fallback_config = yaml.safe_load(config_file)
    return fallback_config

FALLBACK_CONFIG = load_fallback()


def get_var(name, default):
    """Return the settings in a precedence way with default"""
    try:
        value = os.environ.get(name, FALLBACK_CONFIG.get(name, default))
        return ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return value
