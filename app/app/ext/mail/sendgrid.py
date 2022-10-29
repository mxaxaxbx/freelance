# pylint: disable=E1101
import sendgrid
from sendgrid.helpers import mail
from sendgrid.helpers.mail import Personalization, Email, Mail
from app.config.local_settings import SENDGRID_API_KEY

import sys
import json

from_email = 'maarenas586@misena.edu.co'

class SendGridMail():

    @staticmethod
    def sendEmailDinamicTemplate(add_to='', template_id=None, personalizations=None, sub=''):
        if not add_to: return {'error':'error', 'reason': 'add_to is None'}
        if not template_id: return {'error':'error', 'reason': 'template_id is None'}
        if not personalizations: return {'error':'error', 'reason': 'personalizations is None'}
        if not sub: return {'error':'error', 'reason': 'personalizations is None'}
        
        try:
            sg = sendgrid.SendGridAPIClient(SENDGRID_API_KEY)
            
            personalization = Personalization()
            personalization.add_to(Email(add_to))

            mail = Mail()
            mail.from_email = Email(from_email)
            mail.add_personalization(personalization)
            mail.template_id = template_id

            request_body = mail.get()
            request_body['personalizations'][0]['dynamic_template_data'] = personalizations
            response = sg.client.mail.send.post(request_body=request_body)
            return {'OK':True, 'message':'Mail successfully sent'}
        except Exception as e:
            print(sys.exc_info()[-1].tb_lineno)
            return {'error':'error', 'reason':str(e)}