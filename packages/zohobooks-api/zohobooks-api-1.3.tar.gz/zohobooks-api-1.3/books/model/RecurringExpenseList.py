#$Id$

from books.model.PageContext import PageContext

class RecurringExpenseList:
    """This class is used to create object for recurring expenses list."""
    def __init__(self):
        """Initialize parameters for recurring expenses list object."""
        self.recurring_expenses = []
        self.page_context = PageContext()
 
    def set_recurring_expenses(self, recurring_expenses):
        """Set recurring expenses.

        Args:
            recurring_expenses(instance): Recurring expenses object.

        """
        self.recurring_expenses.append(recurring_expenses)
 
    def get_recurring_expenses(self):
        """Get recurring expenses.

        Returns:
            list of instance: List of recurring expenses object.

        """
        return self.recurring_expenses

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


