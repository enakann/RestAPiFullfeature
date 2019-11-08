from user import User

# users=[
#     User(1,"kannan","kannan")
# ]
#
# username_mapping={u.username:u for u in users}
#
#
# userid_mapping={ u.id : u for u in users}


def authenticate(username,password):
    #user=username_mapping.get(username,None)
    user=User.find_user_by_name(username)
    if user and user.password == password:
        return user


def identity(payload):
    #import pdb;pdb.set_trace()
    print(payload)
    user_id=payload['identity']
    return User.find_user_by_id(user_id)