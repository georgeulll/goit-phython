from contact_book_classes import AdressBook, Record


def input_error(func):
    def inner(*user_data):
        try:
            return func(*user_data)
        except IndexError:
            return "Получено недостаточно информации. Проверьте корректность ввода."
        # except KeyError:
        #     return f"KeyError. Данное значение или команда не найдены."
        except ValueError:
            return f"'{user_data[1]}' не является телефонным номером. Телефон может содержать только цифры."

    return inner


def main():
    print("Чтоб посмотреть команды введите 'help'")
    while True:

        user_text = input()
        command, user_data = refactor_user_text(user_text)

        if command not in commands:
            print(f"Неизвестная команда '{command}'")
            continue

        if command == "create":
            result = get_functional(command)(user_data)
            print(result)
            continue

        try:
            main_record = book[user_data[0]] if user_data else None
        except KeyError:
            print(f"Данный контакт {user_data[0]} не найден. Повторите ввод или создайте пользователя командой 'create X' где Х - имя контакта.")
            continue

        result = get_functional(command)(main_record, user_data)

        if result:
            if type(result) is list:
                print(*result, sep="\n")
            else:
                print(result)


@input_error
def get_functional(command: str):
    """Получение сигнатуры"""

    signature = commands[command]
    return signature


@input_error
def refactor_user_text(user_text: str) -> list:
    """Обработка введенного пользователем текста и разделение на понятные для программы части"""

    if not user_text:
        return ['', '']
    splited_text = user_text.split()

    if splited_text[0].lower() in ("show", "good", "delete"):
        return [" ".join(splited_text[:2]).lower(), splited_text[2:]]
    else:
        return [splited_text[0].lower(),  splited_text[1:]]


@input_error
def greeting(*_) -> str:
    return "Hello, my dear friend!\n" \
           "How can i help you?\n"


@input_error
def create_new_contact(user_info, *_):

    name = user_info[0]
    if name not in book:
        book.add_record(name)
        return f"Создан контакт {name}"
    else:
        return f"Контакт {name} уже существует."


@input_error
def edit_contact(old_name: Record, new_name):
    if old_name.name.value != new_name[1]:
        return book.change_contact_name(old_name, new_name[1])
    else:
        return f"Старое имя {old_name.name.value} такое же как то, на которое вы хотите изменить - {new_name[1]}"


@input_error
def delete_contact(main_record: Record, *_):
    del book[main_record.name.value]
    return f"Контакт {main_record.name.value} удален из телефонной книги "


@input_error
def add_number(main_record: Record, user_info: list):
    return main_record.add_phone(int(user_info[1]))


@input_error
def change_number(main_record: Record, user_info: list):
    return main_record.edit_phone(int(user_info[1]), int(user_info[2]))


@input_error
def delete_phone(main_record: Record, user_info: list):
    return main_record.delete_phone(int(user_info[1]))


@input_error
def show_phones(new_record: Record, *_) -> str:
    return f"{new_record.name.value} contact phone numbers are: {[v.value for v in new_record.phones]}"


@input_error
def show_all(*_):
    full_list = []
    for contact_name, numbers in book.items():
        full_list.append(f"{contact_name} содержит такие номера телефонов: {[v.value for v in numbers.phones]}")
    return full_list


@input_error
def go_away(*_):
    exit("Bye. See you soon.")


@input_error
def help_me(*_):
    return "Команды, которые вы можете использовать: (X / Y в указанных команда = место для ввода пользователя)\n" \
           "'hello': Скажи привет, мой дорогой.\n" \
           "'help': Список команд.\n" \
           "'create Х': Создает новый контакт Х.\n" \
           "'edit X Y': Изменить имя контакта X на Y.\n" \
           "'delete contact X': Удаляет из книги контакт Х.\n"\
           "'add X Y': Добавляет к записи контакта X номер телефона Y.\n"\
           "'change X Y V': Заменяет для пользователя X номер телефона Y на номер телефона V.\n"\
           "'delete phone Х Y': Удаляет для контакта X номер телефона Y.\n" \
           "'show phones X': Показывает все номера телефонов пользователя X.\n"\
           "'show all': Показывает всех пользователей что есть в записной книге и их номера телефонов.\n"\
           "'good bye/close/exit/.': Выход из программы.\n"


commands = {"hello": greeting,
            "help": help_me,
            "create": create_new_contact,
            "edit": edit_contact,
            "delete contact": delete_contact,
            "add": add_number,
            "change": change_number,
            "delete phone": delete_phone,
            "show phones": show_phones,
            "show all": show_all,
            "good bye": go_away,
            "close": go_away,
            "exit": go_away,
            ".": go_away
            }

if __name__ == "__main__":
    book = AdressBook()
    main()