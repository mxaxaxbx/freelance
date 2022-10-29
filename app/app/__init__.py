from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from .config.settings import SECRET_KEY
from .config.storage import MAX_FILE_SIZE, DEFAULT_BUCKET
from .config.cache import init_werkzeug_cache
from .config.local_settings import ALLOW_METHODS


app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY=SECRET_KEY,
    MAX_CONTENT_LENGTH=MAX_FILE_SIZE,
    UPLOAD_FOLDER=DEFAULT_BUCKET,
))

BINDS = {
    'db': 'postgresql+psycopg2://postgres:postgres@db_app:5432/freelance_db',
}

app.config.update(dict(
    SQLALCHEMY_ECHO=False,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_BINDS=BINDS,
    SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://postgres:postgres@db_app:5432/freelance_db'
))
db = SQLAlchemy(app)
ma = Marshmallow(app)

cache = init_werkzeug_cache()

api = Api(app)

cors = CORS(app, resources={
    r'*':{
        'allow_headers':'*',
        'support_credentials':'true',
        'max_age':1,
        'methods':ALLOW_METHODS,
        'Access-Control-Allow-Origin': '*',
    }
})

from app.ext.register import Register
reg_api = Register()