from os import environ


def get_storage_namespace():
    return environ.get('T3DN_STORAGE_NAMESPACE', 't3dn')


def get_api_url():
    return environ.get('T3DN_API_URL', 'https://api.3dn.cloud')
