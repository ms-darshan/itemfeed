from sqlalchemy import Integer, Column, String, create_engine, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship, joinedload, subqueryload, sessionmaker, backref
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from config import settings

Base = settings.getDeclartiveBase()

class Variant(Base):
    __tablename__ = "variant"
    variant_id = Column(Integer(), primary_key=True)
    name = Column(String(40), nullable=False)
    selling_price = Column(Numeric(12, 2))
    cost_price = Column(Numeric(12))
    item_id = Column(Integer, ForeignKey('item.item_id'))
    quantity = Column(Integer())
    status = Column(String(20), default="Active")
    item = relationship("Item", uselist=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "{}(name = {}, selling_price = {}, cost_price = {}, itm_id = {}, quantity = {}, status = {})".format(
                                                                             self.__class__.__name__, 
                                                                             self.name, self.selling_price, 
                                                                             self.cost_price, self.itm_id,
                                                                             self.quantity, self.status
                                                                            )

class Property(Base):
    __tablename__ = "property"
    propert_id = Column(Integer, primary_key=True)
    option = Column(String(10))
    value = Column(String(10))
    variant_id = Column(Integer, ForeignKey('variant.variant_id'))
    variant = relationship("Variant", backref=backref("property"))
    status = Column(String(20), default="Active")
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "{}(option = {}, value = {}, variantId = {}, variant = {})".format(self.__class__.__name__, self.option,
                                                                    self.value, self.variant_id, type(self.variant)
                                                                   )
