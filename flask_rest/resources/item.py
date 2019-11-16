from flask import Flask,request,jsonify
from flask_restful import Resource,reqparse
from flask_jwt_extended import (jwt_required,
                                fresh_jwt_required,
                                get_jwt_claims,
                                jwt_optional,
                                get_jwt_identity)
from models.item import ItemModel


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

    @jwt_required
    def get(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"status": 404,"msg": "{} not found".format(name)}

    @fresh_jwt_required
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

    @jwt_required
    def delete(self,name):
        claims=get_jwt_claims()
        print(claims)
        if not claims['is_admin']:
            return {'message':'Admin privilage required'},401
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
    @jwt_optional
    def get(self):
        user_id=get_jwt_identity()
        items=[ item.json() for item in ItemModel.query.all()]
        if user_id:
            return {"items":items},200
        return {'items':[item['name'] for item in items],
                'message':'More data available if you login'},200
