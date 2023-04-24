from typing import Optional

import redis

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import pickle

from src.database.db import get_db
from src.repository import users as repository_users
from src.conf.config import settings


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    SECRET_KEY = settings.secret_key_jwt
    ALGORITHM = settings.algorithm

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    r = redis.Redis(host=settings.redis_host,
                    port=settings.redis_port,
                    db=0)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    # define a function to generate a new access token
    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
    The create_access_token function creates a new access token for the user.
        The function takes in two arguments: data and expires_delta. Data is a dictionary that contains all of the information about the user, such as their username, email address, etc. Expires_delta is an optional argument that specifies how long you want your access token to be valid for (in minutes). If no value is specified then it defaults to 120 minutes (2 hours).
        The function first creates a copy of the data dictionary called to_encode and adds three additional key-value pairs: iat which stands for issued at time and represents when
    :param self: Refer to the current object
    :param data: dict: Pass the data that will be encoded in the token
    :param expires_delta: Optional[float]: Set the expiration time of the access token
    :return: A string that is the encoded access token
    :doc-author: Trelent
    """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(minutes=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=120)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    # define a function to generate a new refresh token
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
    The create_refresh_token function creates a refresh token for the user.
        Args:
            data (dict): A dictionary containing the user's id and username.
            expires_delta (Optional[float]): The number of seconds until the token expires, defaults to None.
    :param self: Represent the instance of the class
    :param data: dict: Pass in the user's information
    :param expires_delta: Optional[float]: Set the expiry time of the token
    :return: A refresh token that is encoded using the secret_key and algorithm
    :doc-author: Trelent
    """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
    The decode_refresh_token function is used to decode the refresh token.
    It takes a refresh_token as an argument and returns the email of the user if it's valid.
    If not, it raises an HTTPException with status code 401 (UNAUTHORIZED) and detail 'Could not validate credentials'.
    :param self: Represent the instance of a class
    :param refresh_token: str: Pass the refresh token to the function
    :return: The email of the user
    :doc-author: Trelent
    """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
    The get_current_user function is a dependency that will be used in the
        UserResource class. It takes an OAuth2 token as input and returns the user
        associated with that token. If no user is found, it raises an exception.
    :param self: Represent the instance of the class
    :param token: str: Get the token from the authorization header
    :param db: Session: Get the database session
    :return: A user object, which is used to identify the user
    :doc-author: Trelent
    """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        user = self.r.get(f"user:{email}")
        print(f'User get from Cashe')
        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            print(f'User get from Postgres_Db')
            if user is None:
                raise credentials_exception
            self.r.set(f"user:{email}", pickle.dumps(user))
            self.r.expire(f"user:{email}", 900)
        else:
            user = pickle.loads(user)
        return user

    def create_email_token(self, data: dict):
        """
    The create_email_token function takes a dictionary of data and returns a token.
    The token is created using the JWT library, which uses the SECRET_KEY and ALGORITHM to create an encoded string.
    The data dictionary contains information about the user's email address, as well as when it was issued (iat)
    and when it expires (exp). The iat and exp values are added to the data dict before encoding.
    :param self: Represent the instance of the class
    :param data: dict: Pass in the data that we want to encode
    :return: A token that is encoded with the user's email and a timestamp
    :doc-author: Trelent
    """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    async def get_email_from_token(self, token: str):
        """
    The get_email_from_token function takes a token as an argument and returns the email address associated with that token.
    The function uses the jwt library to decode the token, which is then used to return the email address.
    :param self: Represent the instance of the class
    :param token: str: Pass in the token that was sent to the user's email
    :return: The email address associated with the token
    :doc-author: Trelent
    """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")


auth_service = Auth()