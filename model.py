import psycopg2

class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update()

class ClientModel(Observable):
    def __init__(self, db_config):
        super().__init__()
        self.db_config = db_config
        self.clients = []

    def get_all_clients(self):
        connection = psycopg2.connect(**self.db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT client_id, fullname, document FROM clients")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        self.clients = rows
        return rows

    def get_client_by_id(self, client_id):
        connection = psycopg2.connect(**self.db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT client_id, fullname, document, age, phone_number, address, email FROM clients WHERE client_id = %s", (client_id,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        return row

    def refresh_data(self):
        self.get_all_clients()
        self.notify_observers()
