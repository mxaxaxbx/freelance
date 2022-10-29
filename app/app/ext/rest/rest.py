from app import api
from .cors import CORS_HEADERS

from flask import make_response, jsonify, Response

class Rest:
    @staticmethod
    @api.representation('aplication/json')
    def response(status_http=200, message='success', data=None, status_code=None, errors=None):
        data = None if data is None else data
        json_res = {'status': status_code or status_http, 'message': message, 'data': data}

        if errors is not None:
            json_res.update({'error': errors})

        res = make_response(jsonify(json_res), status_http)
        res.headers.extend(CORS_HEADERS or {})
        return res

    @staticmethod
    @api.representation('aplication/json')
    def response_custom(status_http=200, data=None):
        json_res = {'message': 'success'} if data is None else data
        res = make_response(jsonify(json_res), status_http)
        res.headers.extend(CORS_HEADERS or {})
        return res

    @staticmethod
    def response_xml(status_http=200, data=None):
        xml_res = data if data is not None else '<root></root>'
        res = make_response(xml_res, status_http)
        res.headers.extend(CORS_HEADERS or {})
        res.headers.extend({'Content-Type':'application/xml'} or {})
        return res

    @staticmethod
    def response_csv(status_http=200, data=None, filename='exportCSV'):
        csv_res = data if data is not None else 'some;example\nplease;input data'
        res = make_response(csv_res, status_http)
        res.headers.extend(CORS_HEADERS or {})
        res.headers.extend({'Content-Type':'application/csv'} or {})
        res.headers.extend({'Content-Disposition':'attachment; filename{0}.csv'.format(filename)} or {})
        return res

    @staticmethod
    def raw_response(status_http=200, data=None):
        res = Response(data, mimetype='text/html')
        return res