import urllib
import urllib.request
import ssl as ssl_lib
import xml.etree.ElementTree as xmlTree

class StoreCookie(object):
    the_cookie = None

    @classmethod
    def save_cookie(self, new_cookie):
        self.the_cookie = new_cookie

    def get_cookie(self):
        return self.the_cookie

    def remove_cookie(self):
        self.the_cookie = None

cookie_jar = StoreCookie()

def consumer(uri=None, method='GET', data=None, custom_headers=None, session=False, use_ssl=False, options=None):
    if uri is None:
        return None

    _default_header = {'Content-Type':'application/json'}
    _url = uri
    _data = None if data is None else json.dumps(data)
    _method = 'GET' if method is None else method
    _req = None
    _default_timeout = 60

    if options is not None:
        if options  == 'xml':
            _default_header = custom_headers
            _data = None if data is None else str(data)
        else:
            return None
    elif custom_headers is not None:
        _default_header.update(custom_headers)

    if _data is None:
        _req = urllib.request.Request(_url, headers=_default_header)
    else:
        _req = urllib.request.Request(_url, _data_encode(), headers=_default_header)

    if _req is None:
        return None
    else:
        _req.get_method = lambda: _method

        if session is True:
            _cookie = cookie_jar.get_cookie()

            if _cookie is not None:
                _req.add_header('Cookie', _cookie)
        
        try:
            context = None

            if use_ssl is True:
                context = ssl_lib._create_unverified_context()

            response = urllib.request.urlopen(_req, timeout=_default_timeout, context=context)
            status = response.getcode()

            if status == 200 or 201:
                meta = response.info()
                content_type = meta.get('Content-Type')

                if session is True:
                    the_cookie = meta.get('Set-Cookie')

                    if the_cookie:
                        cookie_jar.save_cookie(the_cookie[0])

                if 'application/csv' in content_type:
                    return None
                elif 'application/json' in content_type:
                    read = response.read()

                    try:
                        res = json.loads(read)

                        if 'status' in res:
                            print('the response status: {}'.format(res['status']))

                        if 'message' in res:
                            print('The response message: {}'.format(res['message']))

                        return res
                    except ValueError as e:
                        print('The response is not a valid json')
                        print(e)
                        return None
                elif 'application/xml' in content_type or 'text/xml' in content_type:
                    print('The response is a csv file')
                    read = response.read()

                    try:
                        xml_root = xmlTree.fromstring(read)
                        return xml_root
                    except ValueError as e:
                        print('The response is not a valid xml')
                        print(e)
                        return read
                    except Exception as e:
                        print('A exception an ocurred while read the XML: {0}'.format(str(e)))
                        return read
                else:
                    print('content_type', content_type)
                    print('The response is not a csv file, json or xml response, trying to convert to JSON...')

                    try:
                        res = response.read()
                        return res
                    except ValueError as e:
                        print('An error ocurred while trying  to convert the response to JSON')
                        print(e)
                        return None
            else:
                print('The response status Error: {0}'.format(str(status)))
                return None
        except urllib.error.HTTPError as e:
            print('HttpError: {0} {1}'.format(e.code, e.reason))
            return e.reason
        except Exception as e:
            print('A Exception an ocurred: {0}'.format(str(e)))
            return str(e)
        except IOError as e:
            print('Can\'t connect, reason: {0}'.format(e.reason))
            return e.reason