from lib.request import RequestHandler
from sqlalchemy.orm import  sessionmaker
from variant.producer import VariantFeedGeneration
from variant.models import Variant, Property
from item.models import Item
from lib.itemfeed_response import build_response
import arrow
import json

class VariantFeedMaker(object):
    def __init__(self, userName, itmName, variantName, action, atrbt=[]):
        self.userName = userName
        self.itmName  = itmName
        self.atrbt    = atrbt
        self.prducr   = VariantFeedGeneration()
        self.action   = action
        self.variantName = variantName

    async def generate(self):
        data = {
                 "user_name": self.userName,
                 "item_name": self.itmName,
                 "action": self.action,
                 "whtTime": arrow.utcnow().timestamp
               }
        if len(self.atrbt)>0:
            data["attribute"] = self.atrbt
        print(self.prducr.send(data))

class InsertVariantHandler(RequestHandler):
    async def post(self):
        body = json.loads(self.request.body.decode("utf-8"))
        mandate = ["name", "selling_price", "cost_price", "item_id", "quantity", "property", "user_name"]
        for x in mandate:
            if x not in body:
                return self.respond_json(build_response(119, "Missing Payload: "+x))
            if x == "property":
                for prpt in body["property"]:
                    if "option" not in prpt or "value" not in prpt:
                        return self.respond_json(build_response(119, "Wrong Format: "+x + " expects option and value as mandatory object"))
        engine     = self.APP.DBCONN.databases["itemandvariant"].client
        Session    = sessionmaker(bind=engine)
        session    = Session()
        vrntObj    = Variant(name=body["name"], selling_price=body["selling_price"], cost_price=body["cost_price"], 
                            quantity=body["quantity"], status="Active")
        itmObj     = session.query(Item).filter(Item.item_id==body["item_id"], Item.status=="Active").one()
        vrntObj.item = itmObj
        session.add(vrntObj)
        for prptyObj in body["property"]:
            proprtObj = Property(option=prptyObj["option"], value=prptyObj["value"])
            vrntObj.property.append(proprtObj)
        session.commit()
        data = dict({"variant_id": vrntObj.variant_id, "item_id": body["item_id"]})
        vrnt_instanse = VariantFeedMaker(body["user_name"], itmObj.name, vrntObj.name, "create")
        self.respond_json(data=data, raw = True)
        await vrnt_instanse.generate()

class UpdateVariantHandler(RequestHandler):
    async def post(self):
        body = json.loads(self.request.body.decode("utf-8"))
        mandate = ["name", "selling_price", "cost_price", "item_id", "quantity", "property", "user_name", "variant_id"]
        for x in body:
            if x not in mandate:
                return self.respond_json(build_response(119, "Invalid Payload: " +x))
        if "variant_id" not in body:
            return self.respond_json(build_response(119, "Missing Payload: " +"variant_id"))
        if "user_name" not in body:
            return self.respond_json(build_response(119, "Missing Payload: " +"user_namec"))

        atrbt = []
        engine     = self.APP.DBCONN.databases["itemandvariant"].client
        Session    = sessionmaker(bind=engine)
        session    = Session()
        varintObj  = session.query(Variant).filter(Variant.variant_id==body["variant_id"], Variant.status=="Active").one()
        if "name" in body:
            varintObj.name = body["name"]
            atrbt.append("name")
        if "selling_price" in body:
            varintObj.selling_price = body["selling_price"]
            atrbt.append("selling_price")
        if "cost_price" in body:
            varintObj.cost_price = body["cost_price"]
            atrbt.append("cost_price")
        if "quantity" in body:
            varintObj.quantity = body["quantity"]
            atrbt.append("quantity")
        session.add(varintObj)
        if "property" in body:
            propertObj = session.query(Property).filter(Property.variant==varintObj).all()
            for prop in propertObj:
                prop.status = "deleted"
                varintObj.property.append(prop)
            for prptyObj in body["property"]:
                try:
                    proprtObj = Property(option=prptyObj["option"], value=prptyObj["value"])
                    varintObj.property.append(proprtObj)
                except ValueError:
                    continue
            atrbt.append("property")
        session.commit()
        data = dict({"variant_id": varintObj.variant_id, "item_id": varintObj.item.item_id})
        vrnt_instanse = VariantFeedMaker(body["user_name"], varintObj.item.name, varintObj.name, "update", atrbt=atrbt)
        self.respond_json(data=data, raw = True)
        await vrnt_instanse.generate()

class DeleteVariantHandler(RequestHandler):
    async def post(self):
        body = json.loads(self.request.body.decode("utf-8"))
        mandate = ["variant_id", "user_name"]
        variantName = ""
        ItemName = ""
        for x in mandate:
            if x not in body:
                return self.respond_json(build_response(119, "Missing Payload: "+x))
        
        engine      = self.APP.DBCONN.databases["itemandvariant"].client
        Session     = sessionmaker(bind=engine)
        session     = Session()
        varintObj   = session.query(Variant).filter(Variant.variant_id==body["variant_id"], Variant.status=="Active").one()
        variantName = varintObj.name
        ItemName    = varintObj.item.name
        propertObj  = session.query(Property).filter(Property.variant==varintObj).delete()
        session.delete(varintObj)
        session.commit()
        data = dict({"variant_id": body["variant_id"]})
        vrnt_instanse = VariantFeedMaker(body["user_name"], ItemName, variantName, "delete")
        self.respond_json(data=data, raw = True)
        await vrnt_instanse.generate()
