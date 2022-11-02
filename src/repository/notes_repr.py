from sqlalchemy.orm import joinedload
from src import db
from src.models import Note, Tag
from typing import List


def get_notes(user_id: int, page: int = 1) -> List[Note]:
    """Return all notes by user name without loading joined information"""

    notes = db.session.query(Note).filter(user_id == user_id). \
        paginate(page=page, per_page=16)
    return notes


def get_note_by_id(note_id: int) -> Note:
    """Return note by id with loading joined information"""
    note = db.session.query(Note).get(note_id)

    return note


def get_notes_by_tag(user_id: int, tag_name: List[str], page: int = 1) -> List[Note]:
    """Return notes by tag with loading joined information"""
    notes = db.session.query(Note). \
        join(Tag, Note.tags). \
        filter(user_id == user_id, Tag.name.in_(tag_name)). \
        paginate(page=page, per_page=16)
    return notes


def get_tags() -> List[Tag]:
    """Return all tags without loading joined information"""
    tags = db.session.query(Tag).all()
    return tags


def get_tag_by_name(tag_name: str):
    """Return tag by name without loading joined information"""
    tag = db.session.query(Tag).filter(Tag.name == tag_name).one()
    return tag


def create_joined_tags(note_id: int, **kwargs):
    """Creates new Association object in current session
        which join to inputted contact """
    for tag in kwargs['tags']:
        note = get_note_by_id(note_id)
        note.tags.append(tag)
        db.session.commit()


def create_note(**kwargs) -> Note:
    """Creates new Note object and joined objects"""
    note = Note(
        user_id=kwargs['user_id'],
        title=kwargs['title'],
        text=kwargs['text'])

    db.session.add(note)
    db.session.commit()

    if kwargs.get('tags'):
        create_joined_tags(note.id, **kwargs)

    db.session.refresh(note)
    return note


def add_tag(name: str) -> Tag:
    """Create new Tag object"""
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    db.session.close()
    return tag
