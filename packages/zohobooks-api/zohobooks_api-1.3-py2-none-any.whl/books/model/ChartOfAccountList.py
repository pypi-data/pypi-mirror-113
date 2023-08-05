#$Id$

from books.model.PageContext import PageContext

class ChartOfAccountList:
    """This class is used to create object for Chart of accounts list."""
    def __init__(self):
        """Initialize parameters for chart of accounts list object."""
        self.chartofaccounts = []
        self.page_context = PageContext()

    def set_chartofaccounts(self, chart_of_accounts):
        """Set chart of accounts.

        Args:
            chart_of_accounts(instance): Chart of accounts object.

        """
        self.chartofaccounts.append(chart_of_accounts)

    def get_chartofaccounts(self):
        """Get chart of accounts.

        Returns:
            list of instance: List of chart of accounts object.

        """
        return self.chartofaccounts

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

