#$Id$

class SearchCriteria:
    """This class is used to create object for Criteria."""
    def __init__(self): 
        """Initialize parameter for search criteria."""
        self.column_name = ''
        self.search_text = ''
        self.comparator = ''

    def set_column_name(self, column_name):
        """Set column name.

        Args:
            column_name(str): Column name.

        """
        self.column_name = column_name

    def get_column_name(self):
        """Get column name.

        Returns:
            str: Column name.

        """
        return self.column_name

    def set_search_text(self, search_text):
        """Set search text.

        Args:
            search_text(str): Search text.

        """
        self.search_text = search_text

    def get_search_text(self):
        """Get search text.

        Returns:
            str: Search text.

        """
        return self.search_text

    def set_comparator(self, comparator):
        """Set comparator.
 
        Args:
            comparator(str): Comparator.
 
        """
        self.comparator = comparator

    def get_comparator(self):
        """Get compparator.

        Returns:
            str: Comparator.

        """
        return self.comparator

