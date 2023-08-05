#$Id$

from books.model.PageContext import PageContext

class ContactPersonList:
    """This class is used to create object for contact person list."""
    def __init__(self):
        """Initialize the parameters for contact person list.""" 
        self.contact_person = []
        self.page_context = PageContext()

    def set_contact_persons(self, contact_person):
        """Set contact persons.
        
        Args:
            contact_person(instance): Contact person object.

        """ 
        self.contact_person.append(contact_person)

    def get_contact_persons(self):
        """Get contact person.
       
        Returns: 
            list: List of contact persons list.
      
        """
        return self.contact_person
  
    def set_page_context(self, page_context):
        """Set page context.
        
        Args:
            page_context(instance): Page_context object.
       
        """
        self.page_context = page_context
 
    def get_page_context(self):
        """Get page context.
        
        Returns:  
            instance: Page context object.

        """
        return self.page_context


