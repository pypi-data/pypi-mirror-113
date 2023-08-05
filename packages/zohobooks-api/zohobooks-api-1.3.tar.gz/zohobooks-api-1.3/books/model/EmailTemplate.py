#$Id$

class EmailTemplate:
    """This class is used to create object for email templates."""
    def __init__(self):
        """Initialize parameters for email templates."""
        self.selected = None
        self.name = ''
        self.email_template_id = ''
   
    def set_selected(self, selected):
        """Set whether to select or not.

        Args:
            selected(bool): True to select else False.

        """
        self.selected = selected
 
    def get_selected(self):
        """Get whether to select or not.

        Returns:
            bool: True to select else False.

        """
        return self.selected
 
    def set_name(self, name):
        """Set name.

        Args:
            name(str): Name.

        """
        self.name = name

    def get_name(self):
        """Get name.

        Returns:
            str: Name.

        """
        return self.name

    def set_email_template_id(self, email_template_id):
        """Set email template id.

        Args: 
            email_template_id(str): Email template id.

        """
        self.email_template_id = email_template_id

    def get_email_template_id(self):
        """Get email template id.

        Returns:
            str: Email template id.

        """
        return self.email_template_id

   
