from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, Column, String, ForeignKey
from passlib.hash import bcrypt_sha256
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String(25), unique=True)
    password = Column("password", String, nullable=False)

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
            f"username: {self.username}"
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


class UserApp:
    def __init__(self):
        self.engine = create_engine("sqlite:///database.db")
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def signup(self):
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        username = input("Enter a username: ")
        existing_user = self.session.query(User).filter_by(username=username).first()

        if existing_user:
            print("Username already exists. Please choose a different username.")
            return

        password = input("Enter a password: ")
        new_user = User(first_name=first_name, last_name=last_name, username=username)
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

        print(f"Welcome, {user.first_name}!")
        return user

    def add_contact(self, user):
        print("Add Contact")
        full_name = input("Enter Full Name of Contact: ")
        email = input("Enter email: ")

        while True:
            phone = input("Enter phone (10 digits): ")
            if len(phone) != 10 or not phone.isdigit():
                print("Invalid phone number. Please enter a 10- digit number.")
            else:
                break
        home_address = input("Enter home address: ")

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
        from contact_operations import delete_contact_by_id

        self.view_contacts(user)
        contact_id = input("Enter the ID of the contact to delete: ")
        delete_contact_by_id(self.session, int(contact_id))

    def run_app(self):
        Base.metadata.create_all(bind=self.engine)
        while True:
            print("1. Signup\n2. Login\n3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.signup()
            elif choice == "2":
                user = self.login()
                if user:
                    while True:
                        print(
                            "1. Add Contact\n2. View Contacts\n3. Delete Contact\n4. Logout"
                        )
                        sub_choice = input("Enter your choice: ")

                        if sub_choice == "1":
                            self.add_contact(user)
                        elif sub_choice == "2":
                            self.view_contacts(user)
                        elif sub_choice == "3":
                            self.delete_contact(user)
                        elif sub_choice == "4":
                            break
                        else:
                            print("Invalid choice. Please select a valid option.")
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    app = UserApp()
    app.run_app()
