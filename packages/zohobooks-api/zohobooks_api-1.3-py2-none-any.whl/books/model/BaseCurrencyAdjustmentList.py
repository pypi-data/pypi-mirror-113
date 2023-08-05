#$Id$

from books.model.PageContext import PageContext

class BaseCurrencyAdjustmentList:
    """This class is used to creste object for Base Currency Adjustment List."""
    def __init__(self):
        """Initialize parameters for Base Currency list object."""
        self.base_currency_adjustments = []
        self.page_context = PageContext()

    def set_base_currency_adjustments(self, base_currency_adjustment):
        """Set base currency adjustment.

        Args:
            base_currency_adjustment(instance): Base currency adjustment object.

        """
        self.base_currency_adjustments.append(base_currency_adjustment)
 
    def get_base_currency_adjustments(self): 
        """Get base currency adjustments.

        Returns:
            list of instance: List of base currency adjustments.

        """
        return self.base_currency_adjustments

    def set_page_context(self, page_context):
        """Set page context.

        Args:
            page_context(instance): Page context object.

        """
        self.page_context = page_context

    def get_page_context(self):
        """Get page context.

        Returns:
            instance: Page context.

        """
        return self.page_context

