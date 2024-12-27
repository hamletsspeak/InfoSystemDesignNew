import tkinter as tk
from model import ClientModel
from view import ClientView
from controller import ClientController

def main():
    db_config = {
        'dbname': 'clients',
        'user': 'postgres',
        'password': '123',
        'host': 'localhost',
        'port': '5432',
    }

    model = ClientModel(db_config)
    root = tk.Tk()
    view = ClientView(root)
    controller = ClientController(model, view)

    controller.load_clients()

    root.mainloop()

if __name__ == "__main__":
    main()
