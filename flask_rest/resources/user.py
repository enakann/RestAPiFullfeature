import sqlite3
from flask_restful import Resource,reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_required,
                                jwt_refresh_token_required,
                                get_jwt_identity,
                                get_raw_jwt)
from models.user import UserModel
from blacklist import BLACKLIST


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                    type=str,
                    required=True,
                    help="This field cannot be blank")
_user_parser.add_argument('password',
                    type=str,
                    required=True,
                    help="This field cannot be blank")

class RegisterUser(Resource):
    def post(self):
        data=_user_parser.parse_args()
        user=UserModel(data['username'],data['password'])
        try:
            user.insert()
        except Exception as e:
            print(e)
            return {"status":500,"msg":"Issue in creating the user"}
        return {"status":201}

class User(Resource):
    @classmethod
    def get(cls,user_id):
        user=UserModel.find_user_by_id(user_id)
        #import pdb;pdb.set_trace()
        if not user:
            return {"Message":"User not found"},404
        return user.json()
    @classmethod
    def delete(cls,user_id):
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {"Message": "User not found"}, 404
        user.delete()
        return {"Message":"User deleted"},200

class UserLogin(Resource):
    def post(self):
        # get data from parser
        data=_user_parser.parse_args()
        # find user in database
        user=UserModel.find_user_by_name(data['username'])
        # check password and # create access & refresh token
        if user and safe_str_cmp(user.password,data["password"]):   #this was done by authenticate function
            access_token= create_access_token(identity=user.id,fresh=True) #this was done by identity function
            refresh_token=create_refresh_token(user.id)
        # return (access & refresh tokens)
            return {
                'access_token':access_token,
                'refresh_token':refresh_token
            },200
        return {'message':'Invalid Credentials'},401

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user=get_jwt_identity()
        new_token=create_access_token(identity=current_user,fresh=False)
        return {'access_token':new_token},200

class UserLogOut(Resource):
    @jwt_required
    def post(self):
        jti= get_raw_jwt()['jti'] #jti is a unique identier for a jwt
        BLACKLIST.add(jti)
        return {'message':"Sucessfully logged out"},200
if __name__ == '__main__':
    user=User.find_user_by_name(("kannan",))
    print(user)