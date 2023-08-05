#$Id$

class ToContact:
    """This class is used to create object for to Contacts."""
    def __init__(self):
        """Initialize parameters for to contacts."""
        self.first_name = ''
        self.selected = None
        self.phone = ''
        self.email = ''
        self.last_name = ''
        self.salutation = ''
        self.contact_person_id = ''
        self.mobile = ''

    def set_first_name(self, first_name):
        """Set first name.
  
        Args:
            first_name(str): First name. 
 
        """
        self.first_name = first_name

    def get_first_name(self):
        """Get first name.
     
        Returns:
            str: First name.

        """
        return self.first_name
  
    def set_selected(self, selected):
        """Set selected.
          
        Args:
            selected(bool): Selected.
 
        """
        self.selected = selected

    def get_selected(self):
        """Get selected.
        
        Returns:
            bool: Selected.
        
        """
        return self.selected

    def set_phone(self, phone): 
        """Set phone.
          
        Args:
            phone(str): Phone.
 
        """
        self.phone = phone

    def get_phone(self):
        """Get phone.
 
        Returns:
            str: Phone.

        """
        return self.phone

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
  
    def set_last_name(self, last_name):
        """Set last name.
        
        Args:
            last_name(str): Last name.

        """
        self.last_name = last_name

    def get_last_name(self):
        """Get last name.

        Returns:
            str: Last name.

        """
        return self.last_name
  
    def set_salutation(self, salutation):
        """Set salutation.
 
        Args:
            salutation(str): Salutation.
    
        """        
        self.salutation = salutation

    def get_salutation(self):
        """Get salutation.
         
        Returns:
            str: Salutation.
        
        """
        return self.salutation
  
    def set_contact_person_id(self, contact_person_id):
        """Set contact person id.
      
        Args:
            contact_person_id(str): Contact person id.

        """
        self.contact_person_id = contact_person_id

    def get_contact_person_id(self):
        """Get person id.
 
        Returns:
            str: Contact person id.

        """
        return self.contact_person_id

    def set_mobile(self, mobile):
        """Set mobile.
  
        Args:
            mobile(str): Mobile.

        """
        self.mobile = mobile

    def get_mobile(self):
        """Get mobile.
  
        Returns:
            str: Mobile.

        """
        return self.mobile

  


