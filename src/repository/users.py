from src import db
from src import models
import bcrypt


def create_user(email: str, password: str):
    hash_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(
        rounds=10))
    hashed = hash_pass.decode('utf-8')

    user = models.User(email=email, hash=hashed)
    db.session.add(user)
    db.session.commit()
    return user


def login(email: str, password: str):
    user = find_by_email(email)
    if not user:
        return None
    if not bcrypt.checkpw(password.encode('utf-8'), user.hash.encode('utf-8')):
        return None
    return user


def find_by_email(email: str):
    user = db.session.query(models.User).filter(models.User.email == email).\
        first()
    return user


def find_by_id(ids: int):
    user = db.session.query(models.User).filter(models.User.id == ids).\
        first()
    return user
