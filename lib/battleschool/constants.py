import os
import sys


def get_config(env_var, default):
    """ return a configuration variable with casting """
    if env_var is not None:
        value = os.environ.get(env_var, None)
        if value is not None:
            return value
    return default


# Needed so the RPM can call setup.py and have modules land in the
# correct location. See #1277 for discussion
if getattr(sys, "real_prefix", None):
    DIST_MODULE_PATH = os.path.join(sys.prefix, 'share/battleschool/')
else:
    DIST_MODULE_PATH = '/usr/share/battleschool/'

DEFAULT_MODULE_PATH = get_config('BATTLESCHOOL_LIBRARY', os.path.join(DIST_MODULE_PATH, 'library'))
DEFAULT_HOST_LIST = os.path.expanduser(get_config('BATTLESCHOOL_HOSTS', os.path.join(DIST_MODULE_PATH, 'defaults', 'hosts')))
DEFAULT_PLAYBOOK = os.path.expanduser(get_config('BATTLESCHOOL_PLAYBOOK', os.path.join(DIST_MODULE_PATH, 'defaults', 'battleschool.yml')))
DEFAULT_CALLBACK_PLUGIN_PATH = os.path.expanduser(get_config('BATTLESCHOOL_CALLBACK_PLUGINS', os.path.join(DIST_MODULE_PATH, 'callback_plugins')))
DEFAULT_SUDO_FLAGS = get_config('BATTLESCHOOL_SUDO_FLAGS', '-E')

