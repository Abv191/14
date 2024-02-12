import pickle
from datetime import datetime
from collections import UserDict



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
    def __init__(self, filename='address_book.pkl'):
        self.filename = filename
        self.load()

    def load(self):
        try:
            with open(self.filename, 'rb') as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            self.data = {}

    def save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.data, f)

    def add_record(self, record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def search(self, query):
        found_records = []
        for record in self.values():
            if query.lower() in record.name.value.lower():
                found_records.append(record)
            for phone in record.phones:
                if query in phone.value:
                    found_records.append(record)
                    break
        return found_records

    def find(self, name):
        return self.data.get(name, None)

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()


def add_record_handler(address_book):
    name = input("Enter the contact's name: ")
    birthday_input = input("Enter the contact's birthday (YYYY-MM-DD), leave blank if unknown: ")
    try:
        birthday = datetime.strptime(birthday_input, "%Y-%m-%d").date()
    except ValueError:
        birthday = None
    record = Record(name, birthday)
    while True:
        phone = input("Enter a phone number for the contact (10 digits): ")
        try:
            record.add_phone(phone)
        except ValueError as e:
            print(e)
        choice = input("Do you want to add another phone number? (yes/no): ")
        if choice.lower() != 'yes':
            break
    address_book.add_record(record)
    print("Contact added successfully.")


def delete_record_handler(address_book):
    query = input("Enter the name or phone number of the contact you want to delete: ")
    found_records = address_book.search(query)
    if not found_records:
        print("No matching contacts found.")
        return
    print("Found matching contacts:")
    for i, record in enumerate(found_records, 1):
        print(f"{i}. {record}")
    choice = input("Enter the number of the contact you want to delete: ")
    try:
        index = int(choice) - 1
        if 0 <= index < len(found_records):
            address_book.delete_record(found_records[index])
            print("Contact deleted successfully.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid choice.")


def search_handler(address_book):
    query = input("Enter the name or phone number you want to search for: ")
    found_records = address_book.search(query)
    if not found_records:
        print("No matching contacts found.")
    else:
        print("Matching contacts:")
        for record in found_records:
            print(record)


def main():
    with AddressBook() as address_book:
        while True:
            print("\nAddress Book Menu:")
            print("1. Add a new contact")
            print("2. Delete a contact")
            print("3. Search for a contact")
            print("4. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                add_record_handler(address_book)
            elif choice == '2':
                delete_record_handler(address_book)
            elif choice == '3':
                search_handler(address_book)
            elif choice == '4':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
