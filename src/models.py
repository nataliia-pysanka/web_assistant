from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    hash = db.Column(db.String(255), nullable=False)
    token_cookie = db.Column(db.String(255), nullable=True, default=None)

    def __repr__(self):
        return f'User({self.username}, {self.email})'

#
# class Contact(db.Model):
#     __tablename__ = 'contacts'
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(30), nullable=False)
#     last_name = db.Column(db.String(30), nullable=False)
#     phones = relationship('Phone', back_populates='contact')
#     emails = relationship('Email', back_populates='contact')
#     adress = db.Column('address', db.String(100), nullable=True)
#     birth = db.Column('birth', db.Date, nullable=True)
#     groups = relationship('Group', secondary='contacts_to_groups',
#                           back_populates='contacts')
#
#
# class Phone(db.Column):
#     __tablename__ = 'phones'
#     id = db.Column(db.Integer, primary_key=True)
#     phone = db.Column('phone', db.String(20), nullable=False)
#     contact_id = db.Column('contact_id',
#                         ForeignKey('contacts.id', ondelete='CASCADE'),
#                         nullable=False)
#     contact = relationship('Contact', back_populates='phones')
#
#
# class Email(db.Column):
#     __tablename__ = 'emails'
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column('email', db.String(50), nullable=False)
#     contact_id = db.Column('contact_id',
#                         ForeignKey('contacts.id', ondelete='CASCADE'),
#                         nullable=False)
#     contact = relationship('Contact', back_populates='emails')
#
#
# class Group(db.Column):
#     __tablename__ = 'groups'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(120), nullable=False)
#     contacts = relationship('Contact', secondary='contacts_to_groups',
#                             back_populates='groups')
#
#
# class ContactGroup(db.Column):
#     __tablename__ = 'contacts_to_groups'
#     id = db.Column(db.Integer, primary_key=True)
#     group_id = db.Column('group_id', ForeignKey('groups.id', ondelete='CASCADE'))
#     contact_id = db.Column('contact_id', ForeignKey('contacts.id',
#                                                  ondelete='CASCADE'))
