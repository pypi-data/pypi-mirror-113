#$Id$

from books.model.PageContext import PageContext

class JournalList:
    """This class is used to create object for journals list."""
    def __init__(self):
        """Initialize parameters for Journals list object."""
        self.journals = []
        self.page_context = PageContext()

    def set_journals(self, journal):
        """Set journals.

        Args:
            journal(instance): Journal object.

        """
        self.journals.append(journal)

    def get_journals(self):
        """Get journals.

        Returns:
            list of instance: List of journals object.

        """
        return self.journals

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

 

