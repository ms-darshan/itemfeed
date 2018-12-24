from sqlalchemy import Integer, Column, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship, sessionmaker, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from config import settings

Base = settings.getDeclartiveBase()

class Item(Base):
    __tablename__ = "item"
    item_id = Column(Integer(), primary_key=True, unique=True)
    name = Column(String(40), nullable=False)
    brand = Column(String(40), nullable=False)
    category = Column(String(40), nullable=False, index=True)
    barcode = Column(String(40))
    status = Column(String(20), default="Active", nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return "{}(name = {}, brand = {}, category = {}, barcode = {}, status = {})".format(self.__class__.__name__, 
                                                                                    self.name, self.brand, self.category,
                                                                                    self.barcode, self.status)
