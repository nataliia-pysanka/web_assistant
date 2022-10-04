from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from src.db import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    hash = db.Column(db.String(255), nullable=False)
    token_cookie = db.Column(db.String(255), nullable=True, default=None)

    def __repr__(self):
        return f'User({self.username}, {self.email})'


class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    phones = relationship('Phone', back_populates='contact')
    emails = relationship('Email', back_populates='contact')
    adress = db.Column('address', db.String(100), nullable=True)
    birth = db.Column('birth', db.Date, nullable=True)
    groups = relationship('ContactGroup', back_populates='contact')

    def __repr__(self):
        return f"Contact({self.first_name} {self.last_name})"


class Phone(db.Model):
    __tablename__ = 'phones'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column('phone', db.String(20), nullable=False)
    contact_id = db.Column(db.Integer, ForeignKey('contacts.id'),
                           nullable=False)
    contact = relationship('Contact', cascade='all, delete',
                           back_populates='phones')

    def __repr__(self):
        return f"Phone({self.phone})"


class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column('email', db.String(50), nullable=False)
    contact_id = db.Column('contact_id', ForeignKey('contacts.id'),
                        nullable=False)
    contact = relationship('Contact', cascade='all, delete',
                           back_populates='emails')

    def __repr__(self):
        return f"Email({self.email})"


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    contacts = relationship('ContactGroup', back_populates='group')

    def __repr__(self):
        return f"Group({self.name})"


class ContactGroup(db.Model):
    __tablename__ = 'contacts_to_groups'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(ForeignKey('groups.id', primary_key=True))
    contact_id = db.Column(ForeignKey('contacts.id', primary_key=True))
    group = relationship("Group", back_populates="contacts")
    contact = relationship("Contact", back_populates="groups")
