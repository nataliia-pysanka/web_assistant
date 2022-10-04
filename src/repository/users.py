import bcrypt
from src import db
from src.models import User


def create_user(email: str, password: str):
    hash_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(
        rounds=10))
    hashed = hash_pass.decode('utf-8')

    user = User(email=email, hash=hashed)
    db.session.add(user)
    db.session.commit()
    return user


def login(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return None
    if not bcrypt.checkpw(password.encode('utf-8'), user.hash.encode('utf-8')):
        return None
    return user


def get_user_by_email(email: str):
    user = db.session.query(User).filter(User.email == email).\
        first()
    return user


def get_user_by_id(ids: int):
    user = db.session.query(User).filter(User.id == ids).\
        first()
    return user


def set_token(user: User, token: str):
    user.token_cookie = token
    db.session.commit()


def get_user_by_token(token):
    user = db.session.query(User).filter(User.token_cookie == token).first()
    if not user:
        return None
    return user
