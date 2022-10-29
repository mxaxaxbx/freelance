from app.ext.resource_handler import ResourceHandler
from app.ext.rest import Rest, HttpStatus
from app.ext.security import Auth
from app.ext.utils import Commons
from app.cloudant_modules.post.models.Post import Post

from flask import request

class ViewPublishPost(ResourceHandler):
    decorators = [
        Auth.require_auth_session,
    ]

    def get(self, id=''):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)

    def post(self):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)

    def put(self):
        user_id = request.headers.get('UserId')

        data = request.get_json()

        postId = data.get('postId')
        postTitle = data.get('postTitle')
        postBody = data.get('postBody')

        post = Post.get_by_id(postId)
        if type(post) == dict: return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, errors=post['reason'])

        if post.user_id != user_id: return Rest.response(400, HttpStatus.UNAUTHORIZED)

        if len(postTitle) < 1: return Rest.response(400, HttpStatus.DEFAULT_ERROR_MESSAGE, errors='Enter a valid Post Title ')

        if len(post.url) == 7:
            titleHashed = postTitle.replace(' ', '-')
            postUrl = titleHashed+post.url
        else:
            postUrl = post.url

        post.title = postTitle
        post.body = postBody
        post.draft = 2
        post.url = postUrl
        res = Post.update(post)

        if 'error' in res: return Rest.response(400, HttpStatus.UNEXPECTED_ERROR, errors=str(res['reason']))
        
        return Rest.response(200, HttpStatus.OK, res)

    def delete(self, id=''):
        return Rest.response(404, HttpStatus.RESOURCE_NOT_EXIST)
