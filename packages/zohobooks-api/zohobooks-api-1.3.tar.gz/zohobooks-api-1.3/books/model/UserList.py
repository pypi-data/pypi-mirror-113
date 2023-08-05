#$Id$

from books.model.PageContext import PageContext

class UserList: 
    """This class is used to create object for Users list."""
    def __init__(self):
        """Initialize parameters for users."""
        self.users = []
        self.page_context = PageContext()

    def set_users(self, user):
        """Set users.

        Args:
            user(instance): User object.

        """
        self.users.append(user)

    def get_users(self):
        """Get users.

        Returns:
            list of instance: List of user objects.

        """
        return self.users

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

