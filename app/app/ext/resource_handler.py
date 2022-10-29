from flask_restful import Resource

from app.ext.rest import Rest, HttpStatus

class ResourceHandler(Resource):
    def patch(self):
        return Rest.response(400, HttpStatus.UNAUTHORIZED)