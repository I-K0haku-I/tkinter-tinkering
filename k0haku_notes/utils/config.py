import os
import configparser

# enable for creating executable
# CONFIG_PATH = os.path.expanduser('~/notes-config.ini')
# honeslty, we don't even need this if we keep the executable in a folder and the config right next to it
CONFIG_PATH = 'config.ini'


def create_default(conf):
    conf['API'] = {
        'url': 'http://127.0.0.1:8000/b/api/',
        'pass': 'yourpasswordhere'
    }
    with open(CONFIG_PATH, 'w') as f:
        conf.write(f)
    print('Created default config.ini')


def init_config():
    conf = configparser.ConfigParser()
    result = conf.read(CONFIG_PATH)
    if not result:
        create_default(conf)
    return conf


config = init_config()
