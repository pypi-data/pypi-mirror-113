#$Id$

class PageContext:
    """This class is used to create object for page context."""
    def __init__(self):
        """Initialize parameters for page context."""
        self.page = 0
        self.per_page = 0
        self.has_more_page = None
        self.applied_filter = ''
        self.sort_column = ''
        self.sort_order = ''
        self.report_name = ''
        self.search_criteria = []
        self.from_date = ''
        self.to_date = ''

    def set_page(self, page):
        """Set page number for the list.
     
        Args:
            page(int): Page number for list.
 
        """
        self.page = page

    def get_page(self):
        """Get page number for the list.
       
        Returns:
            int: Page number for the list.
 
        """
        return self.page
 
    def set_per_page(self, per_page):
        """Set details per page.
 
        Args:
            per_page(int): Details per page.

        """
        self.per_page = per_page

    def get_per_page(self):
        """Get details per page.
 
        Returns:
            int: Details per page.

        """ 
        return self.per_page

    def set_has_more_page(self, has_more_page):
        """Set has more page.
    
        Args:
            has_more_page(bool): Has more page.

        """
        self.has_more_page = has_more_page

    def get_has_more_page(self):
        """Get has more page.
 
        Returns:
            bool: Has more page.

        """
        return self.has_more_page
  
    def set_applied_filter(self, applied_filter):
        """Set applied filter for the report.
 
        Args:
            applied_filter(str): Applied filter for the report.

        """
        self.applied_filter = applied_filter

    def get_applied_filter(self):
        """Get applied filter for the report.
     
        Returns:
            str: Applied filter for the report.
  
        """
        return self.applied_filter

    def set_sort_column(self, sort_column):
        """Set sort column.
      
        Args: 
            sort_column(str): Sort column.
 
        """
        self.sort_column = sort_column

    def get_sort_column(self):
        """Get sort column.
          
        Returns: 
            str: Sort column.

        """
        return self.sort_column

    def set_sort_order(self, sort_order):
        """Set sort order.
          
        Args:
            sort_order(str): Sort order.
       
        """
        self.sort_order = sort_order

    def get_sort_order(self):
        """Get sort order.
         
        Returns:
            str: Sort order.
  
        """
        return self.sort_order

    def set_report_name(self, report_name):
        """Set report name.
       
        Args: 
            report_name(str): Report name.
     
        """
        self.report_name = report_name

    def get_report_name(self):
        """Get report name.
 
        Returns:
            str: Report name.

        """
        return self.report_name

    def set_search_criteria(self, search_criteria):
        """Set search criteria.

        Args:
            search_criteria(instance): Search criteria object.

        """
        self.search_criteria.append(search_criteria)

    def get_search_criteria(self):
        """Get search criteria.

        Returns:
            list of instance: List of search criteria object.

        """
        return self.search_criteria

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

    def set_to_date(self, to_date):
        """Set to date.

        Args:
            to_date(str): To date.

        """
        self.to_date = to_date

    def get_to_date(self):
        """Get to date.

        Returns: 
            to_date(str): To date.

        """
        return self.to_date
 
   
