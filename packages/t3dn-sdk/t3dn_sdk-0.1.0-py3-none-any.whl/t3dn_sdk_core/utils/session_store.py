from json import dumps, loads
from os.path import expanduser, isfile, join
from os import remove
from . import config


def _get_credential_path():
    return join(
        expanduser('~'),
        '.' + config.get_storage_namespace() + '_credentials.json',
    )


def _write_credentials(data):
    path = _get_credential_path()
    with open(path, 'w') as file:
        file.write(dumps(data))


def _read_credentials():
    path = _get_credential_path()
    if isfile(path):
        with open(path, 'r') as file:
            return loads(file.read())
    else:
        return None


def _clear_credentials():
    path = _get_credential_path()
    if isfile(path):
        remove(path)


class SessionStore(object):

    @staticmethod
    def clear():
        _clear_credentials()

    @staticmethod
    def exists():
        return _read_credentials() is not None

    @staticmethod
    def get():
        return _read_credentials()

    @staticmethod
    def set(credentials):
        _write_credentials(credentials)

    @staticmethod
    def update(credentials_update):
        credentials_update = {
            k: v for k, v in credentials_update.items() if v is not None
        }

        current_credentials = SessionStore.get()
        if current_credentials is None:
            current_credentials = {}

        new_credentials = {}
        new_credentials.update(current_credentials)
        new_credentials.update(credentials_update)
        SessionStore.set(new_credentials)
