from app.config.local_settings import ENDPOINT_API, DEBUG, APP_PATH
from app.config.settings import INSTALLED_MODULES
from app import api

from importlib import import_module

def url(name, endpoint, namespace=None):
    _rt = list(map(lambda r: ENDPOINT_API + r, endpoint))

    if DEBUG:
        print('Loading resource at: ', _rt)

    try:
        if namespace is None:
            print('loading without namespace:')
            api.add_resource(name, *_rt)
        else:
            api.add_resource(name, *_rt, endpoint=namespace)
    except Exception as e:
        print('Resource loading Error: ', e)

class Register(object):
    @staticmethod
    def __init__():
        for mod in INSTALLED_MODULES:
            if DEBUG:
                print('Registering module:', mod)

            try:
                import_module('{0}.{1}.urls'.format(APP_PATH, mod))
            except Exception as e:
                print('Registering Error: ', e)