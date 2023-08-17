from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, Column, String, ForeignKey
from passlib.hash import bcrypt_sha256
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import DateTime


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String(25), unique=True)
    password = Column("password", String, nullable=False)
    phone_number = Column(String(10), nullable=False)

    contacts = relationship("Contact", backref="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password = bcrypt_sha256.hash(password)

    def check_password(self, password):
        return bcrypt_sha256.verify(password, self.password)

    def __repr__(self):
        return (
            f"id: {self.id}, "
            f"firstname: {self.first_name}, "
            f"lastname: {self.last_name}, "
            f"username: {self.username},"
            f"phone: {self.phone_number}"
        )


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(30), nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    home_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return (
            f"id: {self.id}, "
            f"full_name: {self.full_name}"
            f"email: {self.email}, "
            f"phone: {self.phone}, "
            f"home_address: {self.home_address}"
        )


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    message_text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender = relationship("Contact", foreign_keys=[sender_id])
    receiver = relationship("Contact", foreign_keys=[receiver_id])


class UserApp:
    def __init__(self):
        self.engine = create_engine("sqlite:///database.db")
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def signup(self):
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        phone_number = input("Enter your 10 digit phone number: ")

        existing_number = (
            self.session.query(User).filter_by(phone_number=phone_number).first()
        )

        if existing_number:
            print("Phone number already exists. Please choose a different username.")
            return

        username = input("Enter a username: ")
        existing_user = self.session.query(User).filter_by(username=username).first()

        if existing_user:
            print("Username already exists. Please choose a different username.")
            return

        password = input("Enter a password: ")
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
        )
        new_user.set_password(password)

        self.session.add(new_user)
        self.session.commit()
        print("User registered successfully!")

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

    def add_contact(self, user):
        print("\nAdd Contact")
        if self.abort_with_menu():
            return

        full_name = input("Enter Full Name of Contact: ")
        if full_name.upper() == "MENU":
            print("\nAborting to Main Menu...")
            return

        email = input("Enter email: ")
        if email.upper() == "MENU":
            print("\nAborting to Main Menu...")
            return

        while True:
            phone = input("Enter phone (10 digits): ")
            if phone.upper() == "MENU":
                print("\nAborting to Main Menu...")
                return
            if len(phone) != 10 or not phone.isdigit():
                print("Invalid phone number. Please enter a 10-digit number.")
            else:
                break

        home_address = input("Enter home address: ")
        if home_address.upper() == "MENU":
            print("\nAborting to Main Menu...")
            return

        new_contact = Contact(
            email=email,
            full_name=full_name,
            phone=phone,
            home_address=home_address,
            user=user,
        )
        self.session.add(new_contact)
        self.session.commit()
        print("Contact added successfully!")

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

    def send_message(self, sender):
        if self.abort_with_menu():
            return
        self.view_contacts(sender)
        receiver_id = input("Enter the ID of the contact to send the message to: ")
        if receiver_id.upper() == "MENU":
            print("\nAborting to Main Menu...")
            return
        receiver = self.session.query(Contact).get(receiver_id)
        if not receiver:
            print("Contact not found.")
            return
        message_text = input("Enter the message: ")
        new_message = Message(
            sender_id=sender.id, receiver_id=receiver.id, message_text=message_text
        )
        self.session.add(new_message)
        self.session.commit()
        print("Message sent successfully!")

    def check_messages(self, user):
        sent_messages = (
            self.session.query(Message)
            .filter_by(sender_id=user.id)  # Filter messages sent by the logged-in user
            .order_by(Message.timestamp)
            .all()
        )

        if sent_messages:
            print("Messages sent:")
            for message in sent_messages:
                receiver_contact = (
                    self.session.query(Contact)
                    .filter_by(id=message.receiver_id)
                    .first()
                )
                print(
                    f"To: {receiver_contact.full_name}\n"
                    f"Timestamp: {message.timestamp}\n"
                    f"Message: {message.message_text}\n"
                )
        else:
            print("No messages sent.")

    def view_received_messages(self, user):
        received_messages = (
            self.session.query(Message)
            .join(Contact, Message.sender_id == Contact.id)
            .filter(
                Contact.phone == user.phone_number
            )  # I want to filter by reciever's messages
            .order_by(Message.timestamp)
            .all()
        )

        if received_messages:
            print("\nMessages received:")
            for message in received_messages:
                sender_contact = (
                    self.session.query(Contact).filter_by(id=message.sender_id).first()
                )
                print(
                    f"From: {sender_contact.full_name}\n"
                    f"Timestamp: {message.timestamp}\n"
                    f"Message: {message.message_text}\n"
                )
        else:
            print("\nNo messages received.\n")

    def run_app(self):
        Base.metadata.create_all(bind=self.engine)
        while True:
            print("\nContact Manager App\n")
            print("1. Signup\n2. Login\n3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.signup()
            elif choice == "2":
                user = self.login()
                if user:
                    while True:
                        print(
                            "1. Add Contact\n2. View Contacts\n3. Delete Contact\n4. Send Message\n5. Check Sent Messages\n6. View Received Messages\n7. Logout"
                        )
                        sub_choice = input("\nEnter your choice: ")

                        if sub_choice == "1":
                            self.add_contact(user)
                        elif sub_choice == "2":
                            self.view_contacts(user)
                        elif sub_choice == "3":
                            self.delete_contact(user)
                        elif sub_choice == "4":
                            self.send_message(user)
                        elif sub_choice == "5":
                            self.check_messages(user)
                        elif sub_choice == "6":
                            self.view_received_messages(user)
                        elif sub_choice == "7":
                            print("\n" * 40)
                            break
                        else:
                            print("Invalid choice. Please select a valid option.")
            elif choice == "3":
                print("\n" * 40)
                break
            else:
                print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    app = UserApp()
    app.run_app()
