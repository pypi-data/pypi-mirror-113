#$Id$

from books.model.PageContext import PageContext

class EstimateList:
    """This class is used to create object for estimates list."""
    def __init__(self):
        """Initialize parameters for estimates list."""
        self.estimates = []
        self.page_context = PageContext()

    def set_estimates(self, estimate):
        """Set estimates.

        Args:
            estimate(instance): Estimate object.
 
        """
        self.estimates.append(estimate)

    def get_estimates(self):
        """Get estimates.
       
        Returns:
            list of estimetes object.

        """
        return self.estimates

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

