#$Id$

from books.model.PageContext import PageContext

class Statement: 
    """This class is used to create object for statement."""
    def __init__(self): 
        """Initialize parameters for Statement object."""
        self.statement_id = ''
        self.from_date = ''
        self.to_date = ''
        self.source = ''
        self.transactions = []
        self.page_context = PageContext()

    def set_statement_id(self, statement_id): 
        """Set statement id.

        Args:
            statement_id(str): Statement id.
 
        """
        self.statement_id = statement_id

    def get_statement_id(self):
        """Get statement id.

        Returns:
            str: Statement id.

        """
        return self.statement_id

    def set_from_date(self, from_date):
        """Set from date.
 
        Args:
            from_date(str): From date.

        """
        self.from_date = from_date

    def get_from_date(self):
        """Get from date.

        Returns: 
            str: From date.

        """
        return self.from_date

    def set_source(self, source): 
        """Set source.

        Args:
            source(str): Source.

        """
        self.source = source

    def get_source(self):
        """Get source.

        Returns:
            str: Source.

        """
        return self.source

    def set_transactions(self, transactions):
        """Set transactions.

        Args:
            transactions(instance): Transactions object.

        """
        self.transactions.append(transactions)

    def get_transactions(self): 
        """Get transactions.

        Returns:
            list of instance: List of transactions object.

        """
        return self.transaction

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

    def set_to_date(self, to_date):
        """Set to date.
       
        Args:
            to_date(str): To date.

        """
        self.to_date = to_date

    def get_to_date(self):
        """Get to date.

        Returns:
            str: To date.

        """
        return self.to_date 

