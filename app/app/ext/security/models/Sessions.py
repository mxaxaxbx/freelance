from app.ext.couchdb_model import CouchdbModel

class Sessions(CouchdbModel):
    __tablename__ = 'sessions'

    _id = None
    token = ''
    status = None
    token_type = ''
    user_id = ''
    created_at = None
    updated_at = None