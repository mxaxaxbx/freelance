from app.ext.generic_model import GenericModel

from sqlalchemy import Column, Integer, VARCHAR, TEXT, TIMESTAMP,  FLOAT

class Packages (GenericModel):
    __tablename__ = 'packages'
    
    id   = Column(Integer, primary_key=True)
    description = Column(TEXT)
    price = Column(FLOAT)
    deliverables_id = Column(Integer)
    service_id = Column(Integer)
