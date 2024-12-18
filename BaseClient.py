import re
class BaseClient:
    
    def __init__(self, client_id, fullname, document, age, phone_number, address, email):
        self.__client_id = client_id
        self.__fullname = fullname
        self.__document = document
        self.__age = age
        self.__phone_number = phone_number
        self.__address = address
        self.__email = email
        
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
        self.__fullname = fullname
    def set_document(self, document):
        self.__document = document
    def set_age(self, age):
        self.__age = age
    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number
    def set_address(self, address):
        self.__address = address
    def set_email(self, email):
        self.__email = email