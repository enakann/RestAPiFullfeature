from flask import Flask,request,jsonify,render_template
from flask_restful import Api,Resource
import copy


app=Flask(__name__)

api=Api(app)


storecontents=[
    {
        "name":"store1",
        "items":[
            {
                "name":"shirt",
                "price":100
            }
        ]
    },
{
        "name":"store2",
        "items":[
            {
                "name":"pant",
                "price":200
            }
        ]
    }
]

def geturl_fordata(ls):
    copy_ls=copy.deepcopy(ls)
    newcontent=[]
    for item in copy_ls:
        item["url"]="http://127.0.0.1:5000/store/{}".format(item["name"])
        newcontent.append(item)
    return newcontent

@app.route("/")
def home():
    return render_template("index.html")


class Store(Resource):
    def get(self):
        new_storecontents = geturl_fordata(storecontents)
        return jsonify({"storecontents":new_storecontents})

    def post(self):
        data=request.get_json()
        new_store={
            "name":data['name'],
            "items":[]
        }
        storecontents.append(new_store)
        return {"status":200,"store":new_store}


class Item(Resource):

    def get(self,name):
        store = [x for x in storecontents if x["name"] == name][0]
        return jsonify({"stauts":200,"store":store})

    def post(self,name):
        item=request.get_json()
        for store in storecontents:
            if store["name"]==name:
                store["items"].append(item)
                return jsonify({"status":200})





api.add_resource(Store,'/store')

api.add_resource(Item,"/store/<string:name>")


if __name__ == '__main__':
    app.run()
