from app.ext.couchdb_model import CouchdbModel

class Post(CouchdbModel):
    __tablename__ = 'posts'

    _id = None
    title = ''
    body = ''
    draft = None
    url = ''
    user_id = None
    created_at = None
    updated_at = None