from abc import ABC, abstractmethod
from print_table import header_func, line_func
from termcolor import colored
from address_book2 import address_book


class DataOperation(ABC):                     # AbstractFactory
    """Абстрактна фабрика з операціями над данними"""
    @abstractmethod
    def visualise_data(self):
        pass

    @abstractmethod
    def search_in(self):
        pass


class TableDataOperation(DataOperation):       # ConcreteFactory1
    """фабрика з операціями над табличними данними"""
    def visualise_data(self):  # AbstractProductA
        return TableDataVisualise()

    def search_in(self): # AbstractProductB
        return TableDataSearchIn()


class StringDataOperation(DataOperation):        # ConcreteFactory2
    """фабрика з операціями над строковми данними"""
    def visualise_data(self): # AbstractProductA
        return StringDataVisualise()

    def search_in(self): # AbstractProductB
        return StringDataSearchIn()


class DataVisualise(ABC):                       # AbstractProductA(ABC)
    """Абстрактний продукт А"""
    @abstractmethod
    def visualise(self, address_book):
        pass


class TableDataVisualise(DataVisualise):        # ConcreteProductA1
    def visualise(self, address_book):
        '''Looks for mathches in names, phones, mails, tags, notes, birthdays.'''

        table = header_func()
        data = address_book.data
        counter = 0

        for name, record in data.items():

            phones = [phone.value for phone in record.phones]
            phones = " ".join(phones)
            emails = [email.value for email in record.emails]
            emails = " ".join(emails)
            birthday = record.birthday.value.strftime(
                "%m.%d.%Y") if record.birthday else ""
            tag = " ".join(record.tag.value if record.tag else "")
            note = record.note.value if record.note else ""

            table += line_func(record)
            counter += 1

        if counter < 1 and not data:
            return colored(f"The address book is emty.", "yellow")

        if counter < 1:
            return colored(f"I didn't find any '{data}' in adress book.", "yellow")

        return table


class StringDataVisualise(DataVisualise):        # ConcreteProductA2
    def visualise(self,address_book):
        return f'In progress. Expected at version 1.2 '


class DataSearch(ABC):                          # AbstractProductB(ABC)
    """Абстрактний продукт B"""
    @abstractmethod
    def search_in(self,request,address_book):
        pass


class TableDataSearchIn(DataSearch):             # ConcreteProductB1
    def search_in(self, address_book, request):
        '''Looks for mathches in names, phones, mails, tags, notes, birthdays.'''

        table = header_func()
        request_data = request[0]
        data = address_book.data
        counter = 0

        for name, record in data.items():

            phones = [phone.value for phone in record.phones]
            phones = " ".join(phones)
            emails = [email.value for email in record.emails]
            emails = " ".join(emails)
            birthday = record.birthday.value.strftime(
                "%m.%d.%Y") if record.birthday else ""
            tag = " ".join(record.tag.value if record.tag else "")
            note = record.note.value if record.note else ""

            if (
                    request_data in name or
                    request_data in birthday or
                    request_data in emails or
                    request_data in phones or
                    request_data in tag or
                    request_data in note
            ):
                table += line_func(record)
                counter += 1

        if counter < 1 and not data:
            return colored(f"The address book is emty.", "yellow")

        if counter < 1:
            return colored(f"I didn't find any '{data}' in adress book.", "yellow")

        return table



class StringDataSearchIn(DataSearch):            # ConcreteProductB2
    def search_in(self):
        return f'In progress. Expected at version 1.2'



if __name__ == "__main__":
    print(TableDataVisualise().visualise(address_book))
    print(TableDataSearchIn().search_in(address_book,'gle'))