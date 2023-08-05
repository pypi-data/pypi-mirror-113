#$Id$

class CustomField:
    """This class is used to create custom field."""
    def __init__(self):
        """Initialize the parameters for custom field object"""
        self.index = 0
        self.show_on_pdf = None
        self.value = ''
        self.label = ''
  
    def set_index(self, index):
        """Set index for custom field.
        
        Args:
            index(int): Index for custom field.
 
        """
        self.index = index

    def get_index(self):
        """Get index for custom field.
        
        Returns:
            int: Index for custom field.
  
        """
        return self.index
 
    def set_show_on_pdf(self, show_on_pdf):
        """Set whether to show as pdf or not.
 
        Args:
            show_on_pdf(bool): True to show as pdf else False.

        """
        self.show_on_pdf = show_on_pdf
    def get_show_on_pdf(self):
        """Get whether to show as pdf or not.
    
        Returns:
            bool: True to show as pdf else False.

        """
        return self.show_on_pdf

    def set_value(self, value):
        """Set value for custom field.
 
        Args:
            value(str): Value for custom field.

        """
        self.value = value

    def get_value(self):
        """Get value of custom field.
     
        Returns:
            str: Value for custom field.

        """
        return self.value
 
    def set_label(self, label):
        """Set label for custom field.
          
        Args:
            label(str): Label for custom field.

        """
        self.label = label

    def get_label(self):
        """Get label of custom field.
      
        Returns:
            str: Label of custom field.
 
        """
        return self.label

    def set_invoice(self, invoice):
        """Set invoice.

        Args:
            invoice(instance): Invoice custom field.

        """
        self.invoice.append(invoice)

    def get_invoice(self):
        """Get invoice.

        Returns: 
            list of instance: List of Invoice custom field.

        """
        return self.invoice
  
    def set_contact(self, contact):
        """Set cocntact.

        Args: 
            contact(instance): Contact custom field.

        """
        self.contact.append(contact)

    def get_contact(self):
        """Get contact.

        Returns: 
            list of instance: List of Contact custom field.

        """
        return self.custom_field

    def set_estimate(self, estimate): 
        """Set estimate.

        Args:
            estimate(instance): Estimate custom field.

        """
        self.estimate.append(estimate)

    def get_estimate(self):
        """Get estimate.

        Returns:
            list of instance: List of estimate custom field.

        """
        return self.estimate

    def to_json(self):
        """This method is used to convert custom field object to json object.

        Returns:
            dict: Dictionary containing json object for custom field.

        """
        data = {}
        #if self.index != None:
            #data['index'] = self.index
        if self.value != '':
            data['value'] = self.value
            data['api_name'] = self.label
        return data

