from record import Record
from termcolor import colored


def header_func() -> str:
    '''Creates a header of a table.'''
    header = "\n|" + "-" * 117 + "|"
    headers = ["Name", "Phone", "Birthday", "Email", "Tags", "Notes"]
    columns = "\n|{:^15}|{:^15}|{:^12}|{:^25}|{:^15}|{:^30}|"
    header += columns.format(*headers)
    header += "\n|" + "-" * 117 + "|"
    header = colored(f"{header}", "blue")

    return header


def line_func(record: Record) -> str:
    '''Creates lines of a table.'''
    line = ""
    columns = "\n|{:^15}|{:^15}|{:^12}|{:^25}|{:^15}|{:^30}|"

    name = record.name.value.title()
    name_table = [name[i:i+13] for i in range(0, len(name), 13)]

    phone_table = [phone.value for phone in record.phones]

    birthday = record.birthday.value.strftime(
        "%d.%m.%Y") if record.birthday else ""
    birthday_table = [birthday]

    email_table = []

    for email in record.emails:
        for i in range(0, len(email.value), 23):
            email_table.append(email.value[i:i+23])

    tag = record.tag.value if record.tag else ""
    tag_table = []
    temp = ""
    tag_i = ""

    for tag_i in tag:

        if len(temp + tag_i) < 13:
            temp += " " + tag_i

        else:
            tag_table.append(temp)
            temp = tag_i

    tag_table.append(temp)

    note = record.note.value if record.note else " "
    note_table = [note[i:i+28] for i in range(0, len(note), 28)]

    all_table = [name_table, phone_table, birthday_table,
                 email_table, tag_table, note_table]
    max_len_table = len(max(all_table, key=lambda table: len(table)))

    for i in range(max_len_table):
        cells = []

        for table in all_table:

            table = table[i] if i < len(table) else ""
            cells.append(table)

        line += columns.format(*cells)

    line += "\n|" + "-" * 117 + "|"

    return line