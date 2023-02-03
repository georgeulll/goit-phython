
from datetime import datetime
from termcolor import colored
import re


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        fixed_phone = self._sanitize_phone_number(value)

        if len(fixed_phone) < 10 or len(fixed_phone) > 12:
            raise ValueError(
                colored("Wrong format of phone, must be 10 or 12 numbers.", "red"))
        if not fixed_phone.isnumeric():
            raise ValueError(
                colored("Wrong format of phone, must be only numbers.", "red"))
        self._value = fixed_phone

    def _sanitize_phone_number(self, phone):
        new_phone = (
            phone.strip()
            .replace("+", "")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        return new_phone


class Email(Field):

    @Field.value.setter
    def value(self, email: str):
        new_email = re.search(
            r'[a-zA-Z]+[\w.]+[@][a-zA-Z]+[.][a-zA-Z]{2,}', email)

        if not new_email:
            raise ValueError(colored(f"Email {email} is not valid.", "red"))
        self._value = new_email.group()


class Note(Field):
    pass


class Tag(Field):
    @Field.value.setter
    def value(self, value):
        for tag in value:
            if not isinstance(tag, str):
                raise ValueError(colored(f"The tag shall be string", "red"))
            if not tag.startswith("#"):
                raise ValueError(colored(f"The tag must start #", "red"))
        self._value = value


class Birthday(Field):

    @Field.value.setter
    def value(self, birthday: datetime):
        if isinstance(birthday, datetime):
            self._value = birthday
        else:
            return f"{birthday} is not a birthday. Check it."
