#$Id$

class FromEmail:
    """This class is used to create object for FromEmails."""
    def __init__(self):
        """Initialize parameters for FromEmails."""
        self.user_name = '' 
        self.selected = None
        self.email = '' 
        self.is_org_email_id = None

    def set_user_name(self, user_name):
        """Set the user name.
         
        Args:
            user_name(str): User name. 
        """
        self.user_name = user_name

    def get_user_name(self):
        """Get the user name.
       
        Returns:
            str: User name.
      
        """ 
        return self.user_name
   
    def set_selected(self, selected):
        """Set selected.
        
        Args:
            selected(bool): True if selected else False.
 
        """
        self.selected = selected
 
    def get_selected(self):
        """Get selected.
       
        Returns:
            bool: True if selected else False.
   
        """
        return self.selected
  
    def set_email(self, email):
        """Set email address.
       
        Args:
            email(str): Email address.
       
        """
        self.email = email

    def get_email(self):
        """Get email address.
       
        Returns:
            str: Email address.
 
        """
        return self.email
  
    def set_is_org_email_id(self, is_org_email_id):
        """Set whether it is organization's email id or not.
         
        Args:
            is_org_email_id(bool): True if it is organization's mail 
                id else False.

        """
        self.is_org_email_id = is_org_email_id

    def get_is_org_email_id(self):
        """Get whether it is organization's mail id or not.
 
        Returns:
            bool: True if it is organization's mail id else False.

        """
        return self.is_org_email_id
