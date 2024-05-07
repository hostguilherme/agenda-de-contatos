import sqlite3
from tabulate import tabulate


# Classe para gerenciar contatos
class ContactManager:
    def __init__(self, db_file='contacts.db'):
        self.connection = sqlite3.connect(db_file)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute(
                '''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    phone TEXT,
                    email TEXT
                )
                '''
            )

    def add_contact(self, name, phone, email):
        with self.connection:
            self.connection.execute(
                'INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)',
                (name, phone, email)
            )

    def view_contacts(self):
        cursor = self.connection.execute('SELECT * FROM contacts')
        contacts = cursor.fetchall()
        print(tabulate(contacts, headers=["ID", "Name", "Phone", "Email"], tablefmt="fancy_grid"))

    def edit_contact(self, contact_id, name=None, phone=None, email=None):
        with self.connection:
            if name:
                self.connection.execute('UPDATE contacts SET name = ? WHERE id = ?', (name, contact_id))
            if phone:
                self.connection.execute('UPDATE contacts SET phone = ? WHERE id = ?', (phone, contact_id))
            if email:
                self.connection.execute('UPDATE contacts SET email = ? WHERE id = ?', (email, contact_id))

    def delete_contact(self, contact_id):
        with self.connection:
            self.connection.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))


# Funções para a interface
def menu():
    print("1. Adicionar contato")
    print("2. Visualizar contatos")
    print("3. Editar contato")
    print("4. Excluir contato")
    print("5. Sair")


def main():
    manager = ContactManager()

    while True:
        menu()
        choice = int(input("Escolha uma opção: "))

        if choice == 1:
            name = input("Nome do contato: ")
            phone = input("Telefone do contato: ")
            email = input("Email do contato: ")
            manager.add_contact(name, phone, email)
            print("Contato adicionado com sucesso!")
        elif choice == 2:
            print("Contatos:")
            manager.view_contacts()
        elif choice == 3:
            contact_id = int(input("ID do contato a ser editado: "))
            name = input("Novo nome (deixe em branco para não alterar): ")
            phone = input("Novo telefone (deixe em branco para não alterar): ")
            email = input("Novo email (deixe em branco para não alterar): ")
            manager.edit_contact(contact_id, name or None, phone or None, email or None)
            print("Contato editado com sucesso!")
        elif choice == 4:
            contact_id = int(input("ID do contato a ser excluído: "))
            manager.delete_contact(contact_id)
            print("Contato excluído com sucesso!")
        elif choice == 5:
            break
        else:
            print("Opção inválida, tente novamente.")


if __name__ == '__main__':
    main()
