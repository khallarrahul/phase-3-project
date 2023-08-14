from models import User, UserApp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

print("Seeding DB....")

engine = create_engine("sqlite:///database.db")

Session = sessionmaker(bind=engine)
session = Session()

session.query(User).delete()


def input_user_data():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    return {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "password": password,
    }


users = []

while True:
    user_data = input_user_data()
    users.append(user_data)
    another_user = input("Add another user? (y/n): ")
    if another_user.lower() != "y":
        break

for user_data in users:
    new_user = User(**user_data)
    new_user.set_password(user_data["password"])  # Hash the password
    session.add(new_user)

# Commit the changes to the database
session.commit()

print("Seeding complete!")
