from collections import UserDict
from record import Record
from datetime import datetime
from termcolor import colored
from print_table import header_func, line_func
import os
import pickle
from abc import ABC, abstractmethod


class AbstractAddressBook(ABC):
    @abstractmethod
    def add_record(self, record):
        pass

    @abstractmethod
    def delete_record(self, contact_name):
        pass


#AbstractBotName+UserInputBotName
class AbstractBotName(ABC):
    @abstractmethod
    def change_bot_name(self, new_name):
        pass


class UserInputBotName(AbstractBotName):
    def __init__(self):
        if os.path.exists("bot_name.bin") and os.path.getsize("bot_name.bin") > 0:
            with open("bot_name.bin", "rb") as b_name:
                self.bot_name = pickle.load(b_name)
        else:
            self.bot_name = "Jarvis"

    def change_bot_name(self, new_name: str) -> str:
        '''Changes the name of the bot.'''
        if new_name and new_name != self.bot_name:
            self.bot_name = new_name.title()
            with open("bot_name.bin", "wb") as file:
                pickle.dump(self.bot_name, file)
            return f"The bot's name was changed to {self.bot_name}."
        else:
            return f"Please enter the name or the bot already has this name."


# AbstractAddressBookSaver + ConcretSaver
class AbstractAddressBookSaving(ABC):
    @abstractmethod
    def save_address_book(self, addressbook):
        pass


class PickleAddressBookSaving(AbstractAddressBookSaving):
    def save_address_book(self, addressbook: AbstractAddressBook):
        '''Saves the address book.'''
        with open("address_book.bin", "wb") as file:
            pickle.dump(addressbook, file)


# AbstractAddressBookLoader + ConcretLoader
class AbstractAddressBookLoading(ABC):
    @abstractmethod
    def load_address_book(self):
        pass


class PickleAddressBookLoading(AbstractAddressBookLoading):
    def load_address_book(self):
        """Loads the address book."""
        try:
            with open("address_book.bin", "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            addressbook = UserAddressBook()
            return addressbook


class UserDictBook(AbstractAddressBook):
    def add_record(self, record):
        pass

    def delete_record(self, contact_name):
        pass


class UserAddressBook(UserDict, UserDictBook):
    def __init__(self):
        super().__init__()

    def add_record(self, record: Record) -> str:
        '''Adds name (key) of the contact and his fields (value).'''
        self.data[record.name.value] = record  # .title()
        return colored("New contact was added successfuly.", "green")

    def delete_record(self, contact_name: str) -> str:
        '''Deletes the contact (key).'''
        self.data.pop(contact_name)
        return colored("The contact was deleted successfully.", "green")

    def all_birthdays(self, range_days) -> list:
        '''Returns the list of all b-days in the next N-days.'''
        list_accounts = []

        for record_elem in self.data.values():

            if record_elem.birthday:
                days_to_next_birthday = record_elem.days_to_birthdays()

                if days_to_next_birthday <= range_days:
                    current_year = datetime.now().year
                    current_day = datetime.now()
                    this_year_birthday = datetime(
                        year=current_year, month=record_elem.birthday.value.month, day=record_elem.birthday.value.day)

                    if (this_year_birthday - current_day).days >= 0:
                        next_birth = this_year_birthday - current_day
                        return next_birth.days
                    else:
                        next_birth = datetime(
                            year=current_year + 1, month=record_elem.birthday.value.month, day=record_elem.birthday.value.day)
                    data = [record_elem.name.value.title(
                    ), next_birth.strftime("%A %d %B %Y")]
                    list_accounts.append(data)

            else:
                continue

        return list_accounts


class AddressBookRun:
    def run(self):
            addressbook = PickleAddressBookLoading().load_address_book()
            return addressbook



address_book = AddressBookRun().run()