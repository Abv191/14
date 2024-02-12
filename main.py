import pickle
from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __str__(self):
        return str(self.__value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self.validate_phone(value)
        super().__init__(value)

    def validate_phone(self, value):
        if not isinstance(value, str) or len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must contain exactly 10 digits.")

    @Field.value.setter
    def value(self, new_value):
        self.validate_phone(new_value)
        super().value(new_value)


class Birthday(Field):
    def __init__(self, value=None):
        self.validate_date(value)
        super().__init__(value)

    def validate_date(self, value):
        if value is not None and not isinstance(value, datetime):
            raise ValueError("Birthday must be a datetime object.")

    @Field.value.setter
    def value(self, new_value):
        self.validate_date(new_value)
        super().value(new_value)


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

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

    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.now().date()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()
            return (next_birthday - today).days
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.birthday.value}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, N):
        records = list(self.data.values())
        for i in range(0, len(records), N):
            yield records[i:i+N]

    def save_to_file(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.data, f)

    @classmethod
    def load_from_file(cls, filename):
        address_book = cls()
        try:
            with open(filename, 'rb') as f:
                address_book.data = pickle.load(f)
        except FileNotFoundError:
            # If file doesn't exist, return an empty address book
            pass
        return address_book


# Example usage:
if __name__ == "__main__":
    # Creating an address book
    address_book = AddressBook()
    record1 = Record("John Doe", datetime(1990, 5, 15))
    record1.add_phone("1234567890")
    record1.add_phone("0987654321")
    record2 = Record("Jane Smith", datetime(1985, 10, 20))
    record2.add_phone("9876543210")
    address_book.add_record(record1)
    address_book.add_record(record2)

    # Saving the address book to a file
    address_book.save_to_file('address_book.pkl')

    # Loading the address book from a file
    loaded_address_book = AddressBook.load_from_file('address_book.pkl')
    print("Loaded address book:")
    for record in loaded_address_book.values():
        print(record)
