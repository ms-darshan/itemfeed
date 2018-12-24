"""
db_url = "postgresql://darshanms:@localhost/itemandvariant"
Session    = sessionmaker(bind=engine)
session    = Session()
itmObj     = Item(name="Cotton Shirt", brand="Polo", category="shirt", barcode="abcdg123253mdhs", status="active")
session.add(itmObj)
session.commit()

Session    = sessionmaker(bind=engine)
session    = Session()
varnObj    = Variant(name="Shirt", selling_price=105.5, cost_price=90, quantity=30, status="active")
itmObj     = session.query(Item).filter(Item.item_id==itmObj.item_id).one()
varnObj.item = itmObj
session.add(varnObj)
proprtObj1 = Property(option="size", value="L")
proprtObj2 = Property(option="size", value="M")
varnObj.property.append(proprtObj1)
varnObj.property.append(proprtObj2)
session.commit()
"""

"""
Session    = sessionmaker(bind=engine)
session    = Session()
itmObj     = session.query(Item).filter(Item.item_id==1).one()
varintObj  = session.query(Variant).filter(Variant.item==itmObj).one()
#prptyObj   = session.query(Property).filter(varintObj in Property.variant).all()
prptyObj = session.query(Property).filter(Property.variant==varintObj).all()

print("{} {} {} ".format(itmObj, varintObj, prptyObj))
"""

"""
Session    = sessionmaker(bind=engine)
session    = Session()
itemObj    = session.query(Item).filter(Item.id=1).one()
varnObj1   = Variant(Name="Shirt", SellingPrice=105.5, CostPrice=100, Quantity=30, status="active")
prptyObj3  = Property(option="size", value="XL")
session.commit()

Session    = sessionmaker(bind=engine)
session    = Session()
itemObj    = session.query(Item).filter(Item.id=1).one()
varnObj1   = Variant(Name="Shirt", SellingPrice=105.5, CostPrice=102, Quantity=40, status="active")
prptyObj4  = Property(option="size", value="XXL")
session.commit()
"""

"""
Session = sessionmaker(bind=engine)
session = Session()


instance = Item(Name="Cotton Shirt", Brand="Polo", Category="shirt", Barcode="abcdg123253mdhs", status="active")
Variant(Name="Shirt", SellingPrice=105.5, CostPrice=90, Quantity=30, status="active")
Property(option="size", value="L")
Property(option="size", value="M")

Variant(Name="Shirt", SellingPrice=105.5, CostPrice=100, Quantity=30, status="active")
Property(option="size", value="XL")

Variant(Name="Shirt", SellingPrice=105.5, CostPrice=102, Quantity=40, status="active")
Property(option="size", value="XXL")

session.add(instance)
session.bulk_save_objects([c1, c2])



session.query(Item).all()

session.query(Item.Name, Item.Category).first()



session.commit()
"""
