from app.ext.resource_handler import ResourceHandler
from app.ext.rest import Rest, HttpStatus
from app.ext.security import Auth, check_password
from app.cloudant_modules.users.models.Users import Users

from flask import request

from random import choice

class ViewloginUser(ResourceHandler):
    def get(self):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)

    @Auth.validate_request('username','password')
    def post(self):
        # return Rest.response(201, HttpStatus.OK, {'data_session':'data_session'})
        data = request.get_json()
        user = Users.get_by('email', data.get('username'))
        if not user:
            return Rest.response(400, HttpStatus.UNAUTHORIZED, 'Username or Password Incorrect')

        if user[0]['role'] != 'editor':
            return Rest.response(400, HttpStatus.UNAUTHORIZED, 'Username or Password Incorrect')

        isValidPassword = check_password(user[0]['password'], data.get('password'))
        if isValidPassword is False:
            return Rest.response(400, HttpStatus.UNAUTHORIZED, 'Username or Password Incorrect')

        key = self.generateRandomString(30)
        new_session = Auth.create_session(key, user[0]['_id'])
        if type(new_session) == tuple:
            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, new_session[1])

        data_session = {
            'token': new_session,
            'user_id': user[0]['_id'],
            'name': user[0]['name'],
            'lastname': user[0]['lastname'],
            'email': user[0]['email'],
            'role': user[0]['role'],
        }
        return Rest.response(201, HttpStatus.OK, data_session)

    def put(self):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)

    def delete(self):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)

    def generateRandomString(self, long=7):
        values = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return ''.join([choice(values) for i in range(long)])