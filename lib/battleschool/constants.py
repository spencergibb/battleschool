import os


def get_config(env_var, default):
    """ return a configuration variable with casting """
    if env_var is not None:
        value = os.environ.get(env_var, None)
        if value is not None:
            return value
    return default


def get_share_path(*paths):
    lib_path = os.path.dirname(__file__)
    share_path = os.path.join(lib_path, 'share')
    return os.path.join(share_path, *paths)


DEFAULT_MODULE_PATH = get_config('BATTLESCHOOL_LIBRARY', get_share_path('library'))
DEFAULT_HOST_LIST = os.path.expanduser(get_config('BATTLESCHOOL_HOSTS', get_share_path('defaults', 'hosts')))
DEFAULT_PLAYBOOK = os.path.expanduser(get_config('BATTLESCHOOL_PLAYBOOK', get_share_path('defaults', 'battleschool.yml')))
DEFAULT_CALLBACK_PLUGIN_PATH = os.path.expanduser(get_config('BATTLESCHOOL_CALLBACK_PLUGINS', get_share_path('callback_plugins')))
DEFAULT_SUDO_FLAGS = get_config('BATTLESCHOOL_SUDO_FLAGS', '-E')

