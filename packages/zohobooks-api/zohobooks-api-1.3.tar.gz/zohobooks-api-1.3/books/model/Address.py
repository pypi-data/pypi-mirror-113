#$Id$

class Address:
    """This class is used to create an object for Address."""
    def __init__(self):
        """Initialize parameters for address object"""
        self.address = ''
        self.city = ''
        self.state = ''  
        self.zip = ''
        self.country = ''
        self.fax = ''
        self.is_update_customer = None
        self.street_address1 = ''
        self.street_address2 = ''

    def set_address(self, address):
        """Set address.
        
        Args:
            address(str): Address.
         
        """
        self.address = address

    def get_address(self):
        """Get address.
        
        Returns:
            str: Address.

        """
        return self.address
  
    def set_city(self, city):
        """Set city.

        Args:
            str: City.
         
        """
        self.city = city

    def get_city(self):
        """Get city.
    
        Returns:
            str: City.
        
        """
        return self.city
  
    def set_state(self, state):
        """Set state.
        
        Args:
            state(str): State.

        """
        self.state = state

    def get_state(self):
        """Get the state.
        
        Returns:
            str: State.
        
        """
        return self.state
  
    def set_zip(self, zip_code):
        """Set zip.
 
        Args:
            zip_code(str): Zip code.
        
        """
        self.zip = zip_code
 
    def get_zip(self):
        """Get zip.
     
        Returns:
            str: Zip code.

        """
        return self.zip
  
    def set_country(self, country):
        """Set country.
        
        Args:
            country(str): Country.
     
        """
        self.country = country
     
    def get_country(self):
        """Get country.
     
        Returns:
            str: Country.
        
        """
        return self.country
  
    def set_fax(self, fax):
        """Set fax.
       
        Args:
            fax(str): Fax.
      
        """
        self.fax = fax

    def get_fax(self):
        """Get fax.
 
        Returns:
            str: Fax.
      
        """  
        return self.fax
 
    def set_is_update_customer(self, is_update_customer):
        """Set whether to update customer.
        
        Args:
            is_update_customer(bool): True to update customer else False.
         
        """
        self.is_update_customer = is_update_customer

    def get_is_update_customer(self):
        """Get is update customer
      
        Returns:
            bool: True to update customer else False.
        
        """
        return self.is_update_customer

    def set_street_address1(self, street_address1):
        """Set street address1.

        Args:
            street_address1(str): Street address 1.

        """
        self.street_address1 = street_address1

    def get_street_address1(self):
        """Get street address1.

        Returns:
            str: Street address 1.

        """
        return self.street_address1

    def set_street_address2(self, street_address2):
        """Set street address 2.

        Args:
            street_address2(str): street address 2.

        """
        self.street_address2 = street_address2

    def get_street_address2(self):
        """Get street address 2.

        Returns:
            str: Street address 2.

        """
        return self.street_address2

    def to_json(self):
        """This method is used to convert the address object to JSON object.

        Returns:
            dict: Dictionary containing details of address object.

        """
        address = {}
        if self.street_address1 != '':
            address['street_address1'] = self.street_address1
        if self.street_address2 != '':
            address['street_address2'] = self.street_address2
        if self.address != '':
            address['address'] = self.address
        if self.city != '':
            address['city'] = self.city
        if self.state != '':
            address['state'] = self.state
        if self.zip != '':
            address['zip'] = self.zip
        if self.country != '':  
            address['country'] = self.country
        if self.fax != '':
            address['fax'] = self.fax
        return address
