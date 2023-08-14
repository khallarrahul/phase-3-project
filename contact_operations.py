from models import Contact
from sqlalchemy.orm import Session


def delete_contact_by_id(session: Session, contact_id):
    contact = session.query(Contact).get(contact_id)
    if contact:
        session.delete(contact)
        session.commit()
        print("Contact deleted successfully.")
    else:
        print("Contact not found.")
