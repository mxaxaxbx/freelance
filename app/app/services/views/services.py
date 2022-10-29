from app.ext.resource_handler import ResourceHandler
from app.ext.rest import Rest

from app.models.services import Services as ServicesModel
from app.models.packages import Packages
from app.models.deliverables import Deliverables

from flask import request

class Services(ResourceHandler):

    def get (self, id=0):
        if id == 0:
            services = ServicesModel.get_all()
            data = list()
            for s in services:
                d = ServicesModel.to_json(s)
                package = Packages.get_by('service_id', s.id)
                if package:
                    d['package'] = Packages.to_json(package)
                    deliverable = Deliverables.get_by_id(package.deliverables_id)
                    d['package']['deliverables'] = Deliverables.to_json(deliverable)

                data.append(d)

            return Rest.response(200, data=data)
        
        else:
            service = ServicesModel.get_by_id(id)
            if service is None:
                return Rest.response(400, message='Enter a valid service ID')
            d = ServicesModel.to_json(service)

            package = Packages.get_by('service_id', service.id)
            if package:
                d['package'] = Packages.to_json(package)
                deliverable = Deliverables.get_by_id(package.deliverables_id)
                d['package']['deliverables'] = Deliverables.to_json(deliverable)
            
            return Rest.response(200, data=d)
    
    def post (self):
        content = request.json
        name = content.get('name')
        service = ServicesModel()
        service.name = name
        ServicesModel.save(service)
        return Rest.response(200, 'OK', data=ServicesModel.to_json(service))
