class ClientController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.controller = self

        self.model.add_observer(self.view)

    def load_clients(self):
        clients = self.model.get_all_clients()
        self.view.display_clients(clients)

    def get_full_client_info(self, client_id):
        client_details = self.model.get_client_by_id(client_id)
        return client_details

    def refresh_clients(self):
        self.model.refresh_data()
