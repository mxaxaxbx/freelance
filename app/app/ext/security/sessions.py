from app.ext.security.models.Sessions import Sessions

class HandleSession():
    @classmethod
    def get_current_session(self, key):
        if key is None: return 721, 'Missing Key, to complete the action.'

        try:
            session_to_find = Sessions.get_by_id(key)

            if 'error' in session_to_find: return 723, 'The server could not verify that a session exists.'

            _session_status = session_to_find['status']

            if _session_status != 'Active':
                reason = "User is not active, current status: {0}".format(_session_status)
                return 722, reason
            else:
                return None, session_to_find
        except Exception as e:
            print("Auth get_current_session Exception: ",e)
            return 724, "{0}: {1}".format('Unexpected Error: The debugger detected an exception in the application', str(e))
        return 724, 'Unexpected Error: The debugger detected an exception in the application'

    @classmethod
    def check_current_session(self, username, uuid):
        if username is None: return 725, 'Missing Username, to complete the action.'

        if uuid is None: return 726, 'Missing UUID, to complete the action.'

        try:
            res = Sessions.and_([
                ('uuid', '==', uuid), ('email','==',username)
            ], limit=1)

            if res is not None:
                if len(res) > 0:
                    return None, res[0]
                else:
                    return 727, "RESOURCE_NOT_EXIST"
            else:
                return 728, "DEFAULT_ERROR_MESSAGE"
        except Exception as e:
            print("Auth check_current_session Exception: ", e)
            return 729, "{0}: {1}".format('Unexpected Error: The debugger detected an exception in the application', str(e))
        return 728, 'Unexpected Error: The debugger detected an exception in the application'

    @classmethod
    def remove_session(self, key):
        if key is None: return None

        try:
            res = Sessions.delete(key)

            if res is None: return None, res

            return 730, result
        except Exception as e:
            print("Auth remove_session Exception: ", e)
            return 731, "{0}: {1}".format('Unexpected Error: The debugger detected an exception in the application', str(e))
        return 731, 'Unexpected Error: The debugger detected an exception in the application'

    @classmethod
    def create_session(self, key, user_id):
        if key is None: return 732, 'Missing Key, to complete the action.'
        if user_id is None: return 733, 'Missing Information, to complete the action.'

        try:
            session = Sessions()
            session.token = key
            session.type = 'Bearer '
            session.status = True
            session.user_id = user_id
            res = Sessions.save(session)
            
            if 'error' in res: return 734, res['reason']

            return key
        except Exception as e:
            print("Auth create_session Exception: ", e)
            return 734, "{0}: {1}".format('Unexpected Error: The debugger detected an exception in the application', str(e))
        return 734, 'Unexpected Error: The debugger detected an exception in the application'

    @classmethod
    def get_from_session(self, key, value=None, on_fallback=False):
        if key is None: return 735, 'Missing Key, to complete the action.'
        
        try:
            session_to_find = Sessions.get_by_id(key)

            if 'error' in session_to_find: return 735, 'The server could not verify that a session exists.'

            if value is None: return None, session_to_find

            if value in session_to_find: return None, session_to_find[value]

            if on_fallback is True:
                return None, session_to_find
            else:
                return 737, 'The key provied. does not exist in the session object.'

        except Exception as e:
            print("Auth create_session Exception: ", e)
            return 738, "{0}: {1}".format('Unexpected Error: The debugger detected an exception in the application', str(e))
        return 738, 'Unexpected Error: The debugger detected an exception in the application'