from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.set_value(value)

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def set_value(self, value):
        if not isinstance(value, str) or len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must contain exactly 10 digits.")
        self.value = value


class Birthday(Field):
    def set_value(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
            self.value = value
        except ValueError:
            raise ValueError("Invalid birthday format. Use YYYY-MM-DD.")

    def get_value(self):
        return self.value

    def days_to_birthday(self):
        if not self.value:
            raise ValueError("Birthday not set.")

        today = datetime.now()
        bday = datetime.strptime(self.value, '%Y-%m-%d').replace(year=today.year)

        if bday < today:
            bday = bday.replace(year=today.year + 1)

        return (bday - today).days


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != str(phone)]

    def edit_phone(self, old_phone, new_phone):
        if not self.find_phone(old_phone):
            raise ValueError("Old phone number not found.")
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        return next((p for p in self.phones if str(p) == str(phone)), None)

    def set_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def get_birthday(self):
        return self.birthday.get_value() if self.birthday else None

    def days_to_birthday(self):
        return self.birthday.days_to_birthday() if self.birthday else None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def __iter__(self):
        return self.iterator()

    def iterator(self, n=10):
        items = list(self.data.values())
        for i in range(0, len(items), n):
            yield items[i:i + n]


