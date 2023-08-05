#$Id$

from books.model.PageContext import PageContext

class CurrencyList:
    """This class is used to create object for currency list."""
    def __init__(self):
        """Initialize parameters for currency list."""
        self.currencies = []
        self.page_context = PageContext()

    def set_currencies(self, currency):
        """Set currencies.

        Args:
            currency(instance): Currency object.

        """
        self.currencies.append(currency)
 
    def get_currencies(self):
        """Get currencies.

        Returns:
            list of instance: List of currency object.

        """
        return self.currencies

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


