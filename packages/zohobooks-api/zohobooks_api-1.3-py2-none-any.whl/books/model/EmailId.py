#$Id$

class EmailId:
    """This class is used to create object for email ids."""
    def __init__(self):
        """Initialize parameters for email ids."""
        self.email = ''
        self.is_selected = None

    def set_email(self, email):
        """Set email.

        Args:
            email(str): Email.
        
        """
        self.email = email

    def get_email(self):
        """Get email.

        Returns:
            str: Email.

        """
        return self.email

    def set_is_selected(self, is_selected):
        """Set whether selected or not.

        Args:
            is_selected(bool): True if selected else false.

        """
        self.is_selected = is_selected

    def get_is_selected(self):
        """Get whether selected or not.

        Returns:
            bool: True if selected else false.

        """ 
        return self.is_selected

