from app.ext.resource_handler import ResourceHandler
from app.ext.rest import Rest, HttpStatus
from app.ext.security import Auth
from app.ext.utils import Commons
from app.cloudant_modules.post.models.Post import Post
from app.cloudant_modules.users.models.Users import Users

from flask import request

class ViewUserPosts(ResourceHandler):
    decorators = [
        Auth.require_auth_session,
    ]

    def get(self, id=''):
        user_id = request.headers.get('UserId')

        if id == '':
            q = {'user_id': user_id}
            listFileds = ['_id', 'title', 'draft', 'updated_at']
            res = Post.raw_query(q, nSkip=0, nLimit=50, listFileds=listFileds)
        else:
            post = Post.get_by_id(id)
            if type(post) == dict: return Rest.response(400, HttpStatus.RESOURCE_NOT_EXIST, errors=post['reason'])

            if post.user_id != user_id: return Rest.response(400, HttpStatus.UNAUTHORIZED)
            
            res = Post.to_json(post)

        return Rest.response(200, HttpStatus.OK, res)

    def post(self):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)

    def put(self):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)

    def delete(self, id=''):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)
