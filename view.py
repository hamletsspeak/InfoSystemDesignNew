import tkinter as tk
from tkinter import ttk, Toplevel

class ClientView:
    def __init__(self, root):
        self.root = root
        self.root.title("Client Database Viewer")

        self.tree = ttk.Treeview(self.root, columns=("ID", "Full Name", "Document"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Full Name", text="Full Name")
        self.tree.heading("Document", text="Document")
        
        self.tree.bind("<ButtonRelease-1>", self.on_client_select)

        self.details_window = None

    def display_clients(self, clients):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in clients:
            self.tree.insert("", tk.END, values=(row[0], row[1], row[2]))

    def on_client_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        client_id = self.tree.item(selected_item[0])["values"][0]
        self.show_client_details(client_id)

    def show_client_details(self, client_id):
        if self.details_window:
            self.details_window.destroy()

        client_details = self.get_client_details(client_id)

        self.details_window = Toplevel(self.root)
        self.details_window.title("Client Details")

        labels = ["Client ID", "Full Name", "Document", "Age", "Phone", "Address", "Email"]
        for idx, detail in enumerate(client_details):
            label = tk.Label(self.details_window, text=f"{labels[idx]}: {detail}")
            label.pack(pady=5)

    def get_client_details(self, client_id):
        return self.controller.get_full_client_info(client_id)

    def update(self):
        self.controller.load_clients()
