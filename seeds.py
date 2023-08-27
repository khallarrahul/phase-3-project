# Import necessary models
from models import User, Contact, Message
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Print a message indicating the start of seeding
print("Seeding DB....")

# Create the database engine and session
engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)
session = Session()

# Delete existing data to start fresh
session.query(Message).delete()
session.query(Contact).delete()
session.query(User).delete()

# Seed users data (used for fake data)
users_data = []
users = []
for user_data in users_data:
    new_user = User(**user_data)
    new_user.set_password(user_data["password"])
    users.append(new_user)
    session.add(new_user)

# Seed contacts data (used for seeding fake data)
contacts_data = []
contacts = []
for contact_data in contacts_data:
    new_contact = Contact(**contact_data)
    contacts.append(new_contact)
    session.add(new_contact)

# Seed messages data (used for seeding fake data)
messages_data = []
for message_data in messages_data:
    new_message = Message(**message_data)
    session.add(new_message)

# Commit changes to the database
session.commit()

# Print a message indicating the completion of seeding
print("Seeding complete!")
