#$Id$

class Instrumentation:
    """This class is used tocreate object for instrumentation."""
    def __init__(self):
        """Initialize parameters for Instrumentation object."""
        self.query_execution_time = ''
        self.request_handling_time = ''
        self.response_write_time = ''
        self.page_context_write_time = ''

    def set_query_execution_time(self, query_execution_time):
        """Set query execution time.

        Args:
            query_execution_time(str): Query execution time.
            
        """
        self.query_execution_time = query_execution_time

    def get_query_execution_time(self):
        """Get query execution time.

        Returns:
            str: Query execution time.

        """
        return self.query_execution_time

    def set_request_handling_time(self, request_handling_time): 
        """Set request handling time.
 
        Args:
            request_handling_time(str): Request handling time.

        """
        self.request_handling_time = request_handling_time

    def get_request_handling_time(self): 
        """Get request handling time.

        Returns:
            str: Request handling time.

        """
        return self.request_handling_time

    def set_response_write_time(self, response_write_time):
        """Set response write time.

        Args: 
            response_write_time(str): Response write time.

        """
        self.response_write_time = response_write_time
 
    def get_response_write_time(self):
        """Get response write time.

        Returns:
            str: Response write time.

        """
        return self.response_write_time

    def set_page_context_write_time(self, page_context_write_time):
        """Set page context write time.

        Args: 
            page_context_write_time(str): Page context write time.

        """
        self.page_context_write_time = page_context_write_time

    def get_page_context_write_time(self): 
        """Get page context write time.

        Returns:
            str: Page context write time.

        """
        return self.page_context_write_time

