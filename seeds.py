from models import User, Contact, Message
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


print("Seeding DB....")

engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)
session = Session()


session.query(Message).delete()
session.query(Contact).delete()
session.query(User).delete()


users_data = []

users = []
for user_data in users_data:
    new_user = User(**user_data)
    new_user.set_password(user_data["password"])
    users.append(new_user)
    session.add(new_user)


contacts_data = []

contacts = []
for contact_data in contacts_data:
    new_contact = Contact(**contact_data)
    contacts.append(new_contact)
    session.add(new_contact)


messages_data = []

for message_data in messages_data:
    new_message = Message(**message_data)
    session.add(new_message)

# Commit the changes to the database
session.commit()

print("Seeding complete!")
