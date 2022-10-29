from app.ext.register import url
from app.cloudant_modules.register.views.registerUser import ViewRegisterUser

urlpatterns = [
    url(ViewRegisterUser, endpoint=['/registerUser'], namespace='Register Users'),
]