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
    messages = relationship("Message", backref="user", cascade="all, delete-orphan")

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
    phone = Column(String(10), nullable=False)
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
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    message_text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    receiver = relationship("Contact", foreign_keys=[receiver_id])
