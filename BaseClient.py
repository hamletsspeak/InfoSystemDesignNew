import re
import json
class BaseClientShortInfo:
    def __init__(self, client_id, fullname, document):
        self.__client_id = self.__validate_client_id(client_id)
        self.set_fullname(fullname)
        self.set_document(document)
        
    @staticmethod
    def __validate_client_id(client_id):
        if not isinstance(client_id, int) or client_id <= 0:
            raise ValueError("ID клиента должен быть положительным целым числом.")
        return client_id

    @staticmethod
    def __validate_fullname(fullname):
        if not isinstance(fullname, str) or len(fullname) == 0:
            raise ValueError("ФИО введено неверно (не может быть пустым значением, должны быть только буквы).")
        return fullname

    @staticmethod
    def __validate_document(document):
        if not isinstance(document, str) or not re.fullmatch(r'\d{4} \d{6}', document):
            raise ValueError('Неверные данные паспорта (документа).')
        return document
    
    @staticmethod
    def from_string(data_str):
        try:
            data = data_str.split(',')
            if len(data) != 3:
                raise ValueError("Неверное количество полей в строке.")
            
            client_id = int(data[0].strip())
            fullname = data[1].strip()
            document = data[2].strip()
            
            return BaseClient(client_id, fullname, document)
        except Exception as e:
            raise ValueError(f"Ошибка при разборе данных клиента: {e}")
        
    def get_client_id(self):
        return self.__client_id

    def get_fullname(self):
        return self.__fullname

    def get_document(self):
        return self.__document
    
    def set_fullname(self, fullname):
        self.__fullname = self.__validate_fullname(fullname)

    def set_document(self, document):
        self.__document = self.__validate_document(document)
        
    def __eq__(self, other):
        if isinstance(other, BaseClientShortInfo):
            return (self.__client_id == other.__client_id and
                    self.__fullname == other.__fullname and
                    self.__document == other.__document)
        return False
    
    def __str__(self):
        return f"Client short info [ID: {self.__client_id}, FIO: {self.__fullname}, Document: {self.__document}]"

    def __hash__(self):
        return hash(self.get_fullname()) + hash(self.get_client_id()) + hash(self.get_document())

class BaseClient(BaseClientShortInfo):
    
    def __init__(self, client_id, fullname, document, age = None, phone_number = None, address = None, email = None):
        super().__init__(client_id, fullname, document)
        if phone_number:
            self.set_phone_number(phone_number)
        if address:
            self.set_address(address)
        if email:
            self.set_email(email)
        if age:
            self.set_age(age)
            
    @staticmethod
    def __validate_non_empty_string(value, field_name):
        if isinstance(value, str) and value.strip():
            return value
        raise ValueError(f"{field_name} должно быть непустой строкой.")

    @staticmethod
    def __validate_phone_number(phone_number):
        if not isinstance(phone_number, str) or not re.fullmatch(r'((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}', phone_number):
            raise ValueError("Номер телефона введен неверно.")
        return phone_number
    
    @staticmethod
    def __validate_age(age):
        if not isinstance(age, int) or age <= 18:
            raise ValueError("Вы должны быть старше 18 лет, чтобы использовать эту услугу.")
        return age

    @staticmethod
    def __validate_email(email):
        if not isinstance(email, str) or not re.fullmatch(r'(.+)@(.+)\.(.+)', email):
            raise ValueError("Электронная почта введена неверно.")
        return email

    @staticmethod
    def from_string(data_str):
        try:
            data = data_str.split(',')
            if len(data) != 7:
                raise ValueError("Неверное количество полей в строке.")
            
            client_id = int(data[0].strip())
            fullname = data[1].strip()
            document = data[2].strip()
            age = data[3].strip()
            phone_number = data[4].strip()
            address = data[5].strip()
            email = data[6].strip()
            
            return BaseClient(client_id, fullname, document, age, phone_number, address, email)
        except Exception as e:
            raise ValueError(f"Ошибка при разборе данных клиента: {e}")
        
    @staticmethod
    def from_dict(data: dict):
        return BaseClient(
            data['client_id'], data['fullname'], data['document'], data['age'], 
            data['phone_number'], data['address'], data['email'],)
    def to_dict(self):
        return {
            'client_id': self.get_client_id(),
            'fullname': self.get_fullname(),
            'document': self.get_document(),
            'age': self.get_age(),
            'phone_number': self.get_phone_number(),
            'address': self.get_address(),
            'email': self.get_email()
        }

    def get_age(self):
        return self.__age

    def get_address(self):
        return self.__address

    def get_email(self):
        return self.__email

    def get_phone_number(self):
        return self.__phone_number
    
    def set_age(self, age):
        self.__age = self.__validate_age(age)

    def set_address(self, address):
        self.__address = self.__validate_non_empty_string(address, "Address")

    def set_email(self, email):
        self.__email = self.__validate_email(email)

    def set_phone_number(self, phone_number):
        self.__phone_number = self.__validate_phone_number(phone_number)
    
    def __str__(self):
            return (f"Client [ID: {self.get_client_id()}, FIO: {self.get_fullname()}, "
                    f"Document: {self.get_document()}, Age: {self.__age}, Phone_Number: {self.__phone_number}, "
                    f"Address: {self.__address}, Email: {self.__email}]")
    
    def short_info(self):
        return super().__str__()
        
    def __eq__(self, other):
        if isinstance(other, BaseClient):
            return (super().__eq__(other))
        return False
    
class BaseClient_Rep_Json:
    def __init__(self, file_name):
        self.file_name = file_name
        self.clients = self.read_all()
        
    def read_all(self):
        try:
            with open(self.file_name, 'r') as file:
                data = json.load(file)
                return [BaseClient.from_dict(client) for client in data]
        except FileNotFoundError:
            return []

    def save_all(self):
        data = []
        for client in self.clients:
            data.append(client.to_dict())
        with open(self.file_name, 'w') as file:
            json.dump([client.to_dict() for client in self.clients], file, indent=4)

    def get_by_id(self, client_id):
        for client in self.clients:
            if client.get_client_id() == client_id:
                return client
        raise ValueError(f"Client with ID {client_id} not found")

    def get_k_n_short_list(self, k, n):
        start = (k - 1) * n
        end = start + n
        return self.clients[start:end]

    def sort_by_field(self):
        self.clients.sort(key=lambda client: client.client_id)

    def __is_unique(self, document, unverifiable_client_id=None):
        if unverifiable_client_id:
            for client in self.clients:
                if client.get_client_id() != unverifiable_client_id and client.get_document() == document:
                    return False
        else:
            for client in self.clients:
                if client.get_document() == document:
                    return False
        return True

    def add_client(self, fullname, document, age, phone_number, address, email):
        new_id = max([client.get_client_id() for client in self.clients], default=0) + 1
        if not self.__is_unique(document):
            raise ValueError(f"client with this document already exists.")
        new_client = BaseClient(new_id, fullname, document, age, phone_number, address, email)
        self.clients.append(new_client)
        self.save_all()

    def replace_by_id(self, client_id, new_client):
        if not self.__is_unique(new_client.get_document(), client_id):
            raise ValueError(f"Customer with this document already exists.")
        for i, client in enumerate(self.clients):
            if client.get_client_id() == client_id:
                self.clients[i] = new_client
                self.save_all()
                return True
        return False

    def delete_by_id(self, client_id):
        self.clients = [client for client in self.clients if client.get_client_id() != client_id]
        self.save_all()

    def get_count(self):
        return len(self.clients)

clientFull = BaseClient(1, "Иван Иванов", "1234 123123", 25, "+7 123 123 12 12", "Москва 12", "ivanov@example.com")
clientShort = BaseClientShortInfo(1, "Иван Иванов", "1234 123123")
clientEq = BaseClientShortInfo(1, "Иван Иванов", "1234 123123")

print("Полная версия", clientFull)
print("Краткая версия", clientShort)
print(clientShort==clientEq)