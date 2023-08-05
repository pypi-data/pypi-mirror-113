#$Id$

from books.model.PageContext import PageContext

class BankAccountList:
    """This class is used to create object for Bank accounts list."""
    def __init__(self):
        """Initialize the parameters for Bank accounts list."""
        self.bank_accounts = []
        self.page_context = PageContext()

    def set_bank_accounts(self, bank_accounts): 
        """Set Bank accounts.
    
        Args:
            bank_accounts(instance): Bank accounts object.

        """
        self.bank_accounts.append(bank_accounts)

    def get_bank_accounts(self):
        """Get bank accounts.

        Returns:
            list of instance: List of bank accounts object.

        """
        return self.bank_accounts

    def set_page_context(self, page_context): 
        """Set page context.

        Args:
            page_context(instance): Page context object.
         
        """
        self.page_context = page_context

    def get_page_context(self):
        """Get page_context.
 
        Returns:
            instance: Page context object.

        """
        return self.page_context

 
