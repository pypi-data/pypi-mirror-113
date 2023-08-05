#$Id$

from books.model.PageContext import PageContext

class ExpenseList:
    """This class is used to create object for Expenses List."""
    def __init__(self):
        """Initialize parameters for Expenses list object."""
        self.expenses = []
        self.page_context = PageContext()

    def set_expenses(self, expense):
        """Set expenses.

        Args:
            expense(instance): Expense object.

        """
        self.expenses.append(expense)

    def get_expenses(self):
        """Get expenses.

        Returns:
            list of instance: List of expense object.

        """
        return self.expenses

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
