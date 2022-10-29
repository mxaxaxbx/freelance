from app.ext.register import url
from app.cloudant_modules.users.views.users import ViewUsers

urlpatterns = [
    url(ViewUsers,endpoint=['/users','/users/<string:id>'], namespace='Regiter Users'),
]