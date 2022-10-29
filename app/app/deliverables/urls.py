from app.deliverables.views.deliverables import Deliverables

from app.ext.register import url

urlpatterns = [
    url(name=Deliverables, endpoint=['/deliverables'])
]
