from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models import Base


class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    home_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return (
            f"id: {self.id}, "
            f"email: {self.email}, "
            f"phone: {self.phone}, "
            f"home_address: {self.home_address}"
        )
