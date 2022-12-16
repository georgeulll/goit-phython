from collections import UserDict
from datetime import date


class AdressBook(UserDict):

    def change_contact_name(self, old_name, new_name: str):
        old = old_name.name.value
        self.data[new_name], self.data[old_name.name.value].name.value = self.data[old_name.name.value], new_name
        del self.data[old]
        return f"Имя {old} успешно изменено на {new_name}."

    def add_record(self, name):
        self.data[name] = Record(name)

    def iterator(self, count):
        page = []
        i = 0

        for record in self.data.values():
            page.append(record)
            i += 1

            if i == count:
                yield page
                page = []
                i = 0

        if page:
            yield page


class Record:
    """Класс, в котором хранится весь контакт - список номеров, дата рождения, имя. Имя при создании объекта обязательно. Номера телефонов - список объектов
    класса Record. День рождения только в одном экземпляре, не обязателен для ввода, по умолчанию None."""

    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)] if phone else []
        self.birthday = Birthday(birthday) if birthday else None

    def delete_phone(self, number):
        """Вносит изменения в класс, удаляет запись Рекорд, содержащую конкретный номер. Возвращает ответ об успешности/ошибке операции."""
        try:
            number = int(number)
        except ValueError:
            return f"Номер телефона {number} состоит не только из цифр."
        for phone in self.phones:
            if phone.value == number:
                self.phones.remove(phone)
                return f"Номер телефона {number} удален для пользователя {self.name.value}."
        return f"Я не могу найти {number} у контакта {self.name.value}."

    def edit_phone(self, old_number, new_number):
        """Вносит изменения в класс, изменяет у записи Рекорд, содержащую конкретный номер на новый. Так же проверяет на интование."""

        try:
            old_number, b = int(old_number), int(new_number)
        except ValueError:
            return f"Один из номеров телефона {old_number, new_number} состоит не только из цифр."
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                return f"Номер телефона {old_number} заменен на номер телефона {new_number} для пользователя {self.name.value}."
        return f"Я не могу найти {old_number} у контакта {self.name.value}."

    def add_phone(self, number):
        """Вносит изменения в класс, изменяет поле phones, добавляя номер телефона. Возвращает ответ об успешности операции. Тут же проверка на интовнаие
        введенных данных. Если нужно, тут же можно воткнуть и проверку на соответствие формату (длинна, коды и тд)."""

        self.phones.append(Phone(number))
        return f"Успешно добавлен номер телефона {self.name.value} контакту {self.name.value}"

    def set_birthday(self, birthdays_data):
        """Устанавливаем дату рождения. Тут же происходит и проверка на формат ввода. Ожидается yyyy.mm.dd."""

        self.birthday = Birthday(birthdays_data)
        return f"Успешно установлена дата рождения {self.birthday.value} контакту {self.name.value}."

    def days_to_birthday(self):
        """Вычисляет количество дней до предстоящего дня рождения."""

        today = date.today()
        future_birthday = date(year=today.year, month=self.birthday.value.month, day=self.birthday.value.day)
        result = (future_birthday - today).days
        if result > 0:
            return result
        else:
            future_birthday = date(year=today.year+1, month=self.birthday.value.month, day=self.birthday.value.day)
            result = (future_birthday - today).days
            return result

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if not value.isnumeric():
            raise ValueError("Номер состоит не только из цифр.")
        self._value = int(value)


class Birthday(Field):
    @Field.value.setter
    def value(self, new_value: str):
        try:
            new_value = [int(i) for i in new_value.split(".")]
            birthday_date = date(*new_value)
        except ValueError:
            raise ValueError("Не верный формат даты. Ожидаются только цифры в формате гггг.мм.дд.")
        except TypeError:
            raise ValueError("Не верный формат даты. Ожидаются только цифры в формате гггг.мм.дд.")

        if birthday_date <= date.today():
            self._value = birthday_date
        else:
            raise ValueError("День рождения должен уже состояться, а не планироваться в каком-то будущем. Мы же не Боги, чтоб предвидеть это.")