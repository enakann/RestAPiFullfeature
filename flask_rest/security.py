from models.user import UserModel


def authenticate(username,password):
    user=UserModel.find_user_by_name(username)
    if user and user.password == password:
        return user


def identity(payload):
    print(payload)
    user_id=payload['identity']
    return UserModel.find_user_by_id(user_id)