#$Id$

from books.model.PageContext import PageContext

class InvoiceList:
    """This class is used to create object for InvoiceList."""
    def __init__(self):
        """Initialize parameters for Invoice list."""
        self.invoice = []
        self.page_context = PageContext()

    def set_invoices(self, invoice):
        """Set Invoices.

        Args:
            invoice(instace): Invoice object.
 
        """
        self.invoice.append(invoice)
 
    def get_invoices(self):
        """Get invoices.

        Returns:
            list of instances: List of invoice object.

        """
        return self.invoice

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
   
