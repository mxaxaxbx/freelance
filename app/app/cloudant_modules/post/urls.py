from app.ext.register import url
from app.cloudant_modules.post.views.createPost import ViewCreatePost
from app.cloudant_modules.post.views.setPostTitle import ViewSetPostTitle
from app.cloudant_modules.post.views.setPostBody import ViewSetPostBody
from app.cloudant_modules.post.views.savePostAsDraft import ViewSavePostAsDraft
from app.cloudant_modules.post.views.publishPost import ViewPublishPost
from app.cloudant_modules.post.views.getUserPosts import ViewUserPosts
from app.cloudant_modules.post.views.deletePost import ViewDeletePost
from app.cloudant_modules.post.views.setPostAsDraft import ViewSetPostAsDraft
from app.cloudant_modules.post.views.setPostAsPublic import ViewSetPostAsPublic

urlpatterns = [
    url(ViewCreatePost, endpoint=['/createPost'], namespace='Posts'),
    url(ViewSetPostTitle, endpoint=['/setPostTitle'], namespace='setPostTitle'),
    url(ViewSetPostBody, endpoint=['/setPostBody'], namespace='setPostBody'),
    url(ViewSavePostAsDraft, endpoint=['/savePostAsDraft'], namespace='savePostAsDraft'),
    url(ViewPublishPost, endpoint=['/publishPost'], namespace='publishPost'),
    url(ViewUserPosts, endpoint=['/getPosts', '/getPosts/<string:id>'], namespace='getPosts'),
    url(ViewDeletePost, endpoint=['/deletePost/<string:id>'], namespace='deletePost'),
    url(ViewSetPostAsDraft, endpoint=['/setPostAsDraft/<string:id>'], namespace='setPostAsDraft'),
    url(ViewSetPostAsPublic, endpoint=['/setPostAsPublic/<string:id>'], namespace='setPostAsPublic'),
]