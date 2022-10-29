from app.ext.generic_model import GenericModel

from sqlalchemy import Column, Integer, VARCHAR, TEXT, TIMESTAMP

class Deliverables (GenericModel):
    __tablename__ = 'deliverables'
    
    id   = Column(Integer, primary_key=True)
    name = Column(VARCHAR)
    description = Column(TEXT)
    date = Column(TIMESTAMP)
