import sqlite3
from flask_restful import Resource,reqparse
from models.user import UserModel

class RegisterUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    def post(self):
        data=self.parser.parse_args()
        user=UserModel(data['username'],data['password'])
        try:
            user.insert()
        except Exception as e:
            print(e)
            return {"status":500,"msg":"Issue in creating the user"}
        return {"status":201}




if __name__ == '__main__':
    user=User.find_user_by_name(("kannan",))
    print(user)