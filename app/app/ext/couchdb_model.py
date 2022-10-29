from cloudant.client import Cloudant
from cloudant.error import CloudantException

from app.ext.utils import Commons
from app.config.local_settings import CLOUDANT_CREDENTIALS

from datetime import datetime, time

import hashlib
import json
# import pandas as pd
import sys
import cloudant

try:
    client = Cloudant(CLOUDANT_CREDENTIALS['username'], CLOUDANT_CREDENTIALS['password'], url=CLOUDANT_CREDENTIALS['url'])
    client.connect()
except CloudantException as e:
    print('Cloudant Client Exception: ',e)
    raise e
except Exception as e:
    print('Error trying connect to cloudant database: ',e)
    raise e

class CouchdbModel:
    @classmethod
    def get_all(self):
        try:
            db_name = self.__tablename__
            db = client[db_name]
            return db.all_docs()
        except CloudantException as e:
            print('An error Ocurred Trying create the doc ID: {0} '.format(str(data._id)), e)
            return  {'error':'error','reason':e}
        except Exception as e:
            print('Cloudant Model get_all Exception: ',e)
            return {'error':'error','reason':e}

    @classmethod
    def get_by_id(self, key=None):
        if key is None: return {'error':'error','reason':'Enter a key'}
        try:
            db_name = self.__tablename__
            db = client[db_name]

            if key in db:
                doc = db[key]
                return self.dict_to_obj(doc)
            else:
                return {'error':'error','reason':'Document not exist'}
        except CloudantException as e:
            print('An error Ocurred Trying create the doc ID: {0} '.format(str(data._id)), e)
            return  {'error':'error','reason':e}
        except Exception as e:
            print('An error Ocurred: ', e)
            return  {'error':'error','reason':e}

    @classmethod
    def get_by(self, _name, _value):
        if _name is None: return {'error':'error','reason':'Enter a name'}
        try:
            db_name = self.__tablename__
            db = client[db_name]
            query = cloudant.query.Query(db, selector={str(_name): str(_value)})
            return query()['docs']
        except CloudantException as e:
            print('An error Ocurred Trying create the doc ID: {0} '.format(str(data._id)), e)
            return  {'error':'error','reason':e}
        except Exception as e:
            print('An error Ocurred: ', e)
            return  {'error':'error','reason':e}

    @classmethod
    def save(self, data=None):
        if data is None: return {'error':'error','reason':'Enter data'}
        db_name = self.__tablename__
        db = client[db_name]
        now = datetime.now().timestamp()
        _id = str(now)
        _id = hashlib.md5(_id.encode())
        data._id = _id.hexdigest()
        data.created_at = now
        data.updated_at = now
        try:
            doc = db.create_document(data.__dict__)
            if doc.exists():
                return {'OK':True, 'id':data._id}
            else:
                return {'error':'error','reason':'Error Creating Doc ID: {0}'.format(str(data._id))}
        except CloudantException as e:
            print('An error Ocurred Trying create the doc ID: {0} '.format(str(data._id)), e)
            return  {'error':'error','reason':e}
        except Exception as e:
            print('An error Ocurred: ', e)
            return  {'error':'error','reason':e}

    # @classmethod
    # def update(self, data=None):
    #     if data is None: return {'error':'error','reason':'Enter data'}

    #     try:
    #         db_name = self.__tablename__
    #         db = client[db_name]

    #         now = datetime.now().timestamp()
    #         data.updated_at = now

    #         pd_data = pd.Series(data.__dict__).to_frame()
    #         cols = pd_data.drop(['__doc__','__weakref__','__dict__','__module__'])
    #         pd_json = cols.to_json()
    #         pd_json = json.loads(pd_json)['0']

    #         doc = db[pd_json['_id']]
            
    #         for key in pd_json:
    #             doc[key] = pd_json[key]

    #         res = doc.save()
    #         if res is None:
    #             return {'OK':True, 'id':data._id}
    #         else:
    #             return {'error':'error','reason':'Error Updating Doc ID: {0}'.format(str(data._id))}
    #     except CloudantException as e:
    #         print('An error Ocurred Trying update the doc ID: {0} '.format(str(data._id)), e)
    #         return  {'error':'error','reason':e}
    #     except Exception as e:
    #         print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    #         return  {'error':'error','reason':e}

    @classmethod
    def delete(self, key=None):
        try:
            db_name = self.__tablename__
            db = client[db_name]
            
            if key in db:
                doc = db[key]
                doc.delete()
                return {'OK':True}
            else:
                return {'error':'error','reason':'Document not exist'}
        except CloudantException as e:
            print('An error Ocurred Trying update the doc ID: {0} '.format(str(data._id)), e)
            return  {'error':'error','reason':e}
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            return  {'error':'error','reason':e}

    @classmethod
    def raw_query(self, q=None, nSkip=None, nLimit=None, listFileds=None):
        if q is None: return {'error':'error','reason':'Enter a dict of query'}
        if nSkip is None: return {'error':'error','reason':'Enter a number of skip results'}
        if nLimit is None: return {'error':'error','reason':'Enter a number of limit results'}
        if listFileds is None: return {'error':'error','reason':'Enter a list of fields'}

        try:
            db_name = self.__tablename__
            db = client[db_name]
            query = cloudant.query.Query(db, selector=q)
            return query(skip=nSkip, limit=nLimit, fields=listFileds)['docs']

        except CloudantException as e:
            print('An error Ocurred Trying create the doc ID: {0} '.format(str(data._id)), e)
            return  {'error':'error','reason':e}

        except Exception as e:
            print('An error Ocurred: ', e)
            return  {'error':'error','reason':e}

    @classmethod
    def delete(self, id=None):
        if id is None: return {'error':'error','reason':'Enter a id of document'}

        try:
            db_name = self.__tablename__
            db = client[db_name]

            doc = db[id]
            doc.delete()
            
            return {'OK': True, 'id':id}

        except CloudantException as e:
            print('An error Ocurred Trying create the doc ID: {0} '.format(str(data._id)), e)
            return  {'error':'error','reason':e}

        except Exception as e:
            print('An error Ocurred: ', e)
            return  {'error':'error','reason':e}

    @classmethod
    def dict_to_obj(cls, _dict=None, _name='from_dict'):
        if _dict is None: return  {'error':'error','reason':'Enter dict'}
        try:
            new_obj = type(_name, (object,), _dict)
            return new_obj
        except Exception as e:
            print('Cloudant Model dict_to_obj Exception', e)
            return None

    # @classmethod
    # def to_json(cls, obj=None):
    #     if obj is None: return None
        
    #     try:
    #         if type(obj) == type:
    #             obj = obj.__dict__
    #         obj = dict(obj)
    #         pd_data = pd.Series(obj).to_frame()
    #         pd_json = pd_data.to_json()
    #         return json.loads(pd_json)['0']
    #     except Exception as e:
    #         print('Cloudant Model to_json Exception', e)
    #         return None
    #     return None
        

    # def __del__(self):
        # client.disconnect()
