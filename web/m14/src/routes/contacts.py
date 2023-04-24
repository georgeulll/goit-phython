from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=list[ContactResponse], name='Get all contacts or Get by first_name, last_name, or email',
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact_by_name(skip: int = 0, limit: int = Query(default=10, ge=1, le=50),
                              first_name: Optional[str] = Query(default=None),
                              last_name: Optional[str] = Query(default=None),
                              email: Optional[str] = Query(default=None),
                              db: Session = Depends(get_db),
                              current_user: User = Depends(auth_service.get_current_user)):
    """
The get_contact_by_name function is used to retrieve a contact by name.
    The function takes in the following parameters:
        skip (int): The number of contacts to skip before returning results. Default value is 0.
        limit (int): The maximum number of contacts to return per request. Default value is 10, with a minimum of 1 and maximum of 50 allowed values for this parameter.
        first_name (str): A string containing the first name associated with the contact being searched for in the database, if any exists; default value None means that no search will be performed on this field when searching for a contact record in the
:param skip: int: Skip a number of records
:param limit: int: Limit the number of results returned
:param ge: Set the minimum value for a parameter
:param le: Limit the number of results returned by the query
:param first_name: Optional[str]: Specify that the first_name parameter is optional
:param last_name: Optional[str]: Filter the results by last name
:param email: Optional[str]: Filter the contacts by email
:param db: Session: Pass the database session to the function
:param current_user: User: Get the current user from the database
:return: A contact by name
:doc-author: Trelent
"""
    contact = await repository_contacts.get_contacts(skip, limit,
                                                     first_name, last_name,
                                                     email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/birthday", response_model=list[ContactResponse], name='Show contacts with birthday at the next 7 days')
async def get_birthday(skip: int = 0, limit: int = Query(default=10, ge=1, le=50), db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
The get_birthday function returns a list of contacts with birthdays in the current month.
:param skip: int: Skip the first n records in a query
:param limit: int: Limit the number of contacts returned
:param ge: Set a minimum value for the limit parameter
:param le: Limit the number of results returned
:param db: Session: Get the database session
:param current_user: User: Get the user who is currently logged in
:return: A list of contacts with the same birthday as the current user
:doc-author: Trelent
"""
    contacts = await repository_contacts.get_contact_birthday(skip, limit, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, name='Get contact by ID')
async def get_contact(contact_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
The get_contact function is a GET request that returns the contact with the given ID.
If no such contact exists, it raises an HTTP 404 error.
:param contact_id: int: Get the contact id from the path
:param db: Session: Get a database session
:param current_user: User: Get the current user from the database
:return: A contact object
:doc-author: Trelent
"""
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, description='No more than 10 requests per minute',
             dependencies=[Depends(RateLimiter(times=10, seconds=60))], status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
The create_contact function creates a new contact in the database.
    It takes an email, phone and name as input parameters.
    The function returns the newly created contact object.
:param body: ContactModel: Validate the data that is sent in the request body
:param db: Session: Pass the database connection to the function
:param current_user: User: Get the current user
:return: A contactmodel object
:doc-author: Trelent
"""
    contact_data = await repository_contacts.verify_email_phone(body.email, body.phone, db)
    if contact_data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email or phone is existed')

    return await repository_contacts.create_contact(body, db, current_user)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
The update_contact function updates a contact in the database.
    The function takes three arguments:
        - body: A ContactModel object containing the new values for the contact.
        - contact_id: An integer representing the ID of an existing contact to be updated.
        - db (optional): A Session object used to connect to and query a database, if not provided, one will be created automatically using get_db().
:param body: ContactModel: Pass the contact information to be updated
:param contact_id: int: Identify the contact we want to delete
:param db: Session: Pass the database session to the repository layer
:param current_user: User: Get the user_id from the jwt token
:return: A contactmodel object
:doc-author: Trelent
"""
    contact = await repository_contacts.update_contact(contact_id, body, db, current_user)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    """
The remove_contact function removes a contact from the database.
    Args:
        contact_id (int): The id of the contact to be removed.
        db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
        current_user (User, optional): User object for authentication and authorization purposes. Defaults to Depends(auth_service.get_current_user).
:param contact_id: int: Specify the contact to be removed
:param db: Session: Pass the database session to the repository
:param current_user: User: Get the current user from the database
:return: The contact that was removed
:doc-author: Trelent
"""
    contact = await repository_contacts.remove_contact(contact_id, db, current_user)
    if contact_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact