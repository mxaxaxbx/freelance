from app.ext.generic_model import GenericModel

from sqlalchemy import Column, Integer, VARCHAR

class Services (GenericModel):
    __tablename__ = 'services'
    
    id   = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
