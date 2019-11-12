from flask import Flask,request,jsonify
from flask_restful import Api,Resource,reqparse
from flask_jwt import JWT,jwt_required

from security import authenticate,identity
from resources.user import RegisterUser
from resources.item import Item,ItemList
from resources.store import Store,StoreList
from db import db
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key='kannan'
api=Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt=JWT(app,authenticate,identity)


api.add_resource(RegisterUser,'/register')

api.add_resource(StoreList,'/store')
api.add_resource(Store,'/store/<string:name>')

api.add_resource(ItemList,'/items')
api.add_resource(Item,'/item/<string:name>')



if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0',port=5001,debug=True)
