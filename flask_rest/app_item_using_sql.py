from flask import Flask,request,jsonify
from flask_restful import Api,Resource,reqparse
from flask_jwt import JWT,jwt_required


from security import authenticate,identity

app=Flask(__name__)
app.secret_key='kannan'
api=Api(app)

jwt=JWT(app,authenticate,identity)    #/auth

items=[]


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank")

    @jwt_required()
    def get(self,name):
        item=next(filter(lambda x:x.get("name",None)==name,items),None)
        if item:
            return {"status": 200,"item":item}
        return {"status": 404,"msg": "{} not found".format(name)}

    def post(self,name):
        item=next(filter(lambda x:x.get("name",None)==name,items),None)
        if not item:
            data = self.parser.parse_args()
            item = {"name": name, "price": data["price"]}
            items.append(item)
            return {"status": 201, "item": item}
        return {"status":400,"msg":"Item already exist"}

    def delete(self,name):
        for item in items:
            if item["name"] == name:
                items.remove(item)
                msg = {"status": 200, "msg": "{} deleted".format(name)}
                break
        else:
            msg = {"status": 404, "msg": "{} not found".format(name)}
        return msg

    def put(self,name):
        #data=request.get_json()   #its not needed
        item=next(filter(lambda x:x.get("name",None)==name,items),None)
        if not item:
            data = self.parser.parse_args()
            item={"name":name,"price":data["price"]}
            items.append(item)
            msg={"status":200,"msg":"{} created".format(name)}
        else:
            item.update(data)
            msg={"status":200,"msg":"{} updated".format(name),"item":item}
        return msg

class ItemList(Resource):
    def get(self):
        return {'items':items},200



api.add_resource(ItemList,'/items')
api.add_resource(Item,'/item/<string:name>')


if __name__ == '__main__':
    app.run(debug=True)