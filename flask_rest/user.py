import sqlite3
from flask_restfull import Resource,reqparse

class User:
    def __init__(self,_id,username,password):
        self.id=_id
        self.username=username
        self.password=password
    @classmethod
    def find_user_by_id(cls,_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query="SELECT * from users where id = ?"
        ret=cursor.execute(query,(_id,))
        item=list(ret)[0]
        if item:
            user = cls(*item)
        else:
            user = None
        return user
    @classmethod
    def find_user_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * from users where username = ?"
        ret = cursor.execute(query, (name,))
        item=list(ret)[0]
        if item:
            user = cls(*item)
        else:
            user = None
        return user
    def __str__(self):
        return "User({},{})".format(self.id,self.username)

    def __repr__(self):
        return str(self)


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





if __name__ == '__main__':
    user=User.find_user_by_name(("kannan",))
    print(user)