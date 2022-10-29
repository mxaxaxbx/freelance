from app.ext.resource_handler import ResourceHandler
from app.ext.rest import Rest

from app.models.packages import Packages as PackagesModel
from app.models.services import Services
from app.models.deliverables import Deliverables

from flask import request


class Packages(ResourceHandler):

    def get (self):
        packages = PackagesModel.get_all()
        return Rest.response(200, data=PackagesModel.to_json(packages))
    
    def post (self):
        content = request.json
        description = content.get('description')
        price = content.get('price')
        deliverable_id = content.get('deliverables_id')
        service_id = content.get('service_id')
        
        service = Services.get_by_id(int(service_id))
        if service is None:
            return Rest.response(400, 'Enter a valid service ID')
        
        deliverable = Deliverables.get_by_id(int(deliverable_id))
        if deliverable is None:
            return Rest.response(400, 'Enter a valid deliverable ID')

        package = PackagesModel()
        package.description = description
        package.price = float(price)
        package.deliverables_id = deliverable_id
        package.service_id = service_id
        PackagesModel.save(package)
        
        return Rest.response(200, message='OK', data=PackagesModel.to_json(package))
