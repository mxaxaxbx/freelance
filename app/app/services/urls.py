from app.services.views.services import Services

from app.ext.register import url

urlpatterns = [
    url(name=Services, endpoint=['/services', '/services/<int:id>'])
]
