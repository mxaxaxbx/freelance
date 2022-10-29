# -*- coding: utf-8 -*-
import json
from decimal import Decimal

from datetime import datetime, timedelta, date, time

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import update
from sqlalchemy.sql.expression import bindparam

from app import db
from app.ext.utils.commons import Commons


class customEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
        elif isinstance(obj, date):
            return str(obj)
        elif isinstance(obj, time):
            return str(obj)
        elif isinstance(obj, timedelta):
            return str((datetime.min + obj).time())
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return super(customEncoder, self).default(obj)

        return json.JSONEncoder.default(self, obj)


class GenericModel(db.Model):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def save(cls, _data=None):
        try:
            if _data is None:
                db.session.add(cls)
            else:
                db.session.add(_data)

            resp = db.session.commit()
            return resp
        except Exception as e:
            db.session.rollback()
            print("GenericModel save Exception: {0}".format(str(e)))
            return e

    @classmethod
    def multi_save(cls, _data=None):
        if _data is None:
            return None

        if Commons.is_iterable(_data):
            if len(_data) > 0:
                try:
                    result = db.engine.execute(cls.__table__.insert(), _data)
                    db.session.commit()

                    execute_result = [{
                        "lastrowid": result.lastrowid,
                        "rowcount": result.rowcount,
                        "last_inserted_params": result.last_inserted_params(),
                    }]

                    return execute_result
                except Exception as e:
                    db.session.rollback()
                    print("GenericModel multi_save db.engine.execute Exception: {0}".format(e))
                    return str(e)
            else:
                reason = "GenericModel multi_save Exception: At least one object is required, from the list of data."
                print(reason)
                return str(reason)
        else:
            reason = "GenericModel multi_save Exception: _data is not iterable"
            print(reason)
            return str(reason)

    @classmethod
    def update(cls, _data=None):
        try:
            db.session.add(_data)

            resp = db.session.commit()
            return resp
        except Exception as e:
            db.session.rollback()
            print("GenericModel update Exception: {0}".format(str(e)))
            return e

    @classmethod
    def multi_update(cls,  _query_params=None,  _data=None):
        if _query_params is None or _data is None:
            return None

        if Commons.is_iterable(_data):
            if len(_data) > 0:
                try:
                    _stmt = update(cls)
                    for param in _query_params:
                        p = None
                        if len(param) == 2:
                            p1,p2 = param
                            p = {'p1':p1,'p2':'=','p3':bindparam(p2)}
                        if len(param) == 3:
                            p1,p2,p3 = param
                            p = {'p1':p1,'p2':p2,'p3':bindparam(p3)}
                        _stmt = _stmt.where('{p1}{p2}{p3}'.format(**p))

                    result = db.engine.execute(_stmt, _data)
                    db.session.commit()

                    execute_result = [{
                        "lastrowid": result.lastrowid,
                        "rowcount": result.rowcount,
                        "last_updated_params": result.last_updated_params(),
                    }]
                    return execute_result
                except Exception as e:
                    db.session.rollback()
                    print("GenericModel multi_update db.engine.execute Exception: {0}".format(e))
                    return str(e)
            else:
                reason = "GenericModel multi_update Exception: At least one object is required, from the list of data."
                print(reason)
                return str(reason)
        else:
            reason = "GenericModel multi_update Exception: _data is not iterable"
            print(reason)
            return str(reason)

    @classmethod
    def delete(cls, _data=None):
        try:
            db.session.delete(_data)

            resp = db.session.commit()
            return resp
        except Exception as e:
            db.session.rollback()
            print("GenericModel delete Exception: {0}".format(str(e)))
            return e

    @classmethod
    def delete_table(cls, confirm, re_confirm):
        """Allows you to delete a table from the database, if it exists as a data model."""

        if confirm is None:
            return None

        if re_confirm is None:
            return None

        if confirm == 'Yes' and re_confirm == 'YES':
            try:
                cls.__table__.drop(db.engine)
            except Exception as e:
                reason = "GenericModel delete_table Exception: {0}".format(e)
                print(reason)
                return str(reason)

        return None

    @classmethod
    def get_schema(cls):
        try:
            inspector = inspect(db.engine)
            schemas = inspector.get_schema_names()
            schema_list = []

            for schema in schemas:
                print("schema:", schema)
                for table_name in inspector.get_table_names(schema=schema):
                    schema_list.append(table_name)

            return schema_list
        except Exception as e:
            reason = "GenericModel get_schema Exception: {0}".format(e)
            print(reason)
            return str(reason)

    @classmethod
    def get_all(cls, _limit=0, select_fields=None):
        try:
            resp = None
            query = db.session.query(cls)

            if select_fields is not None:
                query = query.with_entities(*select_fields)

            if _limit > 0:
                query = query.limit(_limit)

            resp = query.all()

            if resp is None:
                return None
            else:
                return resp
        except Exception as e:
            db.session.rollback()
            print("GenericModel get_all Exception: {0}".format(e))
            return e

    @classmethod
    def get_by_id(cls, _id=0):
        if _id > 0:
            try:
                resp = cls.query.get(_id)
                if resp is None:
                    return None
                else:
                    return resp
            except Exception as e:
                db.session.rollback()
                print("GenericModel get_by_id Exception: {0}".format(str(e)))
                return e
        else:
            return None

    @classmethod
    def get_by(cls, _name=None, _value=None, result_fetch='one'):
        if _name is None:
            return None

        if _value is None:
            return None

        try:
            resp = None

            if result_fetch == 'one':
                resp = cls.query.filter(getattr(cls, _name) == _value).first()
            elif result_fetch == 'all':
                resp = cls.query.filter(getattr(cls, _name) == _value).all()

            if resp is None:
                return None
            else:
                return resp
        except Exception as e:
            db.session.rollback()
            print("GenericModel get_by Exception: {0}".format(str(e)))
            return e

    @classmethod
    def where_(cls, select_fields, _conds, result_fetch='one'):
        """Allows executing queries with custom fields (Select) and filters (Where)"""

        if select_fields is None:
            return None

        if _conds is None:
            return None

        resp = None

        try:
            query = db.session.query(cls)

            if select_fields is not None:
                query = query.with_entities(*select_fields)

            if _conds is not None:
                query = query.filter(*_conds)

            if result_fetch == 'one':
                resp = query.first()
            elif result_fetch == 'all':
                resp = query.all()

            if resp is None:
                return None
        except Exception as e:
            print("GenericModel where_(Query) Exception: {0}".format(e))
            return str(e)

        try:

            if isinstance(resp, (tuple)):
                result_one = Commons.to_json(resp._asdict())
                return result_one

            if isinstance(resp, (list)):
                result_all = cls.raw_json(resp, 'tuple')
                return result_all

            if isinstance(resp, (cls)):
                result_one = cls.to_json(resp)
                return result_one

        except Exception as e:
            print("GenericModel where_(Result) Exception: {0}".format(e))
            return str(e)

    @classmethod
    def select_from_view(cls, _view=None, _conds=None, result_fetch='one'):
        sql = None

        if _view is None:
            return None

        if _conds is None:
            sql = db.text("SELECT * FROM {0}".format(_view))
        else:
            sql = db.text("SELECT * FROM {0} WHERE {1}".format(_view, _conds))
        try:
            result_query = db.session.execute(sql)
            db.session.commit()

            fetch_query = None

            if result_fetch == 'one':
                fetch_query = result_query.first()
                result_one = dict(fetch_query)
                # return result_one
                return result_one
            # check
            elif result_fetch == 'all':
                fetch_query = result_query.fetchall()
                result_all = cls.raw_json(fetch_query)
                return result_all
        except Exception as e:
            db.session.rollback()
            print("select_from_view Exception: {0}".format(e))
            return None

    @classmethod
    def dict_to_obj(cls, _dict=None, _name='from_dict'):
        if _dict is None:
            return None

        try:
            new_obj = type(_name, (object,), _dict)
            return new_obj
        except Exception as e:
            print("GenericModel dict_to_obj Exception: {0}".format(str(e)))
            return None

    @classmethod
    def to_json(cls, obj=None):
        if obj is None:
            return None

        if (Commons.is_iterable(obj)):
            try:
                item_list = []
                num_obj = len(obj)
                if num_obj > 0:
                    for item in obj:
                        new_item = {c.key: getattr(item, c.key) for c in inspect(item).mapper.column_attrs}
                        new_item = json.dumps(new_item, indent=4, cls=customEncoder)
                        new_item = json.loads(new_item)
                        item_list.append(new_item)
                    return item_list
            except Exception as e:
                print("GenericModel to_json iterable Exception: {0}".format(str(e)))
                return e

        elif isinstance(obj, cls):
            try:
                resp = {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}
                resp = json.dumps(resp, indent=4, cls=customEncoder)
                resp = json.loads(resp)
                return resp
            except Exception as e:
                print("GenericModel to_json isinstance Exception: {0}".format(str(e)))
                return e

    @classmethod
    def raw_json(cls, obj=None, default='dict'):
        if obj is None:
            return None

        if default is not None:
            pass
            #print("the Default field is considered obsolete and will be removed in the next version")

        try:
            dict_list = []

            for item in obj:
                if isinstance(item, (cls)):
                    result = cls.to_json(item)
                    dict_list.append(result)
                elif isinstance(item, (tuple)):
                    result = Commons.to_json(item._asdict())
                    dict_list.append(result)
                else:
                    dict_list.append(dict(item))

            return dict_list
        except Exception as e:
            print("GenericModel raw_json Exception: {0}".format(str(e)))
            return str(e)

    @classmethod
    def raw_query(cls, _query):
        """allows to execute raw SQL queries"""

        if _query is None:
            return None

        try:
            sql = db.text(_query)
            result = db.session.execute(sql)
            db.session.commit()

            returns_rows = result.returns_rows

            if returns_rows is True:
                result_fetch = result.fetchall()

                if result_fetch is None:
                    return None
                else:
                    result_all = cls.raw_json(result_fetch)
                    return result_all

            return None
        except Exception as e:
            db.session.rollback()
            print("GenericModel raw_query Exception: {0}".format(str(e)))
            return str(e)

    @classmethod
    def raw_queries(cls, _query=None, raw_json=True, _params=None, _string=True):
        if _query is None:
            return None
        if _params is None:
            _params = {}
        try:
            if _string:
                sql = db.text(_query)
            else:
                sql = _query

            result = db.session.execute(sql, _params, bind=db.get_engine(None, cls.__bind_key__))
            db.session.commit()

            result_fetch = result.fetchall()
            if result_fetch is None:
                return None
            else:
                if not raw_json:
                    return result_fetch
                result_all = cls.raw_json(result_fetch)
                return result_all
        except Exception as e:
            db.session.rollback()
            print("GenericModel raw_query Exception: {0}".format(str(e)))
            raise e
