from app.ext.resource_handler import ResourceHandler
from app.ext.rest import Rest, HttpStatus
from app.config.settings import APP_VERSION

class ViewHome(ResourceHandler):
    def get(self):
        return Rest.response(200, HttpStatus.OK, {'home':'Welcome to BackendBase, version '+ APP_VERSION})

    def post(self):
        return Rest.response(200, HttpStatus.OK, {'home':'Welcome to BackendBase, version '+ APP_VERSION})

    def put(self):
        return Rest.response(200, HttpStatus.OK, {'home':'Welcome to BackendBase, version '+ APP_VERSION})

    def delete(self):
        return Rest.response(200, HttpStatus.OK, {'home':'Welcome to BackendBase, version '+ APP_VERSION})