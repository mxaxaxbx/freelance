from app.ext.resource_handler import ResourceHandler
from app.ext.rest import Rest, HttpStatus
from app.cloudant_modules.users.models.Users import Users
from app.ext.security import Auth
from app.ext.mail.sendgrid import SendGridMail

from flask import request

class ViewUsers(ResourceHandler):
    def get(self, id=''):
        personalizations = {
            'EMAIL':'mxaxaxbx@gmail.com',
            'PASS':'1234',
            'SUB':'Bienvenido a Open Blog',
        }
        res = SendGridMail.sendEmailDinamicTemplate(add_to='mxaxaxbx@gmail.com', template_id='d-419352a1ae6f4c96a75ce2cd95d8379e', personalizations=personalizations, sub=personalizations['SUB'])
        if 'error' in res:
            return Rest.response(201, HttpStatus.OK, res['reason'])
        else:
            return Rest.response(201, HttpStatus.OK, res['message'])
        return Rest.response(400, HttpStatus.OK, 'sending error!')

    @Auth.validate_request('name')
    def post(self):
        data = request.get_json()
        user = Users()
        user.name = str(data.get('name'))
        res = Users.save(user)
        if 'error' in res: return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, errors=str(res['reason']))
        return Rest.response(200,HttpStatus.OK, {'OK': True,'id':res['id']})

    @Auth.validate_request('name')
    def put(self, id=''):
        if not id: return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, errors='Enter a User ID')

        user = Users.get_by_id(id)
        if type(user) == dict:
            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, errors='Enter a valid user ID')
        data = request.get_json()
        user.name = str(data.get('name'))
        res = Users.update(user)
        if 'error' in res: return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, errors=str(res['reason']))
        return Rest.response(200,HttpStatus.OK, {'OK': True,'id':res['id']})

    def delete(self, id=''):
        if not id: return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, errors='Enter a User ID')
        user = Users.get_by_id(id)
        if type(user) == dict:
            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, errors='Enter a valid user ID')
        res = Users.delete(id)
        if 'error' in res: return Res.response(400, HttpStatus.UNEXPECTED_ERROR, errors=str(res['reason']))
        return Rest.response(200,HttpStatus.OK, 'User deleted!')