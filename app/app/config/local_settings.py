import os
SESSION_EXPIRE_TIME = 14400
ALLOW_METHODS = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
ENDPOINT_API = ''
DEBUG = True if os.environ.get('FLASK_ENV') else False
APP_PATH = 'app'
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = os.environ.get('APP_PORT')

SENDGRID_API_KEY = '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'

TOKEN_TYPE = 'Bearer'
STDR_UTC_HOUR = 5
HEADER_API_KEY = 'Authorization'

CLOUDANT_CREDENTIALS = {
    'username': 'b8e8ed8c-af90-41bf-8999-b08d26e03bb2-bluemix',
    'password': 'ab83ccddaf508ca535ca597284c7acf092c34fb69b3376e6fa070868b18fe5cd',
    'url': 'https://b8e8ed8c-af90-41bf-8999-b08d26e03bb2-bluemix.cloudant.com',
}