from app.packages.views.packages import Packages

from app.ext.register import url

urlpatterns = [
    url(name=Packages, endpoint=['/packages'])
]
