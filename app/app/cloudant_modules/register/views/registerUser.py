from app.ext.resource_handler import ResourceHandler
from app.ext.rest import Rest, HttpStatus
from app.cloudant_modules.users.models.Users import Users
from app.ext.security import Auth, generate_password
from app.ext.utils import Commons
from app.ext.mail.sendgrid import SendGridMail

from flask import request

class ViewRegisterUser(ResourceHandler):
    def get(self, id=''):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)

    @Auth.validate_request('email','lastname','name','password')
    def post(self):
        data = request.get_json()
        user = Users.get_by('email',data.get('email'))
        if user:
            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, 'The email is registered!')
        isValidEmail = Commons.validate_email(str(data.get('email')))
        if isValidEmail is False:
            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, 'Enter a valid email address!')
        if len(str(data.get('password'))) < 8:
            return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, 'Enter a valid password!')
        password = generate_password(data.get('password'))

        user = Users()
        user.birthdate = str(data.get('birthdate'))
        user.email = str(data.get('email'))
        user.lastname = str(data.get('lastname'))
        user.name = str(data.get('name'))
        user.password = password
        user.role = 'editor'
        res = Users.save(user)
        if 'error' in res: return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, errors=str(res['reason']))

        # sending_email
        template_id = 'd-419352a1ae6f4c96a75ce2cd95d8379e'
        personalizations = {
            'EMAIL':data.get('email'),
            'PASS':data.get('password'),
            'SUB':'Bienvenido a Open Blog',
        }

        res = SendGridMail.sendEmailDinamicTemplate(add_to=data.get('email'), template_id=template_id, personalizations=personalizations, sub=personalizations['SUB'])

        if 'error' in res:
            print(res['reason'])
        else:
            print('{0}: {1}'.format(res['message'], data.get('email')))
        
        return Rest.response(200, HttpStatus.OK, 'You have registered in the platform correctly. Login Now and create your first article.')

    def put(self, id=''):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)

    def delete(self, id=''):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)