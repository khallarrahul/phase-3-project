from models import Contact, User, Message, Base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from simple_term_menu import TerminalMenu
import os


# Function to delete a contact by its ID
def delete_contact_by_id(session: Session, contact_id):
    contact = session.query(Contact).get(contact_id)
    if contact:
        session.delete(contact)
        session.commit()
        print("Contact deleted successfully.")
    else:
        print("Contact not found.")


# Main application class
class UserApp:
    def __init__(self):
        # Initialize the database connection
        self.engine = create_engine("sqlite:///database.db")
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    # Function for user signup
    def signup(self):
        user_data = {}
        user_data["first_name"] = input("Enter your first name: ")
        user_data["last_name"] = input("Enter your last name: ")

        while True:
            user_data["phone_number"] = input("Enter your 10 digit phone number: ")
            if (
                len(user_data["phone_number"]) != 10
                or not user_data["phone_number"].isdigit()
            ):
                print("Invalid phone number. Please enter a 10-digit number.")
            else:
                break

        existing_number = (
            self.session.query(User)
            .filter_by(phone_number=user_data["phone_number"])
            .first()
        )

        if existing_number:
            print(
                "Phone number already exists. Please choose a different phone number."
            )
            return

        user_data["username"] = input("Enter a username: ")
        existing_user = (
            self.session.query(User).filter_by(username=user_data["username"]).first()
        )

        if existing_user:
            print("Username already exists. Please choose a different username.")
            return

        password = input("Enter a password: ")
        new_user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            username=user_data["username"],
            phone_number=user_data["phone_number"],
        )
        new_user.set_password(password)

        self.session.add(new_user)
        self.session.commit()
        print("User registered successfully!")

    # Function for user signup
    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user = self.session.query(User).filter_by(username=username).first()

        if not user or not user.check_password(password):
            print("Invalid username or password.")
            return None
        print("\n" * 40)
        print(f"\nWelcome, {user.first_name}!")
        return user

    # Function to handle user menu abort action
    def abort_with_menu(self):
        print(
            "\n(Enter 'MENU' to return to the main menu or press 'ENTER' to move forward)"
        )
        menu_input = input()
        if menu_input.upper() == "MENU":
            print("\nAborting to Main Menu...\n")
            return True
        else:
            print("ENTER pressed. Continuing...\n")
            return False

    # Function to add a contact
    def add_contact(self, user):
        print("\nAdd Contact")
        if self.abort_with_menu():
            return

        contact_info = {}
        contact_info["full_name"] = input("Enter Full Name of Contact: ")
        if contact_info["full_name"].upper() == "MENU":
            print("\nAborting to Main Menu...")
            return

        contact_info["email"] = input("Enter email: ")
        if contact_info["email"].upper() == "MENU":
            print("\nAborting to Main Menu...")
            return

        while True:
            contact_info["phone"] = input("Enter phone (10 digits): ")
            if contact_info["phone"].upper() == "MENU":
                print("\nAborting to Main Menu...")
                return
            if len(contact_info["phone"]) != 10 or not contact_info["phone"].isdigit():
                print("Invalid phone number. Please enter a 10-digit number.")
            else:
                existing_contact = (
                    self.session.query(Contact)
                    .filter_by(phone=contact_info["phone"], user=user)
                    .first()
                )
                if existing_contact:
                    print("Contact with the same phone number already exists.")
                else:
                    break

        contact_info["home_address"] = input("Enter home address: ")
        if contact_info["home_address"].upper() == "MENU":
            print("\nAborting to Main Menu...")
            return

        new_contact = Contact(
            email=contact_info["email"],
            full_name=contact_info["full_name"],
            phone=contact_info["phone"],
            home_address=contact_info["home_address"],
            user=user,
        )
        self.session.add(new_contact)
        self.session.commit()
        print("Contact added successfully!")

    # Function to view user's contacts
    def view_contacts(self, user):
        print("\n View Contacts\n")
        contacts = user.contacts

        if not contacts:
            print("You have no contacts.\n")
        else:
            for contact in contacts:
                print(
                    f"{contact.id}\n"
                    f"{contact.full_name}\n"
                    f"Email: {contact.email}\n"
                    f"Phone: {contact.phone}\n"
                    f"Home Address: {contact.home_address}\n"
                )

    # Function to delete a contact
    def delete_contact(self, user):
        if self.abort_with_menu():
            return
        from contact_operations import delete_contact_by_id

        self.view_contacts(user)
        contact_id = input("Enter the ID of the contact to delete: ")
        if contact_id.upper() == "MENU":
            print("\nAborting to Main Menu...")
            return
        delete_contact_by_id(self.session, int(contact_id))

    # Function to send a message
    def send_message(self, sender):
        if self.abort_with_menu():
            return

        self.view_contacts(sender)
        receiver_phone_number = input(
            "Enter the phone number of the contact to send the message to: "
        )

        if receiver_phone_number.upper() == "MENU":
            print("\nAborting to Main Menu...")
            return

        receiver_user = (
            self.session.query(User)
            .filter_by(phone_number=receiver_phone_number)
            .first()
        )
        if not receiver_user:
            print("Contact not found.")
            return

        message_text = input("Enter the message: ")
        new_message = Message(
            sender_id=sender.id,
            receiver_id=receiver_user.id,
            message_text=message_text,
        )
        self.session.add(new_message)
        self.session.commit()
        print("Message sent successfully!")

    # Function to check sent messages
    def check_messages(self, user):
        sent_messages = (
            self.session.query(Message)
            .filter_by(sender_id=user.id)
            .order_by(Message.timestamp)
            .all()
        )

        if sent_messages:
            print("Messages sent:")
            for message in sent_messages:
                receiver_contact = (
                    self.session.query(User).filter_by(id=message.receiver_id).first()
                )
                print(
                    f"To: {receiver_contact.first_name}\n"
                    f"Timestamp: {message.timestamp}\n"
                    f"Message: {message.message_text}\n"
                )
        else:
            print("No messages sent.")

    # Function to view received messages
    def view_received_messages(self, user):
        received_messages = (
            self.session.query(Message)
            .join(Contact, Message.sender_id == Contact.id)
            .filter(Contact.phone == user.phone_number)
            .order_by(Message.timestamp)
            .all()
        )

        if received_messages:
            print("\nMessages received:")
            for message in received_messages:
                sender_contact = (
                    self.session.query(User).filter_by(id=message.sender_id).first()
                )
                print(
                    f"From: {sender_contact.first_name}, {sender_contact.last_name}\n"
                    f"Timestamp: {message.timestamp}\n"
                    f"Message: {message.message_text}\n"
                )
        else:
            print("\nNo messages received.\n")

    # Main application loop
    def run_app(self):
        Base.metadata.create_all(bind=self.engine)
        print("\n" * 40)
        main_menu_entries = ["Signup", "Login", "Exit"]
        main_menu = TerminalMenu(
            main_menu_entries,
            title="""
+-+-+-+ +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+
|T|h|e| |C|o|n|t|a|c|t| |M|a|n|a|g|e|r|
+-+-+-+ +-+-+-+-+-+-+-+ +-+-+-+-+-+-+-+
""",
        )

        while True:
            selected_main_option = main_menu.show()

            if selected_main_option == 0:
                self.signup()
            elif selected_main_option == 1:
                user = self.login()
                if user:
                    sub_menu_entries = [
                        "Add Contact",
                        "View Contacts",
                        "Delete Contact",
                        "Send Message",
                        "Check Sent Messages",
                        "View Received Messages",
                        "Logout",
                    ]
                    sub_menu = TerminalMenu(sub_menu_entries, title="User Menu")

                    while True:
                        os.system("clear")
                        selected_sub_option = sub_menu.show()

                        if selected_sub_option == 0:
                            self.add_contact(user)
                        elif selected_sub_option == 1:
                            self.view_contacts(user)
                            input("\nPress Enter to continue...")
                        elif selected_sub_option == 2:
                            self.delete_contact(user)
                        elif selected_sub_option == 3:
                            self.send_message(user)
                        elif selected_sub_option == 4:
                            self.check_messages(user)
                            input("\nPress Enter to continue...")
                        elif selected_sub_option == 5:
                            self.view_received_messages(user)
                            input("\nPress Enter to continue...")
                        elif selected_sub_option == 6:
                            os.system("clear")
                            break
                        else:
                            print("Invalid choice. Please select a valid option.")
            elif selected_main_option == 2:
                os.system("clear")
                break
            else:
                print("Invalid choice. Please select a valid option.")


# Run the application
if __name__ == "__main__":
    app = UserApp()
    app.run_app()
