from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, Column, String
from passlib.hash import bcrypt_sha256
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String(25), unique=True)
    password = Column("password", String, nullable=False)

    # contacts = relationship("Contact", backref="user", cascade="all, delete-orphan")

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
            return

        print(f"Welcome, {user.first_name}!")

    def run_app(self):
        Base.metadata.create_all(bind=self.engine)
        while True:
            print("1. Signup\n2. Login\n3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.signup()
            elif choice == "2":
                self.login()
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    app = UserApp()
    app.run_app()
