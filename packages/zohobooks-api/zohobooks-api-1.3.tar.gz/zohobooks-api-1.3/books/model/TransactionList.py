#$Id$

from books.model.PageContext import PageContext
from books.model.Instrumentation import Instrumentation

class TransactionList: 
    """This class is used to create object for Transaction list."""
    def __init__(self):
        """Initialize parameters for Transaction list object."""
        self.transactions = []
        self.page_context = PageContext()
        self.Instrumentation = Instrumentation()

    def set_transactions(self, transaction):
        """Set transactions.

        Args:
            transaction(instance): Transaction object.

        """
        self.transactions.append(transaction)

    def get_transactions(self):
        """Get transactions.

        Returns:
            list of instance: List of transactions object.

        """
        return self.transactions

    def set_page_context(self, page_context):
        """Set page context.

        Args:
            page_context(instance): Page context  

        """
        self.page_context = page_context

    def get_page_context(self):
        """Get page context.
 
        Returns:
            instance: Page context object.

        """
        return self.page_context

    def set_instrumentation(self, instrumentation):
        """Set instrumentation.

        Args:
            instrumentation(instance): Instrumentation object.
     
        """
        self.instrumentation = instrumentation

    def get_instrumentation(self): 
        """Get instrumentation.

        Returns:
            instance: Instrumentation object.

        """
        return self.instrumentation

 
