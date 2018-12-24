from lib.request import RequestHandler
from sqlalchemy.orm import  sessionmaker
from item.producer import ItemFeedGeneration
from item.models import Item
from sqlalchemy import and_
from lib.itemfeed_response import build_response
import arrow
import json

class ItemFeedMaker(object):
    def __init__(self, userName, itmName, action, atrbt=[]):
        self.userName = userName
        self.itmName  = itmName
        self.atrbt    = atrbt
        self.prducr   = ItemFeedGeneration()
        self.action   = action

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

class InsertItemHandler(RequestHandler):
    async def post(self):
        body = json.loads(self.request.body.decode("utf-8"))
        mandate = ["name", "brand", "category", "barcode", "user_name"]
        for x in mandate:
            if x not in body:
                return self.respond_json(build_response(119, "Missing Payload: "+x))
        engine     = self.APP.DBCONN.databases["itemandvariant"].client
        Session    = sessionmaker(bind=engine)
        session    = Session()
        itmObj     = Item(name=body["name"], brand=body["brand"], category=body["category"], barcode=body["barcode"], 
                         status="Active")
        session.add(itmObj)
        session.commit()
        data = dict({"item_id": itmObj.item_id, "name": itmObj.name})
        itm_instanse = ItemFeedMaker(body["user_name"], itmObj.name, "create")
        self.respond_json(data=data, raw = True)
        await itm_instanse.generate()

class UpdateItemHandler(RequestHandler):
    async def post(self):
        body = json.loads(self.request.body.decode("utf-8"))
        mandate = ["name", "brand", "category", "barcode", "user_name", "item_id"]
        for x in body:
            if x not in mandate:
                return self.respond_json(build_response(119, "Invalid Payload: " +x))
        if "item_id" not in body:
            return self.respond_json(build_response(119, "Missing Payload: " +"item_id"))
        if "user_name" not in body:
            return self.respond_json(build_response(119, "Missing Payload: " +"user_namec"))
        atrbt = []
        engine     = self.APP.DBCONN.databases["itemandvariant"].client
        Session    = sessionmaker(bind=engine)
        session    = Session()
        itmObj     = session.query(Item).filter(and_
                                                (Item.item_id==body["item_id"], 
                                                 Item.status=="Active"
                                                 )).one()
        if "name" in body:
            itmObj.name = body["name"]
            atrbt.append("name")
        if "brand" in body:
            itmObj.brand = body["brand"]
            atrbt.append("brand")
        if "category" in body:
            itmObj.category = body["category"]
            atrbt.append("category")
        if "barcode" in body:
            itmObj.barcode = body["barcode"]
            atrbt.append("barcode")
        session.add(itmObj)
        session.commit()
        data = dict({"item_id": itmObj.item_id, "name": itmObj.name})
        itm_instanse = ItemFeedMaker(body["user_name"], itmObj.name, "update", atrbt=atrbt)
        self.respond_json(data=data, raw = True)
        await itm_instanse.generate()

class DeleteItemHandler(RequestHandler):
    """
        DELETING IS NOT SUPPORTED YET.
    """
    pass
