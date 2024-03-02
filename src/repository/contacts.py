from datetime import datetime, timedelta
from typing import List, Type

from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.database.models import Contact
from src.schemas import ContactCreate, ContactUpdate


async def get_contacts(
        skip: int, limit: int, db: Session
) -> list[Type[Contact]]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactCreate, db: Session) -> Contact:
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        for field, value in body.dict().items():
            setattr(contact, field, value)
        db.commit()
    return contact


async def search_contacts(
    db: Session, first_name: str = "", last_name: str = "", email: str = ""
) -> list[Type[Contact]]:
    return db.query(Contact).filter(
        and_(
            Contact.first_name.ilike(f"%{first_name}%"),
            Contact.last_name.ilike(f"%{last_name}%"),
            Contact.email.ilike(f"%{email}%"),
        )
    ).all()


async def get_contacts_upcoming_birthdays(db: Session) -> list[Type[Contact]]:
    today = datetime.now().date()
    next_week = today + timedelta(days=7)

    return db.query(Contact).filter(
        and_(
            Contact.birthday.isnot(None),
            func.date_part(
                'month', Contact.birthday
            ) == func.date_part('month', today),
            func.date_part(
                'day', Contact.birthday
            ) >= func.date_part('day', today),
            func.date_part(
                'day', Contact.birthday
            ) <= func.date_part('day', next_week),
        )
    ).all()
