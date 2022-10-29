from app.ext.resource_handler import ResourceHandler
from app.ext.rest import Rest, HttpStatus
from app.ext.security import Auth
from app.ext.utils import Commons
from app.cloudant_modules.post.models.Post import Post

from flask import request

class ViewDeletePost(ResourceHandler):
    decorators = [
        Auth.require_auth_session,
    ]

    def get(self, id=''):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)

    def post(self):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)
        
    def put(self):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)

    def delete(self, id=''):
        user_id = request.headers.get('UserId')

        if id is None: return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST, errors='Enter a valid Post Id ')

        post = Post.get_by_id(id)
        if type(post) == dict: return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST, errors=post['reason'])

        if post.user_id != user_id: return Rest.response(400, HttpStatus.UNAUTHORIZED)

        res = Post.delete(post._id)
        if 'error' in res: return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, errors=str(res['reason']))
        
        return Rest.response(200, HttpStatus.OK, res)
