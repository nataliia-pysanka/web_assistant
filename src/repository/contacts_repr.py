from src import db
from src.models import Contact, Phone, Email, Group
from typing import List


def get_contacts(user_id: int,
                 page: int = 1) -> List[Contact]:
    """Return all contacts by user name without loading joined information"""

    contacts = db.session.query(Contact).filter(user_id == user_id). \
        paginate(page=page, per_page=16)
    return contacts


def get_contact_by_id(contact_id: int) -> Contact:
    """Return contact by id with loading joined information"""
    contact = db.session.query(Contact).get(contact_id)
    return contact


def get_groups() -> List[Group]:
    """Return all groups without loading joined information"""
    groups = db.session.query(Group).all()
    return groups


def get_group_by_name(group_name: str):
    """Return group by name without loading joined information"""
    group = db.session.query(Group).filter(Group.name == group_name).one()
    return group


def create_joined_phones(contact: Contact, phones):
    """Creates new Phone object in current session
    which join to inputted contact """
    for phone in phones:
        contact.phones.append(Phone(phone=phone))
        db.session.commit()


def create_joined_emails(contact: Contact, emails):
    """Creates new Email object in current session
        which join to inputted contact """
    for email in emails:
        contact.emails.append(Email(email=email))
        db.session.commit()


def create_joined_groups(contact_id: int, groups):
    """Creates new Association object in current session
        which join to inputted contact """
    for group in groups:
        contact = get_contact_by_id(contact_id)
        contact.groups.append(group)
        db.session.commit()


def create_contact(**kwargs) -> Contact:
    """Creates new Contact object and joined objects"""
    data = {}
    for key, item in kwargs.items():
        if key not in ['phones', 'emails', 'groups']:
            data.update({key: item})

    contact = Contact(**data)

    db.session.add(contact)
    db.session.commit()

    if kwargs.get('phones'):
        create_joined_phones(contact, kwargs['phones'])
    if kwargs.get('emails'):
        create_joined_emails(contact, kwargs['emails'])
    if kwargs.get('groups'):
        create_joined_groups(contact.id, kwargs['groups'])

    db.session.refresh(contact)
    return contact


def add_group(name: str) -> Group:
    """Create new Group object"""
    group = Group(name=name)
    db.session.add(group)
    db.session.commit()
    db.session.close()
    return group
