import os

from werkzeug.contrib.cache import FileSystemCache

from app.config.local_settings import SESSION_EXPIRE_TIME

def init_werkzeug_cache():
    cache = None
    server_software = os.environ.get('ENV')

    print('SERVER_SOFTWARE: ', os.environ.get('SERVER_SOFTWARE'))
    print('ENV: ', server_software)

    if server_software is None:
        print('Setup cache on filesystem')
        cache = FileSystemCache('/tmp', default_timeout=SESSION_EXPIRE_TIME)
        return cache

    if 'standar' in server_software:
        print('RUNTIME: ', os.environ.get('RUNTIME'))
        print('SERVICE: ', os.environ.get('SERVICE'))
        print('VERSION: ', os.environ.get('VERSION'))
        print('PORT: ', os.environ.get('PORT'))

        print('Setup cache 2nd Gen')
        cache = FileSystemCache('/tmp', default_timeout=SESSION_EXPIRE_TIME)
        return cache

        if server_software.startswith(('development', 'Development', 'testutil', 'gunicorn')):
            print ('setup cache on LOCAL Server')
            cache = FileSystemCache('/tmp', default_timeout=SESSION_EXPIRE_TIME)
            return cache