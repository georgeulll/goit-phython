import datetime
import unittest
from unittest.mock import MagicMock


from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(
            id=1,
            username='User1',
            email='user1@gmail.com',
            password='qwerty',
            confirmed=True,
        )
        self.contact_test = Contact(
            id=1,
            first_name='Buster',
            last_name='Johns',
            email='buster@meta.ua',
            phone='+35428421424',
            date_of_birth=datetime.date(year=1985, month=10, day=8),
        )

    async def test_get_user_by_email(self):
        user = self.user
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertEqual(result, user)

    async def test_create_user(self):
        body = UserModel(
            username=self.user.username,
            email=self.user.email,
            password=self.user.password,
        )
        result = await create_user(body=body, db=self.session)

        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_confirmed_email(self):
        result = await confirmed_email(email=self.user.email, db=self.session)
        self.assertIsNone(result)

    async def test_update_token(self):
        user = self.user
        token = None
        result = await update_token(user=user, token=token, db=self.session)
        self.assertIsNone(result)

    async def update_avatar(self):
        url = 'https://res.cloudinary.com/web9storage/image/upload/c_fill,h_250,w_250/v1/Web9_FastapiAPP/Johny3'
        user = self.user
        result = await update_avatar(email=self.user.email, url=url, db=self.session)
        self.assertEqual(result, user)



if __name__ == '__main__':
    unittest.main()