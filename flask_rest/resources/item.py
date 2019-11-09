from flask import Flask,request,jsonify
from flask_restful import Api,Resource,reqparse
from flask_jwt import JWT,jwt_required
from models.item import ItemModel

from security import authenticate,identity

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every Item need a store id")

    @jwt_required()
    def get(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"status": 404,"msg": "{} not found".format(name)}

    def post(self,name):
        data = self.parser.parse_args()
        item = ItemModel.query.filter_by(name=name,store_id=data["store_id"])
        if item.first():
            return {"status": 400, "msg": "Item already exist"}
        else:
            newitem = ItemModel(name, data["price"], data["store_id"])
            try:
                newitem.insert()
            except:
                return {"msg": "Error occured while inserting"}, 500
            return {"status": 201, "item": newitem.json()}


    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
        return {"msg":"Item deleted"}

    def put(self,name):
        item=ItemModel.find_by_name(name)
        data = self.parser.parse_args()
        if not item:
            item=ItemModel(name,data["price"],data["store_id"])
            #item = ItemModel(name, **data)
            msg={"status":200,"msg":"{} created".format(name)}
        else:
            item.price=data['price']
            msg={"status":200,"msg":"{} updated".format(name),"item":item.json()}
        item.insert()
        return msg

class ItemList(Resource):
    def get(self):
        return {"items":[ x.json() for x in ItemModel.query.all()]}
