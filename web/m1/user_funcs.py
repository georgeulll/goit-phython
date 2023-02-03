from __future__ import annotations
from record import Record
from sort import sort_files
from address_book2 import address_book, PickleAddressBookSaving,UserInputBotName, UserAddressBook
from termcolor import colored
from datetime import datetime
from VisualTable import TableDataVisualise,TableDataSearchIn
import os


def input_error(func) -> str:
    def inner(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        except KeyError:
            return colored("You forgot to enter the contact name.", "red")

        except ValueError as exception:
            if exception.args[0] == "Not enough values to unpack (expected 2, got 1).":
                return colored("Wrong format. Please enter: '{command} {name} {new_value}'.", "red")
            return exception.args[0]

        except IndexError:
            return colored("Wrong format. Please enter: '{command} {name} {value}'.", "red")

        except TypeError:
            return colored("Unknown command or parameters, please try again.", "red")

        except AttributeError:
            return colored("Can't find information about this contact or the data is incorrect.", "red")

        except StopIteration:
            return colored("There are no other numbers in the book.", "red")

    return inner


@input_error
def help_func(*_) -> str:

    options_bot_str = {

        "add Natally": "I will save the name.",
        "edit contact Natally": "I will correct the name of an existing contact.",
        "show all": "I will show the full list of all contacts.",
        "del contact Natally": "I will delete the contact.",

        "add phone Natally 096-45-34-876": "I will add phone a number to your address book.",
        "edit phone Natally 0986754325": "I will change your friend's phone number.",
        "phone Natally": "I will show your contact's phone, just enter the name.",
        "del phone Natally": "I will delete your contact's phone number.",

        "add mail Vasya vasiliy007@gmail.com": "I will add an email to your address book.",
        "edit mail Vasya new_mail_vasya@gmail.com": "I will change an email of one of your contacts.",
        "del mail Vasya": "I will delete an email of one of your contacts.",

        "add birth Natally 1999 12 23": "I will add the birthday of your friend.",
        "edit birth Natally 1999 12 23": "I will change your friend's date of birth.",
        "all births 50": "I will show the birthdays of all your friends in the next 50 days.",
        "days to birth Leo": "I will tell you the number of days until my friend's birthday.",
        "del birth Natally": "I will delete your contact's birthday.",

        "add note Natally str. Peremogy, house 76.": "I will add any note to the contact.",
        "edit note Natally str. Gagarina, h.126.": "I will add a new note to the existing note.",
        "del note Natally": "I will delete contact's notes.",

        "add tag Natally #address #favorite": "I will add tags.",
        "find tag #favorite": "I will show notes with such tags.",
        "edit tags Natally": "You can delete or add a new tag.",
        "del tags Natally": "I will deletenote's tags of your contact.",

        "help": "I will tell you about my possibilities.",
        "edit bot": "To change the name of the bot",
        "sort": "I will sort all the files in the folder you choose.",
        "find {example}": "I will find all records, which contain 'mi'",
        f"{EXIT_COMMANDS}": "Enter one of these words and I will finish my work.",

    }

    table_options_bot = ""
    header_table = "| {:<51} | {:<80}".format(
        "Example command", "Command description")
    header_table = colored(f"{header_table}", "blue", attrs=["bold"])
    table_options_bot += f"\n{header_table}\n\n"

    for key, value in options_bot_str.items():
        key = colored(f"{key}", "blue")
        row = "| {:<60} | {:<80}".format(key, value)
        table_options_bot += f"{row}\n"

    return table_options_bot


#@input_error
def add_func(args: list) -> str:                                    # AbstractAddressBook
    '''Adds a new contact'''
    record = Record(args[0])
    if record.name.value not in address_book.keys():
        return address_book.add_record(record)
    else:
        return colored(f"The contact with the name {args[0].title()} does not exist in your address book.", "yellow")


@input_error
def edit_contact_name_func(args: list) -> str:
    '''Edits the name of the existing contact.'''
    existing_name, corrected_name, *_ = args

    if not address_book:
        return colored(f"'{existing_name.title()}' wasn't found in your address book.", "yellow")
    for value in address_book.values():
        if existing_name in address_book.keys():
            value.name.value = corrected_name
            address_book[corrected_name] = address_book.pop(existing_name)
            return colored(f"'{existing_name.title()}' was changed to '{corrected_name.title()}'.", "green")
        else:
            return colored(f"'{existing_name.title()}' wasn't found in your address book.", "yellow")


@input_error
def delete_record_func(args: list) -> str:                          # AbstractAddressBook
    '''Deletes the contact including all his records.'''
    contact_name, *_ = args

    if contact_name in address_book.keys():
        return address_book.delete_record(contact_name)
    return colored(f"Name '{contact_name.title()}' doesn't exist in your address book.", "yellow")


@input_error
def add_phone_func(args: list) -> str:
    '''Adds a phone number to an existing contact.'''
    contact_name, phone, *_ = args

    if contact_name in address_book.keys() and phone not in [p.value for p in address_book[contact_name].phones]:
        return address_book[contact_name].add_phone(phone)
    elif contact_name in address_book.keys() and phone in [p.value for p in address_book[contact_name].phones]:
        return colored(f"The '{phone}' already exists in the list.", "yellow")
    else:
        return colored(f"There is no '{contact_name.title()}' in your address book.", "yellow")


@input_error
def change_phone_func(args: list) -> str:
    '''Changes the phone of the contact.'''
    name, new_phone, *_ = args
    record = address_book.data.get(name)
    return record.change_phone(new_phone)


@input_error
def phone_func(args: list) -> str:
    '''Returns the list of contact's phones.'''
    name, *_ = args
    record = address_book[name]

    if record:
        phones_list = [phone.value for phone in record.phones]
        return colored(f"{record.name.value.title()} has these phones {phones_list}", "green")
    return colored(f"I didn't find any '{name.title()}' in your Address Book.", "green")


@input_error
def del_phone_func(args: list) -> str:
    '''Deletes an existing phone.'''
    name, *_ = args
    record = address_book.data.get(name)
    return record.delete_phone()


@input_error
def add_mail_func(args: list) -> str:
    '''Adds an email to an existing contact.'''
    contact_name, email, *_ = args

    if contact_name in address_book.keys() and email not in [e.value for e in address_book[contact_name].emails]:
        return address_book[contact_name].add_mail(email)
    elif contact_name in address_book.keys() and email in [e.value for e in address_book[contact_name].emails]:
        return colored(f"The '{email}' already exists in the list.", "yellow")
    else:
        return colored(f"There is no '{contact_name.title()}' in your Address Book.", "yellow")


@input_error
def change_mail_func(args: list) -> str:
    '''Changes the email of the contact.'''
    name, new_mail, *_ = args
    record = address_book.data.get(name)
    return record.change_mail(new_mail)


@input_error
def delete_mail_func(args: list) -> str:
    '''Deletes an existing email.'''
    name, *_ = args
    record = address_book.data.get(name)
    return record.delete_mail()


@input_error
def show_all_func(*_) -> dict:
    '''Shows all contacts and their records.'''
    #return address_book.search_in_contact_book("")
    return TableDataVisualise().visualise(address_book)


@input_error
def add_birth_func(args: list) -> str:
    '''Adds a birthday to an existing contact.'''
    record = address_book[args[0]]
    years, months, days, *_ = args[1:]
    user_bday = datetime(year=int(years), month=int(months), day=int(days))

    if not record.birthday:
        return record.add_birthday(user_bday)
    else:
        return colored(f"The contact with the name {args[0].title()} does not exist in your address book.", "yellow")


@input_error
def change_birth_func(args: list) -> str:
    '''Changes the birthday of the contact.'''
    record = address_book[args[0]]
    years, months, days, *_ = args[1:]
    user_bday = datetime(year=int(years), month=int(months), day=int(days))

    if record.birthday:
        return record.change_birthday(user_bday)
    else:
        return colored(f"The contact with the name {args[0].title()} does not exist in your address book.", "yellow")


@input_error
def del_birth_func(args: list) -> str:
    '''Deletes the birthday of the contact.'''
    record = address_book[args[0]]

    if record.birthday:
        return record.delete_birthday()
    elif not record.birthday:
        return colored(f"The contact has no birthday information.", "yellow")
    else:
        return colored(f"The contact with the name {args[0].title()} does not exist in your address book.", "yellow")


@input_error
def days_to_birth_func(args: list) -> str:
    '''Returns a quantity of days until contact's birthday.'''
    record = address_book[args[0]]

    if record.birthday != None:
        return colored(f"{args[0].title()}'s birthday will be in {record.days_to_birthdays()} days.", "green")
    elif record.birthday == None:
        return colored(f"The contact has no birthday information.", "yellow")
    else:
        return colored(f"The contact with the name {args[0].title()} does not exist in your address book.", "yellow")


@input_error
def all_birth_func(args) -> str:
    '''Show contacts and their birthdays in the next N days.'''
    days = int(args[0])
    result = "\n"
    bdays = address_book.all_birthdays(days)

    if not bdays:
        return colored(f"There are no bdays in {days} days.", "yellow")

    for data in bdays:
        result += " - ".join(data)
        result += "\n"
    result = result[0:-1]

    return result


@input_error
def add_note_func(args: list) -> str:
    '''Creates a note.'''
    record = address_book[args[0]]
    return record.add_note(args[1:])


@input_error
def change_note_func(args: list) -> str:
    '''Changes and existing note.'''
    name, *new_note = args
    record = address_book.data.get(name)
    return record.change_note(new_note)


@input_error
def del_note_func(args: list) -> str:
    '''Deletes an existing note.'''
    name, *_ = args
    record = address_book.data.get(name)
    return record.delete_note()


@input_error
def add_tag_func(args: list) -> str:
    '''Creates a tag.'''
    record = address_book[args[0]]
    return record.add_tag(args[1:])


@input_error
def edit_tag_func(args: list) -> str:
    '''Corrects existing tag/tags.'''
    record = address_book[args[0]]

    if record.tag:

        while True:

            choices = ["1", "2", "3"]

            print(
                colored(f"The current list of tags is {record.tag.value}", "blue"))
            message = colored(
                "Please choose the way to edit tags:\n 1. Remove any tag\n 2. Add any tag\n 3. Exit\n >>> ", "magenta")

            act = input(message)

            if act not in choices:
                return colored("You have to choose '1', '2' or '3'.", "blue")

            act = int(act)

            if act == 1:
                res = record.del_tag()
                if res == 0:
                    break
                else:
                    continue
            elif act == 2:
                new_line_tag = input(colored(
                    "Please enter new space-separated tags, each of them must start with '#' ('#hello') >>> ", "blue"
                ))
                new_list_tag = new_line_tag.split(' ')
                record.change_tag(new_list_tag)
                continue
            elif act == 3:
                return f""
            else:
                print(colored("You entered a wrong number. Please try again.", "red"))
                continue
    else:
        return colored(f"The list of tags is empty, please fill it.", "yellow")


@input_error
def delete_tags_func(args: list) -> str:
    '''Deletes all user's tags.'''
    record = address_book.data.get(args[0])
    return record.delete_tags()


#@input_error
def find_func(args) -> str:
    '''Searches user input in the address book.'''
    #return address_book.search_in_contact_book(args)
    return TableDataSearchIn().search_in(address_book, args)

@input_error
def sort_func(*_) -> str:
    '''Sorts files in the folder.'''
    user_input = input(
        colored(
            "Enter '1' if you want to sort files in the current folder.\n"
            "Enter '2' if you want to choose another folder.\n", "blue")
    )

    if user_input == "1":
        return sort_files(os.getcwd())
    elif user_input == "2":
        user_path = input("Enter a path: ")
        return sort_files(user_path)
    else:
        return colored(f"You have to enter '1' or '2'.", "magenta")


@input_error
def edit_bot_name(args: list) -> str:                           # AbstractBotName
    '''Changes the name of the bot.'''
    new_bot_name, *_ = args
    return address_book.change_bot_name(new_bot_name)


@input_error
def exit_func(*_) -> str:
    """The function close bot."""
    return exit(colored("Bye! I'm gonna miss you ;)\n", "blue", attrs=["bold"]))


@input_error
def what_is_command(commands: list | dict, user_input: str) -> str:
    '''Checks user input.'''
    command_out = []
    user_input_list = user_input.split()

    if len(user_input_list) == 1:
        commands = ["help", "sort"]

    for j, command_in_one in enumerate(user_input_list):

        count = 0
        command_one_out = ""

        if len(user_input_list) < len(command_out) + 1:
            break

        for commands_str in commands:
            i = 0

            if " ".join(command_out) not in commands_str:
                continue

            if len(commands_str.split()) > j:
                command_one = commands_str.split()[j]
            else:
                continue

            for char_in, char_comm in zip(command_in_one, command_one):

                if char_in == char_comm:
                    i += 1

            if i > count:
                command_one_out = command_one
                count = i

        if command_one_out == "show":
            command_out = ["show all"]
            break

        elif command_one_out:
            command_out.append(command_one_out)

    if len(command_out) > 1 or command_out[0] == "add":
        data = user_input_list[len(command_out):]
    else:
        data = ""

    return " ".join(command_out), " ".join(data)


# Importantly! The more words in the bot command, the higher command is in the dictionary.
FUNCTIONS = {
    "days to birth": days_to_birth_func,
    "add phone": add_phone_func,
    "add mail": add_mail_func,
    "del contact": delete_record_func,
    "edit contact": edit_contact_name_func,
    "edit phone": change_phone_func,
    "edit mail": change_mail_func,
    "del phone": del_phone_func,
    "del mail": delete_mail_func,
    "show all": show_all_func,
    "add birth": add_birth_func,
    "del birth": del_birth_func,
    "edit birth": change_birth_func,
    "all births": all_birth_func,
    "add note": add_note_func,
    "edit note": change_note_func,
    "del note": del_note_func,
    "add tag": add_tag_func,
    "edit tag": edit_tag_func,
    "del tags": delete_tags_func,
    "edit bot": edit_bot_name,
    "add": add_func,
    "help": help_func,
    "sort": sort_func,
    "find": find_func,
    "phone": phone_func
}

EXIT_COMMANDS = ("good bye", "exit", "close", "quit", "bye", "q")


#@input_error
def handler(input_string: str) -> list:
    """
    The function separates the command word for the bot, and writes all other data into a list,
    where the first value is the name.
    """
    command = ""
    #perhaps_command = what_is_command(FUNCTIONS, input_string)
    data = ""
    input_string = input_string.strip().lower() + " "
    for key in FUNCTIONS:
        if input_string.startswith(key + " "):
            command = key
            data = input_string[len(command):].strip()
            break

    message_start = colored("If you mean", "cyan")
    message_end = colored("press enter: ", "cyan")

    if not command:

        command, data = what_is_command(FUNCTIONS, input_string)

        if input(f"{message_start} '{command} {data}' {message_end}") != "":
            command = ""
            data = ""

    if data:
        args = data.strip().split(" ")
        return FUNCTIONS[command](args)

    return FUNCTIONS[command]()