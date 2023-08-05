#$Id$

from books.model.PageContext import PageContext

class TaxList:
    """This class is used to create object for tax list."""
    def __init__(self):
        """Initialize parameters for tax list."""
        self.taxes = []
        self.page_context = PageContext()

    def set_taxes(self, tax):
        """Set taxes.
 
        Args:
            tax(instance): Tax object.

        """
        self.taxes.append(tax)

    def get_taxes(self):
        """Get taxes.

        Returns:
            list of instance: List of Tax object.

        """
        return self.taxes

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
