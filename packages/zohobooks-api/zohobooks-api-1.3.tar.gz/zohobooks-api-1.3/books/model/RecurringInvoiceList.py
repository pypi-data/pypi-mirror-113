#$Id$

from books.model.PageContext import PageContext

class RecurringInvoiceList:
    """This class is used to create object for Recurring invoice list."""
    def __init__(self):
        """Initialize parameters for Recurring invoice list."""  
        self.recurring_invoices = []
        self.page_context = PageContext()
   
    def set_recurring_invoices(self, recurring_invoices):
        """Set recurring invoice.

        Args:
            recurring_invoices(instance): Recurring invoice object.

        """
        self.recurring_invoices.extend(recurring_invoices)
 
    def get_recurring_invoices(self):
        """Get recurring invoice.

        Returns:
            list: List of recurring invoice objects.

        """
        return self.recurring_invoices

    def set_page_context(self, page_context):
        """Set page context.

        Args: 
            page_context(instance): Page context instance.

        """
        self.page_context = page_context

    def get_page_context(self): 
        """Get page context.

        Returns:
            instance: Page context instance.
     
        """
        return self.page_context

