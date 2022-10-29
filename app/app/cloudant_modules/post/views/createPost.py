from app.ext.resource_handler import ResourceHandler
from app.ext.rest import Rest, HttpStatus
from app.ext.security import Auth
from app.ext.utils import Commons
from app.cloudant_modules.post.models.Post import Post

from flask import request
from random import choice

class ViewCreatePost(ResourceHandler):
    decorators = [
        Auth.require_auth_session,
    ]
    def get(self, id=''):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)

    def post(self):
        user_id = request.headers.get('UserId')
        url_id =  '-'+self.generateRandomString(6)

        post = Post()
        post.title = ''
        post.draft = 1
        post.url = url_id
        post.user_id = user_id
        res = Post.save(post)
        if 'error' in res: return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, errors=str(res['reason']))
        return Rest.response(200, HttpStatus.OK, res['id'])

    def put(self, id=''):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)

    def delete(self, id=''):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)

    def generateRandomString(self, long=7):
        values = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
        value = ''.join([choice(values) for i in range(long)])
        isValidUrl = self.validateUrl(value)
        if isValidUrl is False:
            self.generateRandomString(long)
        return value

    def validateUrl(self, url):
        post = Post.get_by('url', url)
        if not post:
            return True
        return False
