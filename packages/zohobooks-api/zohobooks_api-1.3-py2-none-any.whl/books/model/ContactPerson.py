#$Id$

class ContactPerson:
    """This class is used to create model for contact person."""
    def __init__(self):
        """Initialize the parameters for contact person."""
        self.contact_person_id = ''
        self.salutation = ''
        self.first_name = ''
        self.last_name = ''
        self.email = ''
        self.phone = ''
        self.mobile = ''
        self.is_primary_contact = None
        self.contact_id = ''

    def set_contact_person_id(self, contact_person_id):
        """Set contact person id.
 
        Args: 
            contact_person_id(str): Contact person id.

        """
        self.contact_person_id = contact_person_id

    def get_contact_person_id(self):
        """Get contact person id.
 
        Returns:
            str: Contact person id.

        """
        return self.contact_person_id
  
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
 
    def set_mobile(self, mobile):
        """Set mobile.

        Args:
            mobile(str): Mobile.

        """
        self.mobile = mobile

    def get_mobile(self):
        """Get mobile.

        Args: 
            mobile(str): Mobile.

        """
        return self.mobile
  
    def set_is_primary_contact(self, is_primary_contact):
        """Set whether it is primary contact or not.

        Args:
            is_primary_contact(bool): True if it is primary contact. 
                Allowed value is true only.

        """
        self.is_primary_contact = is_primary_contact

    def get_is_primary_contact(self):
        """Get whether it is primary contact or not.

        Returns:
            bool: True if it os primary contact else False.

        """
        return self.is_primary_contact

    def set_contact_id(self, contact_id):
        """Set contact id.
 
        Args:
            contact_id(str): Contact id.

        """
        self.contact_id = contact_id

    def get_contact_id(self):
        """Get contact id.

        Returns: 
            str: Contact id.

        """
        return self.contact_id

    def to_json(self):
        """This method is used to convert the contact person object to JSON object.

        Returns:
            dict: Dictionary containing details of contact person object.

        """
        contact_person = {}
        if self.salutation != '':
            contact_person['salutation'] = self.salutation
        if self.first_name != '':
            contact_person['first_name'] = self.first_name
        if self.last_name != '':
            contact_person['last_name'] = self.last_name
        if self.email != '':
            contact_person['email'] = self.email
        if self.phone != '':
            contact_person['phone'] = self.phone
        if self.mobile != '':
            contact_person['mobile'] = self.mobile
        if self.is_primary_contact != False:
            contact_person['is_primary_contact'] = str(\
            self.is_primary_contact).lower()
        if self.contact_id != '': 
            contact_person['contact_id'] = self.contact_id
        return contact_person
