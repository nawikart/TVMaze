from sqlalchemy import or_, and_
from db.base import DbManager
from db.models import User, Like

def get_all_likes_for(user_id):
    db = DbManager()
    return db.open().query(Like).filter(Like.user_id == user_id).all()

def get_show_ids_liked(user_id):
    show_ids = []
    db = DbManager()
    for s in db.open().query(Like).filter(Like.user_id == user_id).all():
        show_ids.append(s.show_id)
    return show_ids

def _unlike(user_id, show_id):
    db = DbManager()
    like = db.open().query(Like).filter(Like.show_id == show_id).filter(Like.user_id == user_id).one()
    like = db.delete(like)
    db.close()
    return like    

def create__like(user_id, show_id):
    db = DbManager()
    like = Like()
    check = db.open().query(Like).filter(Like.user_id == user_id).filter(Like.show_id == show_id).all()
    if len(check) == 0:
        like.show_id = show_id
        like.user_id = user_id
        return db.save(like)

    return False

def create_user(fullname, username, email, password):
    db = DbManager()
    user = User()
    user.fullname = fullname
    user.username = username
    user.email = email
    user.password = password
    return db.save(user)

def get_user_by_id(user_id):
    db = DbManager()
    return db.open().query(User).filter(User.id == user_id).one()

def get_user_by_email(email):
    db = DbManager()
    return db.open().query(User).filter(User.email == email).one()

def get_user_by_name(username):
    db = DbManager()
    return db.open().query(User).filter(User.username == username).one()