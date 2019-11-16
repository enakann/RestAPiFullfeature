from flask import Flask,request,jsonify
from flask_restful import Api,Resource,reqparse
#from flask_jwt import JWT,jwt_required
from flask_jwt_extended import JWTManager

from blacklist import BLACKLIST
from security import authenticate,identity
from resources.user import RegisterUser,User,UserLogin,TokenRefresh,UserLogOut
from resources.item import Item,ItemList
from resources.store import Store,StoreList
from db import db
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh']
app.secret_key='kannan'  #app.config['JWT_SECRET_KEY']
api=Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

#jwt=JWT(app,authenticate,identity)
jwt=JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: #Instead of hard_coding ,you should read from db
        return {'is_admin':True}
    return {'is_admin':False}

@jwt.token_in_blacklist_loader
def check_if_token_in_black_list(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        "description":"The token has expired.",
        "error":"token expired"
    }),401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "description": "Invalid token idiot.",
        "error": "invalid token"
    }), 401


@jwt.unauthorized_loader
def unauthorized_loader_callback(error):
    return jsonify({
        "description": "There is no token stupid.",
        "error": "No token"
    }), 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(error):
    return jsonify({
        "description": "You have sent a non fresh oken moron",
        "error": "non fresh token"
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "Token has been revoked",
        "error": "token revoked"
    }), 401

api.add_resource(RegisterUser,'/register')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(UserLogin,'/login')
api.add_resource(TokenRefresh,'/refresh')
api.add_resource(UserLogOut,'/logout')

api.add_resource(StoreList,'/store')
api.add_resource(Store,'/store/<string:name>')

api.add_resource(ItemList,'/items')
api.add_resource(Item,'/item/<string:name>')



if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0',port=5000,debug=True)
