from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=list[ContactResponse],
            name='Get all contacts or Get by first_name, last_name, or email')
async def get_contact_by_name(skip: int = 0, limit: int = Query(default=10, ge=1, le=50),
                              first_name: Optional[str] = Query(default=None),
                              last_name: Optional[str] = Query(default=None),
                              email: Optional[str] = Query(default=None),
                              db: Session = Depends(get_db),
                              current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contacts(skip, limit,
                                                     first_name, last_name,
                                                     email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/birthday", response_model=list[ContactResponse], name='Show contacts with birthday at the next 7 days')
async def get_birthday(skip: int = 0, limit: int = Query(default=10, ge=1, le=50), db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contact_birthday(skip, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, name='Get contact by ID')
async def get_contact(contact_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact_data = await repository_contacts.verify_email_phone(body.email, body.phone, db)
    if contact_data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email or phone is existed')

    return await repository_contacts.create_contact(body, db, current_user)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, db, current_user)
    if contact_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact