import re

class BaseClient:
    
    def __init__(self, client_id, fullname, document, age, phone_number, address, email):
        self.__client_id = self.__validate_client_id(client_id)
        self.__fullname = self.__validate_fullname(fullname)
        self.__age = self.__validate_age(age)
        self.__phone_number = self.__validate_phone_number(phone_number)
        self.__email = self.__validate_email(email)
        self.__document = self.__validate_document(document)
        self.__address = self.__validate_non_empty_string(address)
        
    
    @staticmethod
    def __validate_non_empty_string(value, field_name):
        if isinstance(value, str) and value.strip():
            return value
        raise ValueError(f"{field_name} must be a non-empty string.")
    
    @staticmethod
    def __validate_client_id(client_id):
        if not isinstance(client_id, int) or client_id <= 0:
            raise ValueError("ID клиента должен быть положительным целым числом.")
        return client_id

    @staticmethod
    def __validate_fullname(fullname):
        if not isinstance(fullname, str) or len(fullname) == 0:
            raise ValueError("ФИО введено неверно (не может быть пустым значением).")
        return fullname

    @staticmethod
    def __validate_document(document):
        if not isinstance(document, str) or not re.fullmatch(r'\d{4} \d{6}', document):
            raise ValueError('Неверные данные паспорта (документа).')
        return document

    @staticmethod
    def __validate_age(age):
        if not isinstance(age, int) or age <= 18:
            raise ValueError("Вы должны быть старше 18 лет, чтобы использовать эту услугу.")
        return age

    @staticmethod
    def __validate_phone_number(phone_number):
        if not isinstance(phone_number, str) or not re.fullmatch(r'((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}', phone_number):
            raise ValueError("Номер телефона введен неверно.")
        return phone_number

    @staticmethod
    def __validate_email(email):
        if not isinstance(email, str) or not re.fullmatch(r'(.+)@(.+)\.(.+)', email):
            raise ValueError("Электронная почта введена неверно.")
        return email

    # Геттеры
    def get_client_id(self):
        return self.__client_id

    def get_fullname(self):
        return self.__fullname

    def get_document(self):
        return self.__document

    def get_age(self):
        return self.__age

    def get_phone_number(self):
        return self.__phone_number

    def get_address(self):
        return self.__address

    def get_email(self):
        return self.__email

    # Сеттеры
    def set_fullname(self, fullname):
        self.__fullname = self.__validate_fullname(fullname)

    def set_document(self, document):
        self.__document = self.__validate_document(document)

    def set_age(self, age):
        self.__age = self.__validate_age(age)

    def set_phone_number(self, phone_number):
        self.__phone_number = self.__validate_phone_number(phone_number)

    def set_address(self, address):
        self.__address = self.__validate_non_empty_string(address)

    def set_email(self, email):
        self.__email = self.__validate_email(email)
