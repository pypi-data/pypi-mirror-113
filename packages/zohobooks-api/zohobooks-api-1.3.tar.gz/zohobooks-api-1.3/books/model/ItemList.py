#$Id$

from books.model.PageContext import PageContext

class ItemList:
    """This class is used to create object for Items list."""
    def __init__(self):
        """Initialize parameters for Items list."""
        self.items = []
        self.page_context = PageContext()

    def set_items(self, item):
        """Set items.

        Args:
            item(instance): Item object.

        """
        self.items.append(item)

    def get_items(self):
        """Get items.

        Returns:
            list of instance: List of items object.

        """
        return self.items

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
