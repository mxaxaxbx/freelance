class HttpStatus(object):
    OK = 'success!'
    AUTH_ERROR_MSG = 'The server could not verify that you are not authorized to access the URL requested.'
    UNAUTHORIZED = 'You don\'t have permission to access the request resource.'
    RESOURCE_NOT_EXIST = 'The request resource doesn\t exists.'
    DEFAULT_ERROR_MESSAGE = 'An error ocurred. Please try again!'
    UNEXPECTED_ERROR = 'Unexpected Error.'