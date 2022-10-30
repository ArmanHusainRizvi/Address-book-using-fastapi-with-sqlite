from operator import concat
from sqlalchemy import Column, Integer, String
from database import Base

#creating new class named Books==============
 
class Books(Base):
    __tablename__ = "books"
#creating models for our address book ==============

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    father_name = Column(String)
    concat = Column(Integer)
    address = Column(String)