from functools import wraps
from datetime import datetime, timedelta

from flask import request

from app.ext.rest import Rest, HttpStatus
from app.config.local_settings import TOKEN_TYPE, STDR_UTC_HOUR, HEADER_API_KEY
from .models.Sessions import Sessions
from .sessions import HandleSession

class Auth(HandleSession):
    BEARER_TOKEN_LENGTH = 37
    ACCESS_TOKEN_LENGTH = 30

    @classmethod
    def validate_request(self, *expected_args):
        def validating(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                missing = []
                try:
                    json_data = request.get_json(force=True)
                    if json_data is None: return Rest.response(400, 'missing fields')
                    for field in expected_args:
                        if field not in json_data or json_data.get(field) is None or not json_data.get(field):
                            missing.append(field)
                    if len(missing) > 0:
                        return Rest.response(400, 'missing fields: '+str(missing))
                except Exception as e:
                    return Rest.response(400, 'UNEXPECTED ERROR', errors=str(e))
                return func(*args, **kwargs)
            return wrapper
        return validating

    @classmethod
    def require_auth_session(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            error_code, header_api_key = self.get_header_api_key()

            if error_code is not None:
                return Rest.response(401, HttpStatus.UNAUTHORIZED, errors=header_api_key, status_code=error_code)

            error_code, header_userid = self.get_header_userid()
            if error_code is not None:
                return Rest.response(401, HttpStatus.UNAUTHORIZED, errors=header_userid, status_code=error_code)
            
            error_code, api_access_token = self.get_access_token(header_api_key)

            if error_code is not None:
                return Rest.response(401, HttpStatus.UNAUTHORIZED, errors=api_access_token, status_code=error_code)

            error_code, message_code = self.validate_session(api_access_token, header_userid)           
            if error_code is not None:
                return Rest.response(401, HttpStatus.UNAUTHORIZED, errors=message_code, status_code=error_code)

            return func(*args, **kwargs)
        return wrapper

    @classmethod
    def get_header_api_key(self):
        try:
            header_api_key = request.headers.get(HEADER_API_KEY)
            if header_api_key is None or not header_api_key:
                return 709, 'Access_Denied. Invalid Headers'
            return None, header_api_key
        except Exception as e:
            print('Auth get_header_api_key Exception:', e)

    @classmethod
    def get_header_userid(self):
        try:
            header_userid = request.headers.get('UserId')
            if header_userid is None or not header_userid:
                return 709, 'Access denied. Invalid Headers'
            return None, header_userid
        except Exception as e:
            print('Auth get_header_userid Exception:', e)

    @classmethod
    def get_access_token(self, apikey):
        if apikey is None or not apikey: 
            return 709, 'Access_Denied. Invalid Headers'
        elif len(apikey) == self.BEARER_TOKEN_LENGTH:
            token_type = apikey[:6]

            if TOKEN_TYPE == token_type:
                key_token = apikey[-30:]

                if len(key_token) == self.ACCESS_TOKEN_LENGTH:
                    return None, key_token
                else:
                    return 711, 'The length of the Api key is not valid'
            else:
                return 710, 'Access Denied. The Token type is not valid'
        else:
            return 711, 'The length of the Api Key is not valid'

        return 712, 'Unexpected Error'

    @classmethod
    def validate_session(self, data, user_id):
        q = Sessions.get_by('token', data)

        print('=====================================')

        if q[0]['user_id'] != user_id: return 725, 'User id not match'

        if q[0]['status'] is False: return 725, 'Status is False'

        if q is not None:
            user_session = {
                'access_token': q[0]['token'],
                'token_type': TOKEN_TYPE,
            }

            return None, user_session

        return 725, 'Error gettings user_session'

    @classmethod
    def get_current_time(self):
        now = datetime.utcnow() - timedelta(hours=STDR_UTC_HOUR)
        current_time = now.strftime('%Y-%m-%d %H:%M:%S')
        current_time = datetime.strptime(current_time, '%Y-%m-%d %H:%M:%S')
        return current_time