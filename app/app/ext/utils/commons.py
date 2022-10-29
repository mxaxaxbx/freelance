# -*- coding: utf-8 -*-

import re
import unicodedata
import json
import string
from datetime import datetime, timedelta, date, time
from app.config.storage import ALLOWED_EXTENSIONS


class customEncoder(json.JSONEncoder):
    def default(self, obj): # pylint: disable=E0202
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, time):
            return obj.isoformat()
        elif isinstance(obj, timedelta):
            return (datetime.min + obj).time().isoformat()
        else:
            return super(customEncoder, self).default(obj)

        return json.JSONEncoder.default(self, obj)


class Commons:
    @staticmethod
    def validate(data, fields):
        if fields is None:
            return None

        obj = []
        try:
            for field in fields:
                if field not in data or data.get(field) is None:
                    obj.append(field)
                else:
                    pass
            return obj if len(obj) > 0 else None
        except Exception as e:
            print("validate Exception:", e)
            return None

    @staticmethod
    def validate_email(email):
        if email is None:
            return None

        try:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

            if match is None:
                return False
            else:
                return True
        except Exception as e:
            print("validate_email Exception:", e)
            return False

    @staticmethod
    def create_name_from_email(email):
        if email is None:
            return None

        try:
            return re.sub(r'_+|-+|\.+|\++', ' ', email.split('@')[0]).title()
        except Exception as e:
            print("create_name_from_email Exception:", e)
            return None

    @staticmethod
    def is_iterable(value):
        if value is None:
            return None

        return isinstance(value, (tuple, list))

    @classmethod
    def remove_accents(self, unicode_str):
        if unicode_str is None:
            return None

        try:
            return ''.join((char_at for char_at in unicodedata.normalize('NFD', str(unicode_str)) if unicodedata.category(char_at) != 'Mn'))
        except Exception as e:
            print("remove_accents Exception:", e)
            return None

    @classmethod
    def sanity_check(self, dirty_str, upper=False):
        if dirty_str is None:
            return None

        try:
            u_str = dirty_str.encode("utf-8")
        except Exception as e:
            print("sanity_check Exception:", e)
            u_str = dirty_str
            
        normalize_str = self.remove_accents(u_str)
        clean_str = normalize_str.replace(" ", "_")

        if upper is True:
            return clean_str.upper()

        return clean_str

    @staticmethod
    def to_json(obj=None, sort=False, encoding_type='ISO-8859-1'):
        if obj is None:
            return None

        try:
            str_result = json.dumps(obj, encoding=encoding_type, indent=4, sort_keys=sort, cls=customEncoder)
            result = json.loads(str_result)
            return result
        except Exception as e:
            print("to_json Exception:", e)
            return None

    @staticmethod
    def get_file_size(file_size, format='B'):
        if file_size is None:
            return None

        if format == 'B':
            total_bytes = round(float(float(file_size)), 2)
            return total_bytes
        if format == 'Kb':
            kbs = round(float(float(file_size) / 1024), 2)
            return kbs
        elif format == 'Mb':
            megas = round(float(float(file_size) / 1024) / 1024, 2)
            return megas
        else:
            return None

    @staticmethod
    def allowed_files(filename=None):
        if filename is not None:
            if '.' in filename:
                ext = filename.rsplit('.', 1)[1].lower()
                if ext in ALLOWED_EXTENSIONS:
                    return True, ext
        return False, None

    @staticmethod
    def clean_string(ugly_cad=None):
        if ugly_cad is None:
            return None

        try:
            ugly_cad = ugly_cad.encode("utf-8")
        except Exception as e:
            print("clean_string Exception:", e)
            return None

        special_list = [{"b": "á", "g": "a"}, {"b": "é", "g": "e"}, {"b": "í", "g": "i"}, {"b": "ó", "g": "o"},
                        {"b": "ú", "g": "u"}, {"b": "Á", "g": "A"}, {"b": "É", "g": "E"}, {"b": "Í", "g": "I"},
                        {"b": "Ó", "g": "O"}, {"b": "Ú", "g": "U"}, {"b": "ñ", "g": "n"}, {"b": "Ñ", "g": "N"},
                        {"b": "\xe1", "g": "a"}, {"b": "\xe9", "g": "e"}, {"b": "\xed", "g": "i"},
                        {"b": "\xf3", "g": "o"}, {"b": "\xfa", "g": "u"}, {"b": "\xc1", "g": "A"},
                        {"b": "\xc9", "g": "E"}, {"b": "\xcd", "g": "I"}, {"b": "\xd3", "g": "O"},
                        {"b": "\xda", "g": "U"}]

        for item in special_list:
            result = ugly_cad.replace(item['b'], item['g'])
            ugly_cad = result

        return ugly_cad.decode("utf-8", "ignore")

    @staticmethod
    def clean_string_str(string_text=None):
        if string_text is None:
            return None

        special_list = [{"b": "á", "g": "a"}, {"b": "é", "g": "e"}, {"b": "í", "g": "i"}, {"b": "ó", "g": "o"},
                        {"b": "ú", "g": "u"}, {"b": "Á", "g": "A"}, {"b": "É", "g": "E"}, {"b": "Í", "g": "I"},
                        {"b": "Ó", "g": "O"}, {"b": "Ú", "g": "U"}, {"b": "ñ", "g": "n"}, {"b": "Ñ", "g": "N"},
                        {"b": "\xe1", "g": "a"}, {"b": "\xe9", "g": "e"}, {"b": "\xed", "g": "i"},
                        {"b": "\xf3", "g": "o"}, {"b": "\xfa", "g": "u"}, {"b": "\xc1", "g": "A"},
                        {"b": "\xc9", "g": "E"}, {"b": "\xcd", "g": "I"}, {"b": "\xd3", "g": "O"},
                        {"b": "\xda", "g": "U"}]

        ugly_cad = None 
        for item in special_list:
            try:  
                if ugly_cad is not None:
                    new_str = ugly_cad.replace(ugly_cad, item['b'], item['g'])
                else:
                    new_str = ugly_cad.replace(string_text, item['b'], item['g'])
            except Exception as e:
                print('Commons error clean_string_str: ', e)
                return string_text

            ugly_cad = new_str  

        return ugly_cad.decode("utf-8", "ignore")       