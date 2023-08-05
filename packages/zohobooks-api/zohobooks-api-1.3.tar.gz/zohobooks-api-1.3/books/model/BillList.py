#$Id$

from books.model.PageContext import PageContext

class BillList: 
    """This class is used to create object for bill list."""
    def __init__(self):
        """Initialize parameters for bill list object."""
        self.bills = []
        self.page_context = PageContext()

    def set_bills(self, bills):
        """Set bills.
      
        Args:
            bills(instance): Bills object.
 
        """
        self.bills.append(bills)

    def get_bills(self):
        """Get bills.
 
        Returns:
            list of instance: List of bills object.
 
        """
        return self.bills

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

 

