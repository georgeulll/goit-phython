from classe_for_bot import AdressBook, Record


def input_error(func):
    def inner(*user_data):
        try:
            return func(*user_data)
        except IndexError:
            return "Получено недостаточно информации. Проверьте корректность ввода."
        except ValueError as exception:
            return exception.args[0]

    return inner


def main():
    print("Чтоб посмотреть команды введите 'help'")
    while True:

        user_text = input()
        command, user_data = refactor_user_text(user_text)

        if command not in commands:
            print(f"Неизвестная команда '{command}'")
            continue

        if command in ("create", "show pages", "search"):
            result = get_functional(command)(user_data)
            print_results(result)
            continue

        try:
            main_record = book[user_data[0]] if user_data else None
        except KeyError:
            print(f"Данный контакт {user_data[0]} не найден. Повторите ввод или создайте пользователя командой 'create X' где Х - имя контакта.")
            continue

        result = get_functional(command)(main_record, user_data)

        print_results(result)


def print_results(result):
    if result:
        if isinstance(result, list):
            print(*result, sep="\n")
        elif isinstance(result, dict):
            for k, v in result.items():
                print(k)
                for record in v:
                    print(record)
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

    name = ' '.join(user_info)
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
    return main_record.add_phone(user_info[1])


@input_error
def change_number(main_record: Record, user_info: list):
    return main_record.edit_phone(user_info[1], user_info[2])


@input_error
def delete_phone(main_record: Record, user_info: list):
    return main_record.delete_phone(user_info[1])


@input_error
def show_phones(main_record: Record, *_) -> str:
    return f"{main_record.name.value} contact phone numbers are: {[v.value for v in main_record.phones]}"


@input_error
def set_birthday(main_record: Record, user_info: list):
    return main_record.set_birthday(user_info[1])


@input_error
def show_birthday(main_record: Record, *_):
    return f"День рождения пользователя {main_record.name.value} - {main_record.birthday.value}."


@input_error
def birthday_difference(main_record: Record, *_):
    return f"До дня рождения контакта {main_record.name.value} осталось {main_record.days_to_birthday()} дней."

@input_error
def show_pages(n, *_):

    page, result = 1, {}

    try:
        cnt = int(n[0]) if n else 5
    except ValueError:
        raise ValueError(f"{n[0]} is not a number.")

    for page_set in book.iterator(count=cnt):
        for record in page_set:
            result.setdefault(f"Page {page}", []).append(f"\tName: {record.name.value}. Phones: {[i.value for i in record.phones]}. Birthday:"
                                                        f" {record.birthday.value if record.birthday else None}")
        page += 1
    return result

@input_error
def search(value, *_):
    return book.search_in_contact_book(value[0])

@input_error
def show_all(*_):
    full_list = []
    for contact_name, numbers in book.items():
        full_list.append(f"{contact_name} содержит такие номера телефонов: {[v.value for v in numbers.phones]}")
    return full_list

@input_error
def save_contact_book(*_):
    sure = input("Осторожно. Все внесенные изменения будут сохранены и перезаписаны. Вы уверены? Y/N : ")
    if sure == "Y":
        return book.save_to_file()
    else:
        return f"Вы ввели {sure}. Сохранение отменено."


@input_error
def load_contact_book(*_):
    sure = input("Осторожно. Все не сохраненные данные будут утеряны. Вы уверены? Y/N : ")
    if sure == "Y":
        return book.load_from_file()
    else:
        return f"Вы ввели {sure}. Загрузка отменена."

@input_error
def go_away(*_):
    book.save_to_file()
    exit("Контактная книга успешно сохранена. До встречи.")


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
           "'show all': Показывает всех пользователей что есть в записной книге и их номера телефонов.\n" \
           "'show pages X': Показывает все контакты содержащиеся в книге по X записей на странице (не обязательно для указания, по умолчанию X = 5. \n" \
           "'birthday X Y': Указывает для контакта Х день рождения Y в формате гггг.мм.дд\n" \
           "'show birthday X': Показывает дату рождения для контакта Х. \n" \
           "'difference X': Показывает сколько дней осталось до ближайшего дня рождения контакта Х.\n" \
           "'show birthday X': Выводит данные о дне рождения для контакта X.\n" \
           "'save': Сохраняет контактную книгу.\n"\
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
            "show pages": show_pages,
            "search": search,
            "birthday": set_birthday,
            "show birthday": show_birthday,
            "difference": birthday_difference,
            "save": save_contact_book,
            "load": load_contact_book,
            "good bye": go_away,
            "close": go_away,
            "exit": go_away,
            ".": go_away
            }

if __name__ == "__main__":
    book = AdressBook()
    try:
        book.load_from_file()
        print("Контактная книга успешно загружена.")
    except FileNotFoundError:
        print("Файл сохранения адресной книги не найден. Файл будет создан. Будет создана новая контактная книга.")


    main()