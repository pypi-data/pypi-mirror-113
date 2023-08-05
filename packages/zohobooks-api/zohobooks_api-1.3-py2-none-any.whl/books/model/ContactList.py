#$Id$

from books.model.PageContext import PageContext

class ContactList:
    """This class is used to create an object for contact list."""
    def __init__(self):
        """ Initialize contacts list and page context."""
        self.contacts = []
        self.page_context = PageContext()

    def set_contacts(self, contact):
        """Insert contact object to contacts list.
        
        Args:
            contact(instance): Contact object.
   
        """
        self.contacts.append(contact)

    def get_contacts(self):
        """Get contacts list.
        
        Returns:
            list: List of contacts object.
        
        """
        return self.contacts
 
    def set_page_context(self, page_context):
        """Set page context.
        
        Args:
            instance: Page_context object.
        
        """
        self.page_context = page_context
     
    def get_page_context(self):
        """Get page context.
        
        Returns:
            instance: Page context object.
       
        """
        return self.page_context


