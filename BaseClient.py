import re
import json
import yaml
import psycopg2
from psycopg2 import sql
from typing import List
from abc import ABC, abstractmethod
from psycopg2.extras import DictCursor

class BaseClientShortInfo:
    def __init__(self, client_id, fullname, document):
        self.set_id(client_id)
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
    
    def set_id(self, client_id):
        self.__client_id = self.__validate_client_id(client_id)

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

class BaseClient:
    def __init__(self, client_id, fullname, document, age=None, phone_number=None, address=None, email=None, short_info=None):
        if short_info:
            self.short_info = short_info
        else:
            self.short_info = BaseClientShortInfo(client_id, fullname, document)
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

    def get_client_id(self):
        return self.short_info.get_client_id()

    def get_fullname(self):
        return self.short_info.get_fullname()

    def get_document(self):
        return self.short_info.get_document()
    
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
    
    def get_short_info(self):
        return self.short_info

    def __str__(self):
        return (f"Client [ID: {self.get_client_id()}, FIO: {self.get_fullname()}, "
                f"Document: {self.get_document()}, Age: {self.__age}, Phone_Number: {self.__phone_number}, "
                f"Address: {self.__address}, Email: {self.__email}]")

    def __eq__(self, other):
        if isinstance(other, BaseClient):
            return (self.short_info == other.short_info)
        return False

class BaseClient_Rep_Strategy(ABC):
    
    @abstractmethod
    def read_all(self):
        pass

    @abstractmethod
    def save_all(self, data):
        pass

    def __init__(self):
        self.clients = self.read_all()

    def __is_unique(self, document, unverifiable_client_id=None):
        for client in self.clients:
            if client.get_client_id() != unverifiable_client_id and client.get_document() == document:
                return False
        return True

    def add_client(self, fullname, document, age, phone_number, address, email):
        new_id = max([client.get_client_id() for client in self.clients], default=0) + 1
        if not self.__is_unique(document):
            raise ValueError(f"Client with this document already exists.")
        new_client = BaseClient(new_id, fullname, document, age, phone_number, address, email)
        self.clients.append(new_client)
        self.save_all(self.clients)

    def replace_by_id(self, client_id, new_client):
        if not self.__is_unique(new_client.get_document(), client_id):
            raise ValueError(f"Client with this document already exists.")
        for i, client in enumerate(self.clients):
            if client.get_client_id() == client_id:
                self.clients[i] = new_client
                self.save_all(self.clients)
                return True
        return False

    def delete_by_id(self, client_id):
        self.clients = [client for client in self.clients if client.get_client_id() != client_id]
        self.save_all(self.clients)

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
        
    def get_count(self):
        return len(self.clients)
    
class DatabaseConnection:
    _instance = None

    def __new__(cls, db_config):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.connection = None
            cls._instance.db_config = db_config
            cls._instance.connect()
        return cls._instance

    def connect(self):
        """Устанавливает соединение с базой данных, если оно не активно."""
        if self.connection is None or self.connection.closed:
            print("Соединение с базой данных устанавливается...")
            self.connection = psycopg2.connect(**self.db_config)

    def execute_query(self, query, params=None):
        self.connect()  # Проверяем соединение перед запросом
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            self.connection.commit()

    def fetch_all(self, query, params=None):
        self.connect()  # Проверяем соединение перед запросом
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def fetch_one(self, query, params=None):
        self.connect()  # Проверяем соединение перед запросом
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()

    def close(self):
        """Закрывает соединение с базой данных, если оно активно."""
        if self.connection is not None and not self.connection.closed:
            print("Соединение с базой данных закрывается...")
            self.connection.close()


class BaseClientPostgresRep(BaseClient_Rep_Strategy):
    def __init__(self, db_config):
        self.db = DatabaseConnection(db_config)
        self.clients = self.read_all()

    def read_all(self):
        query = "SELECT * FROM clients"
        rows = self.db.fetch_all(query)
        return [BaseClient(client_id=row[0], fullname=row[1], document=row[2],
                           age=row[3], phone_number=row[4], address=row[5], email=row[6]) for row in rows]

    def save_all(self, data):
        query = "DELETE FROM clients"
        self.db.execute_query(query)
        for client in data:
            query = """
                INSERT INTO clients (client_id, fullname, document, age, phone_number, address, email)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(query, (client.get_client_id(), client.get_fullname(), client.get_document(),
                                          client.get_age(), client.get_phone_number(), client.get_address(),
                                          client.get_email()))

    def add_client(self, fullname, document, age, phone_number, address, email):
        new_id = self.get_new_id()
        if not self.__is_unique(document):
            raise ValueError(f"Client with this document already exists.")
        new_client = BaseClient(new_id, fullname, document, age, phone_number, address, email)
        self.clients.append(new_client)
        self.save_all(self.clients)

    def replace_by_id(self, client_id, new_client):
        if not self.__is_unique(new_client.get_document(), client_id):
            raise ValueError(f"Client with this document already exists.")
        query = """
            UPDATE clients 
            SET fullname = %s, document = %s, age = %s, phone_number = %s, address = %s, email = %s
            WHERE client_id = %s
        """
        self.db.execute_query(query, (new_client.get_fullname(), new_client.get_document(), new_client.get_age(),
                                      new_client.get_phone_number(), new_client.get_address(), new_client.get_email(),
                                      client_id))
        return True

    def delete_by_id(self, client_id):
        query = "DELETE FROM clients WHERE client_id = %s"
        self.db.execute_query(query, (client_id,))

    def get_by_id(self, client_id):
        query = "SELECT * FROM clients WHERE client_id = %s"
        row = self.db.fetch_one(query, (client_id,))
        if row:
            return BaseClient(client_id=row[0], fullname=row[1], document=row[2],
                              age=row[3], phone_number=row[4], address=row[5], email=row[6])
        else:
            raise ValueError(f"Client with ID {client_id} not found")

    def __is_unique(self, document, unverifiable_client_id=None):
        query = "SELECT client_id FROM clients WHERE document = %s"
        result = self.db.fetch_one(query, (document,))
        return result is None or result[0] == unverifiable_client_id

    def get_new_id(self):
        query = "SELECT MAX(client_id) FROM clients"
        result = self.db.fetch_one(query)
        return (result[0] or 0) + 1

    def close(self):
        self.db.close()

class BaseClient_Rep_Json(BaseClient_Rep_Strategy):
    def __init__(self, filename):
        self.filename = filename
        self.clients = self.read_all()
        
    def read_all(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return [BaseClient.from_dict(client) for client in data]
        except FileNotFoundError:
            return []

    def save_all(self, data):
        with open(self.filename, 'w') as file:
            json.dump([client.to_dict() for client in data], file, indent=4)

class BaseClient_Rep_Yaml(BaseClient_Rep_Strategy):
    def __init__(self, filename):
        self.filename = filename
        self.clients = self.read_all()
    
    def read_all(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                print(f"Загруженные данные из YAML: {data}")
                return [BaseClient.from_dict(client) for client in data] if data else []
        except FileNotFoundError:
            return []

    def save_all(self, data):
        with open(self.filename, 'w') as file:
            yaml.safe_dump([client.to_dict() for client in data], file)

class BaseClientPostgresAdapter(BaseClient_Rep_Strategy):
    def __init__(self, postgres_rep):
        self.postgres_rep = postgres_rep
        
    def read_all(self):
        print("Hello Adapter!")
        return self.postgres_rep.read_all()

    def save_all(self, data):
        return self.postgres_rep.save_all(data)

    def add_client(self, fullname, document, age, phone_number, address, email):
        return self.postgres_rep.add_client(fullname, document, age, phone_number, address, email)

    def replace_by_id(self, client_id, new_client):
        return self.postgres_rep.replace_by_id(client_id, new_client)

    def delete_by_id(self, client_id):
        return self.postgres_rep.delete_by_id(client_id)

    def get_by_id(self, client_id):
        return self.postgres_rep.get_by_id(client_id)

    def close(self):
        self.postgres_rep.close()

class BaseClientJsonAdapter(BaseClient_Rep_Strategy):
    def __init__(self, json_rep):
        self.json_rep = json_rep

    def read_all(self):
        return self.json_rep.read_all()

    def save_all(self, data):
        return self.json_rep.save_all(data)

    def add_client(self, fullname, document, age, phone_number, address, email):
        return self.json_rep.add_client(fullname, document, age, phone_number, address, email)

    def replace_by_id(self, client_id, new_client):
        return self.json_rep.replace_by_id(client_id, new_client)

    def delete_by_id(self, client_id):
        return self.json_rep.delete_by_id(client_id)

    def get_by_id(self, client_id):
        return self.json_rep.get_by_id(client_id)

    def close(self):
        self.json_rep.close()

class BaseClientYamlAdapter(BaseClient_Rep_Strategy):
    def __init__(self, yaml_rep):
        self.yaml_rep = yaml_rep

    def read_all(self):
        return self.yaml_rep.read_all()

    def save_all(self, data):
        return self.yaml_rep.save_all(data)

    def add_client(self, fullname, document, age, phone_number, address, email):
        return self.yaml_rep.add_client(fullname, document, age, phone_number, address, email)

    def replace_by_id(self, client_id, new_client):
        return self.yaml_rep.replace_by_id(client_id, new_client)

    def delete_by_id(self, client_id):
        return self.yaml_rep.delete_by_id(client_id)

    def get_by_id(self, client_id):
        return self.yaml_rep.get_by_id(client_id)

    def close(self):
        self.yaml_rep.close()
        
class BaseClientManagerStrategy:
    def __init__(self, repository_strategy: BaseClient_Rep_Strategy):
        self.repository = repository_strategy

    def add_client(self, fullname, document, age, phone_number, address, email):
        self.repository.add_client(fullname, document, age, phone_number, address, email)

    def get_client_by_id(self, client_id):
        return self.repository.get_by_id(client_id)

    def replace_client(self, client_id, new_client):
        return self.repository.replace_by_id(client_id, new_client)

    def delete_client(self, client_id):
        return self.repository.delete_by_id(client_id)

    def get_all_clients(self):
        return self.repository.read_all()
    
    def get_k_n_short_list(self, k, n):
        return self.repository.get_k_n_short_list(k, n)
    
    def sort_by_field(self):
        return self.repository.sort_by_field()

db_config = {
    'dbname': 'clients',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost',
    'port': '5432',
}

postgres_repository = BaseClientPostgresRep(db_config)
client_manager = BaseClientManagerStrategy(postgres_repository)

#client_manager.add_client("Иван Иванов", "1211 111112", 30, "89728845782", "Москва", "ivan2@mail.com")

clients = client_manager.get_all_clients()
for client in clients:
    print(client)

postgres_repository.close()


#json_repository = BaseClient_Rep_Yaml('clients.yaml')

#client_manager = BaseClientManagerStrategy(json_repository)

#client_manager.add_client("Иван Иванов", "1211 111111", 30, "89728845781", "Москва", "ivan@mail.com")

#clients = client_manager.get_all_clients()
#for client in clients:
#    print(client)