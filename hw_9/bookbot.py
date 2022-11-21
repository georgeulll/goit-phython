phone_book = {
    "Nikolai": "+380667777777",
    "Elena": "+380687777777",
    "Natasha": "+380637777777"
}


def input_error(func):  # decorator @input_error
    def inner_function(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except KeyError as e:
            result = f"Name {e} not found."
        except IndexError:
            result = "Phone number not entered."
        except TypeError:
            result = "Phone number not entered."
        finally:
            return result

    return inner_function


@input_error
def add_handler(user_input):
    if len(user_input) >= 2:
        phone_book.update({str(user_input[0]).title(): user_input[1]})
    print(phone_book)
    return f"{str(user_input[0]).title()}: {user_input[1]} succesfully added"


@input_error
def change_handler(user_input):
    if len(user_input) >= 2:
        phone_book.update({str(user_input[0]).title(): user_input[1]})
    print(phone_book)
    return f"{str(user_input[0]).title()}: {user_input[1]} succesfully changed"


def exit_handler(user_input):
    print("Good bye!")
    exit()


def error_handler(user_input):
    return 'Command not found. Enter "help" for view command list.'


def hello_handler(user_input):
    return 'How can I help you?'


def help_hendler(user_input):
    text = """ 
    "add" - add name(one word) and phone(digit): "add Vasya +380967777777"
    "close", "exit", "good bye" - close app
    "change" - change phone if name exists: "change Vasya +380967777777"
    "hello" -  print How can I help you?: "hello"
    "help": print help list: "help"
    "phone" - print phone of name: "phone Vasya"
    "show all" - print names and phones: "show all" """
    return text


def input_parser():
    input_list = []
    user_input = str(input("Enter: ")).lower()
    if not user_input.find(".") == -1:
        exit()
    else:
        user_input = user_input.strip()
        input_list = user_input.split(" ")

        if len(input_list) >= 2:

            if input_list[0] == "good" and input_list[1] == "bye":
                input_list[0] = input_list[0] + " " + input_list.pop(1)

            if input_list[0] == "show" and input_list[1] == "all":
                input_list[0] = input_list[0] + " " + input_list.pop(1)

        return input_list


@input_error
def phone_handler(user_input):
    if len(user_input):
        return f"{phone_book[str(user_input[0]).title()]}"
    else:
        raise KeyError


def show_handler(user_input):
    phone_book_list = []
    for item in phone_book:
        phone_book_list.append(f"{item}: {phone_book[item]}")
    return "\n".join(phone_book_list)


HENDLER_DICT = {
    "add": add_handler,
    "change": change_handler,
    "close": exit_handler,
    "exit": exit_handler,
    "good bye": exit_handler,
    "hello": hello_handler,
    "help": help_hendler,
    "phone": phone_handler,
    "show all": show_handler
}


def get_handler(operator):
    return HENDLER_DICT.get(operator, error_handler)


def main():
    while True:
        user_input = input_parser()

        print(get_handler(user_input[0])(user_input[1:]))


if __name__ == '__main__':
    main()