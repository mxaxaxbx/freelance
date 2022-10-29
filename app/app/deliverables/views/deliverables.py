from app.ext.resource_handler import ResourceHandler
from app.ext.rest import Rest

from app.models.deliverables import Deliverables as DeliverablesModel

from flask import request

from datetime import datetime

class Deliverables(ResourceHandler):

    def get (self):
        deliverables = DeliverablesModel.get_all()
        return Rest.response(200, DeliverablesModel.to_json(deliverables))
    
    def post (self):
        content = request.json
        name = content.get('name')
        description = content.get('description')
        date = content.get('date')
        dt = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        deliverables = DeliverablesModel()
        deliverables.name = name
        deliverables.description = description
        deliverables.date = dt
        DeliverablesModel.save(deliverables)
        
        return Rest.response(200, 'OK', data=DeliverablesModel.to_json(deliverables))
