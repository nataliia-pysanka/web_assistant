from sqlalchemy.orm import joinedload
from src import db
from src.models import Contact, Note
from typing import List
from src.repository.contacts_repr import get_contact_by_id


def get_notes(user_id: int,
              page: int = 1) -> List[Note]:
    """Return all notes by user name without loading joined information"""

    notes = db.session.query(Note).filter(user_id == user_id). \
        paginate(page=page, per_page=16)
    return notes


def get_note_by_id(contact_id: int) -> Note:
    """Return note by id with loading joined information"""
    note = db.session.query(Contact).filter(Contact.id == contact_id). \
        options(joinedload('tags')).one()
    return note


def get_tags() -> List[Tag]:
    """Return all tags without loading joined information"""
    tags = db.session.query(Tag).all()
    return tags


def get_tag_by_name(tag_name: str):
    """Return tag by name without loading joined information"""
    tag = db.session.query(Tag).filter(Tag.name == tag_name).one()
    return tag


def create_joined_tags(contact_id: int, **kwargs):
    """Creates new Association object in current session
        which join to inputted contact """
    for tag in kwargs['tags']:
        contact = get_contact_by_id(contact_id)
        contact.groups.append(tag)
        db.session.commit()


def create_note(**kwargs) -> Note:
    """Creates new Note object and joined objects"""
    contact = Contact(
        user_id=kwargs['user_id'],
        first_name=kwargs['first_name'],
        last_name=kwargs['last_name'],
        adress=kwargs['adress'],
        birth=kwargs['birth'])

    db.session.add(contact)
    db.session.commit()

    if kwargs.get('tags'):
        create_joined_tags(contact.id, **kwargs)

    db.session.refresh(contact)
    return contact


def add_tag(name: str) -> Tag:
    """Create new Tag object"""
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    db.session.close()
    return tag
