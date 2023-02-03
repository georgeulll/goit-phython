from fields_for_record import Name, Birthday, Phone, Email, Note, Tag
from datetime import datetime
from copy import copy
from termcolor import colored


class Record:

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.emails = []
        self.tag = None
        self.note = None

    def add_phone(self, phone) -> str:
        '''Adds a phone to the contact's list of phones.'''
        added_phone = Phone(phone)
        self.phones.append(added_phone)
        # f"The phone '{added_phone.value}' was added to the '{self.name.value.title()}'."
        return colored(f"The phone '{added_phone.value}' was added to the '{self.name.value.title()}'.", "green")

    def change_phone(self, new_phone) -> str:
        '''Changes an existing phone.'''
        if self.phones:
            new_phone = Phone(new_phone)
            phones = [phone.value for phone in self.phones]
            showing = dict(enumerate(phones, 1))

            while True:

                try:
                    message = colored("What phone you want to change?", "blue")
                    print(f"{message} {showing}")
                    choosing = input(
                        colored("Choose ¹ of this phone (press Enter to skip)>>> ", "magenta"))

                    if not choosing:
                        return colored(f"You didn't change any phone in your list: {self.name.value.title()}.", "yellow")
                    choosing = int(choosing)

                    if choosing > 0:
                        self.phones[choosing-1] = new_phone
                        return colored(f"Phone '{showing[choosing]}' of '{self.name.value.title()}' changed to '{new_phone.value}'.", "green")
                    else:
                        raise KeyError

                except ValueError:
                    return colored(f"{choosing} is not a number!", "red")
                except KeyError:
                    return colored(f"{choosing} is out of range!", "red")
                except IndexError:
                    return colored(f"{choosing} is out of range!", "red")

        else:
            raise ValueError(
                colored(f"Phone list of '{self.name.value.title()}' is empty"), "red")

    def delete_phone(self) -> str:
        '''Deletes an existing phone.'''
        if self.phones:
            phones = [phone.value for phone in self.phones]
            showing = dict(enumerate(phones, 1))

            while True:

                try:
                    message = colored("What phone you want to remove?", "blue")
                    print(f"{message} {showing}")
                    choosing = input(
                        colored("Choose ¹ of this phone (press Enter to skip)>>> ", "magenta"))

                    if not choosing:
                        return colored("You didn't remove any phone of '{self.name.value.title()}'.", "yellow")
                    choosing = int(choosing)
                    if choosing > 0:
                        self.phones.pop(choosing-1)
                        return colored(f"Phone '{showing[choosing]}' of '{self.name.value.title()}' removed.", "green")
                    else:
                        raise KeyError

                except ValueError:
                    return colored(f"{choosing} is not a number!", "red")
                except KeyError:
                    return colored(f"{choosing} is out of range!", "red")
                except IndexError:
                    return colored(f"{choosing} is out of range!", "red")

        else:
            raise ValueError(
                colored(f"Phones list of '{self.name.value.title()}' is empty."), "red")

    def add_mail(self, mail) -> str:
        '''Add an email to the contact.'''
        added_email = Email(mail)
        self.emails.append(added_email)
        return colored(f"The email '{added_email.value}' was added to '{self.name.value.title()}'.", "green")

    def change_mail(self, new_mail) -> str:
        '''Changes the phone.'''
        if self.emails:
            new_mail = Email(new_mail)
            emails = [email.value for email in self.emails]
            showing = dict(enumerate(emails, 1))

            while True:

                try:
                    message = colored("What email you want to change?", "blue")
                    print(f"{message} {showing}")
                    choosing = input(
                        colored("Choose ¹ of this email (press Enter to skip)>>> ", "magenta"))

                    if not choosing:
                        return colored(f"You didn't change any email of '{self.name.value.title()}'.", "yellow")
                    choosing = int(choosing)

                    if choosing > 0:
                        self.emails[choosing-1] = new_mail
                        return colored(f"Email < {showing[choosing]} > of < {self.name.value.title()} > changed to the < {new_mail.value} >", "green")
                    else:
                        raise KeyError

                except ValueError:
                    return colored(f"{choosing} is not a number!", "red")
                except KeyError:
                    return colored(f"{choosing} is out of range!", "red")
                except IndexError:
                    return colored(f"{choosing} is out of range!", "red")

        else:
            raise ValueError(
                colored(f"Emails list of '{self.name.value.title()}' is empty."), "red")

    def delete_mail(self) -> str:
        '''Removes an email.'''
        if self.emails:
            emails = [email.value for email in self.emails]
            showing = dict(enumerate(emails, 1))

            while True:

                try:
                    message = colored("What email you want to remove?", "blue")
                    print(f"{message} {showing}")
                    choosing = input(
                        colored("Choose ¹ of this email (press Enter to skip)>>> ", "magenta"))

                    if not choosing:
                        return colored(f"You didn't remove any email of '{self.name.value.title()}'.", "yellow")
                    choosing = int(choosing)

                    if choosing > 0:
                        self.emails.pop(choosing-1)
                        return colored(f"Email '{showing[choosing]}' of '{self.name.value.title()}' removed.", "green")
                    else:
                        raise KeyError

                except ValueError:
                    return colored(f"{choosing} is not a number!", "red")
                except KeyError:
                    return colored(f"{choosing} is out of range!", "red")
                except IndexError:
                    return colored(f"{choosing} is out of range!", "red")

        else:
            raise ValueError(
                colored(f"Emails list of '{self.name.value.title()}' is empty."), "red")

    def add_note(self, list_note) -> str:
        '''Add only one note at all.'''
        if not self.note:
            note = ""
            for item in list_note:
                note += f"{item} "
            self.note = Note(note)
        else:
            return colored(f"The note exists. Enter the command 'edit note' to change it.", "yellow")

        return colored(f"The note '{note[:-1]}' was added to the contact '{self.name.value.title()}'.", "green")

    def change_note(self, list_new_note) -> str:
        '''Corrects the note.'''
        new_note = ""
        if not self.note:
            return self.add_note(list_new_note)
        for item in list_new_note:
            new_note += f"{item} "
        old_note = self.note.value
        note = old_note + new_note
        self.note = Note(note)

        return colored(f"The note '{new_note[:-1]}' was added to the contact '{self.name.value.title()}'.", "green")

    def delete_note(self) -> str:
        '''Deletes the note.'''
        deleted_note = self.note.value
        self.note = None
        return colored(f"The note '{deleted_note}' of contact '{self.name.value}' was deleted.", "green")

    def add_tag(self, list_tag) -> str:
        '''Creates and adds tags to the contact's list of tags.'''
        if not list_tag:
            return colored(f"There are no tags in the input, please type again", "yellow")
        elif not self.tag:
            tag_list2 = []
            for tag in list_tag:
                tag_list2.append(tag)
            self.tag = Tag(tag_list2)
            return colored(f"The tag '{tag_list2}' was added to the contact '{self.name.value}'.", "green")
        else:
            return colored(
                f"If you want to add tags to an existing list of tags, "
                f"please choose 'edit tag' command.", "yellow"
            )

    def change_tag(self, new_tag_list):
        '''Adds new tags to the list.'''
        old_tag = self.tag

        if self.tag:
            self.tag = Tag(old_tag.value + new_tag_list)
            return colored(f"The new tag {new_tag_list} has been added to old one {old_tag.value}.", "green")

    def delete_tags(self) -> str:
        '''Deletes all tags.'''
        deleted_tag = self.tag
        self.tag = None
        return colored(f"The tag '{deleted_tag.value}' of contact '{self.name.value}' was deleted.", "green")

    def del_tag(self):
        '''Deletes only that tag which is chosen by a user.'''
        if self.tag:
            old_tags = copy(self.tag.value)
            tags = [tag for tag in self.tag.value]
            showing = dict(enumerate(tags, 1))

            while True:
                try:
                    message = colored(
                        "What tag do you want to remove?", "blue")
                    print(f"{message} {showing}")
                    choosing = input(
                        colored("Choose ¹ of this tags >>> ", "magenta"))

                    if not choosing:

                        message = colored(
                            "You didn't remove any tags of", "yellow")
                        return f"{message} '{self.tag.value}'"

                    choosing = int(choosing)

                    self.tag.value.pop(choosing - 1)
                    return colored(f"The tag '{showing[choosing]}' from '{old_tags}' was removed.", "green")
                except ValueError:
                    return colored(f"{choosing} is not a number!", "red")
                except KeyError:
                    return colored(f"{choosing} is out of range!", "red")
                except IndexError:
                    return colored(f"{choosing} is out of range!", "red")

        else:
            return colored(f"The list of tags '{self.tag}' is empty.", "yellow")

    def add_birthday(self, birthday) -> str:
        '''Adds a birthday.'''
        new_bday = Birthday(birthday)
        if new_bday.value > datetime.now():
            return f"This guy hasn't been born yet."
        self.birthday = new_bday
        return colored(f"Birthday was successfully added.", "green")

    def change_birthday(self, new_birthday) -> str:
        '''Changes a birthday.'''
        if self.birthday and Birthday(new_birthday).value < datetime.now():
            self.birthday = Birthday(new_birthday)
            return colored(f"Birthday has been changed successfully.", "green")
        else:
            return colored("The birthday hasn't been added yet for this contact. Add first.", "yellow")

    def days_to_birthdays(self):
        '''Returns a quantity of days until contact's birthday.'''
        if self.birthday:
            current_year = datetime.now().year
            current_day = datetime.now()
            this_year_birthday = datetime(
                year=current_year, month=self.birthday.value.month, day=self.birthday.value.day)
            if (this_year_birthday - current_day).days >= 0:
                next_birth = this_year_birthday - current_day
                return next_birth.days
            else:
                next_birth = datetime(
                    year=current_year + 1, month=self.birthday.value.month, day=self.birthday.value.day)
                return (next_birth - current_day).days
        else:
            return colored(f"The birthday hasn`t been added yet for this contact. Add first.", "yellow")

    def delete_birthday(self):
        '''Deletes a birthday.'''
        self.birthday = None
        return colored(f"The birhdays was deleted successfully.", "green")