#$Id$

from books.model.PageContext import PageContext

class CreditNoteList:
    """This class is used to create object for credit notes list."""
    def __init__(self):
        """Initialize the parameters for credditnotes list."""
        self.creditnotes = []
        self.page_context = PageContext()

    def set_creditnotes(self, creditnotes):
        """Set credit notes.

        Args:
            creditnotes(list): List of credit notes.

        """ 
        self.creditnotes.extend(creditnotes)
 
    def get_creditnotes(self):
        """Get creditnotes.
    
        Returns:
            list of instance: List of credit notes.

        """
        return self.creditnotes

    def set_page_context(self, page_context):
        """Set page context.

        Args:
            page_context(instance): Page context object.

        """
        self.page_context = page_context

    def get_page_context(self):
        """Get page context.

        Returns:
            instance: Page context object.

        """
        return self.page_context

  
