from app.ext.register import url
from app.home.views.home import ViewHome

urlpatterns = [
    url(ViewHome, endpoint=['/'], namespace="register_home")
]