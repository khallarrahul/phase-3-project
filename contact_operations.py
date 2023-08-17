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


# def abort_with_menu():
#     print(
#         "\n(Enter 'MENU' to return to the main menu or press 'ENTER' to move forward)"
#     )
#     menu_input = input()
#     if menu_input.upper() == "MENU":
#         print("\nAborting to Main Menu...\n")
#         return True
#     else:
#         print("ENTER pressed. Continuing...\n")
#         return False
