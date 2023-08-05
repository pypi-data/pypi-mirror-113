#$Id$

from books.model.PageContext import PageContext

class TimeEntryList:
    """This class is used to create object for Time entrie list."""
    def __init__(self):
        """Initialize parameters for time entries list."""
        self.time_entries = []
        self.page_context = PageContext()

    def set_time_entries(self, time_entry):
        """Set time entries.

        Args:
            time_entry(instance): Time entry object.

        """
        self.time_entries.append(time_entry)
  
    def get_time_entries(self):
        """Get time entries.

        Returns:
            instance: Time entry object.

        """
        return self.time_entries

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

   
