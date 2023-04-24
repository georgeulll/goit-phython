from typing import List
from datetime import date, timedelta
from sqlalchemy import or_, and_

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contact_by_id(contact_id: int, db: Session):
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def get_contacts(skip: int,
                       limit: int,
                       first_name: str,
                       last_name: str,
                       email: str,
                       db: Session):

    if first_name:
        if last_name or email:
            return db.query(Contact).select_from(Contact)\
                              .filter(Contact.first_name == first_name,
                                      or_(Contact.last_name == last_name, Contact.email == email)).all()
        else:
            return db.query(Contact).filter(Contact.first_name == first_name).all()

    if last_name:
        if email:
            return db.query(Contact).select_from(Contact) \
                .filter(Contact.last_name == last_name, Contact.email == email).all()
        else:
            return db.query(Contact).filter(Contact.last_name == last_name).all()

    if email:
        return db.query(Contact).filter(Contact.email == email).all()

    return db.query(Contact).offset(skip).limit(limit).all()


async def verify_email_phone(email: str, phone: str, db: Session):
    email_data = db.query(Contact.email).filter(Contact.email == email).first()
    if email_data:
        return email_data

    phone_data = db.query(Contact.phone).filter(Contact.phone == phone).first()
    if phone_data:
        return phone_data

    return None


async def get_contact_birthday(skip: int,
                               limit: int, db: Session):
    contacts_with_next_birth = []
    today = date.today()
    all_contacts = db.query(Contact).offset(skip).limit(limit).all()
    for contact in all_contacts:
        if contact.date_of_birth.month == today.month:
            if 0 <= (contact.date_of_birth.day - today.day) <= 7:
                contacts_with_next_birth.append(contact)
        else:
            continue
    return contacts_with_next_birth


async def create_contact(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactModel, db: Session):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.date_of_birth = body.date_of_birth
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact