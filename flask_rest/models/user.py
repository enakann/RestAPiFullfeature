import sqlite3
from db import db

class UserModel(db.Model):
    __tablename__ = 'users'
    #__table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))


    def __init__(self,username,password):
        self.username=username
        self.password=password
    @classmethod
    def find_user_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()
    @classmethod
    def find_user_by_name(cls,name):
        return cls.query.filter_by(username=name).first()
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def __str__(self):
        return "User({},{})".format(self.id,self.username)

    def __repr__(self):
        return str(self)