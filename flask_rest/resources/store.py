from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self,name):
        store=StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"msg":"Store not found"},404


    def post(self,name):
        store=StoreModel.find_by_name(name)
        if store:
            return {"msg":"Store {} already exisist".format(store.name)}
        store=StoreModel(name)
        try:
            store.insert()
        except Exception as e:
            print(e)
            return {"msg":"Error occured while inserting store"}
        return store.json(),200

    def delete(self):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
        return {"msg":"{} deleted".format(name)}

class StoreList(Resource):
    def get(self):
        stores=StoreModel.query.all()
        if stores:
            return {"stores":[store.json() for store in stores]}
        return {"msg":"Storelist is empty"},404
