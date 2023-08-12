from models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

print("Seeding DB....")

engine = create_engine("sqlite:///database.db")

Session = sessionmaker(bind=engine)
session = Session()

session.query(User).delete()

users = []

for user_data in users:
    new_user = User(**user_data)
    session.add(new_user)

# Commit the changes to the database
session.commit()

print("Seeding complete!")
