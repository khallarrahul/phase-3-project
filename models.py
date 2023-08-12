from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, Column, String


Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String(25), unique=True)
    password = Column("password", String, nullable=False)

    def __repr__(self):
        return (
            f"id: {self.id}"
            + f"firstname: {self.first_name}"
            + f"lastname: {self.last_name}"
            + f"username: {self.username}"
        )
