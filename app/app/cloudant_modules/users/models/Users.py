from app.ext.couchdb_model import CouchdbModel

class Users(CouchdbModel):
    __tablename__ = 'users'
    _id = None
    birthdate = ''
    email = ''
    lastname = ''
    name = ''
    password = ''
    role = ''
    crated_at = None
    updated_at = None