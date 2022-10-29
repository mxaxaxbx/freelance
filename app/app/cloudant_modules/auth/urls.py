from app.ext.register import url
from app.cloudant_modules.auth.views.loginUser import ViewloginUser

urlpatterns = [
    url(ViewloginUser, endpoint=['/auth/login'], namespace='Login Users'),
]