from sqlalchemy.orm import relationship, backref

from src.db import db


class User(db.Model):
    __tablename__ = 'user_table'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    hash = db.Column(db.String(255), nullable=False)
    token_cookie = db.Column(db.String(255), nullable=True, default=None)
    contacts = relationship('Contact', back_populates='user',
                            cascade="all, delete")

    def __repr__(self):
        return f'User({self.username}, {self.email})'

    def __str__(self):
        return f'{self.username}'


contact_group = db.Table('contact_group',
                         db.Column('contact_id', db.Integer,
                                   db.ForeignKey('contact_table.id')),
                         db.Column('group_id', db.Integer,
                                   db.ForeignKey('group_table.id'))
                         )


class Contact(db.Model):
    __tablename__ = 'contact_table'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_table.id'),
                        nullable=False)
    user = relationship('User', back_populates='contacts')
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    phones = relationship('Phone', back_populates='contact',
                          cascade="all, delete")
    emails = relationship('Email', back_populates='contact',
                          cascade="all, delete")
    adress = db.Column('address', db.String(100), nullable=True)
    birth = db.Column('birth', db.Date, nullable=True)
    groups = relationship('Group', secondary=contact_group, backref='contacts')

    def __repr__(self):
        return f"Contact({self.first_name} {self.last_name})"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Phone(db.Model):
    __tablename__ = 'phone_table'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column('phone', db.String(50), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact_table.id'),
                           nullable=False)
    contact = relationship('Contact', back_populates='phones')

    def __repr__(self):
        return f"Phone({self.phone})"

    def __str__(self):
        return f"{self.phone}"


class Email(db.Model):
    __tablename__ = 'email_table'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column('email', db.String(50), nullable=False)
    contact_id = db.Column('contact_id', db.ForeignKey('contact_table.id'),
                           nullable=False)
    contact = relationship('Contact', back_populates='emails')

    def __repr__(self):
        return f"Email({self.email})"

    def __str__(self):
        return f"{self.email}"


class Group(db.Model):
    __tablename__ = 'group_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"Group({self.name})"

    def __str__(self):
        return f"{self.name}"


class Note(db.Model):
    __tablename__ = 'note_table'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    text = db.Column(db.String(1200), nullable=False)

