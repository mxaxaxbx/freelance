from app import app as application
from app.ext.rest import Rest, HttpStatus
from app.config.local_settings import DEFAULT_HOST, DEFAULT_PORT, DEBUG

@application.route('/')
def home():
    return Rest.response(200, HttpStatus.OK, {'home':'welcome to BackendBase, use /api instead'})

@application.errorhandler(404)
def not_found(error):
    return Rest.response(404, 'not found')

@application.errorhandler(413)
def request_entity_too_large(error):
    return Rest.response(413, 'The file is too large')

@application.errorhandler(500)
def internal_error(error):
    print('An error ocurred during a request.')
    return Rest.response(500, None, [])

if __name__ == '__main__':
    print('running python server from main app')
    application.run(host=DEFAULT_HOST, port=DEFAULT_PORT, debug=DEBUG)