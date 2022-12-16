from collections import UserDict


class AdressBook(UserDict):

    def change_contact_name(self, old_name, new_name: str):
        old = old_name.name.value
        self.data[new_name], self.data[old_name.name.value].name.value = self.data[old_name.name.value], new_name
        del self.data[old]
        return f"Имя {old} успешно изменено на {new_name}."

    def add_record(self, name):
        self.data[name] = Record(name)


class Record:

    def __init__(self, name, phone=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []

    def delete_phone(self, number):
        for values in self.phones:
            if values.value == number:
                self.phones.remove(values)
                return f"Номер телефона {number} удален для пользователя {self.name.value}."
        else:
            return f"Я не могу найти {number} у контакта {self.name.value}"

    def edit_phone(self, old_number, new_number):
        for values in self.phones:
            if values.value == old_number:
                values.value = new_number
                return f"Номер телефона {old_number} заменен на номер телефона {new_number} для пользователя {self.name.value}."
        else:
            return f"Я не могу найти {old_number} у контакта {self.name.value}"

    def add_phone(self, number):
        self.phones.append(Phone(number))
        return f"Номер телефона {number} добавлен к пользователю {self.name.value}."


class Field:
    def __init__(self, name):
        self.value = name


class Name(Field):
    pass


class Phone(Field):
    pass
stas = Record("Stas", phone=8050)
print(stas.phones)