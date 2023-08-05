#$Id$

class Tax:
    """This class is used to create an object for tax."""
    def __init__(self):
        """Initialize parameters for tax."""
        self.tax_name = ''
        self.tax_amount = 0.0
        self.tax_id = ''
        self.tax_percentage = 0.0
        self.tax_type = ''
        self.tax_specification = ''

    def set_tax_id(self, tax_id):
        """Set tax id.

        Args:
            tax_id(str): Tax id.

        """ 
        self.tax_id = tax_id

    def get_tax_id(self):
        """Get tax id.

        Returns:
            str: Tax id.

        """
        return self.tax_id

    def set_tax_percentage(self, tax_percentage):
        """Set tax percentage.

        Args:
            tax_percentage(float): Tax percentage.

        """
        self.tax_percentage = tax_percentage

    def get_tax_percentage(self):
        """Get tax percentage.

        Args:
            float: Tax percentage.

        """
        return self.tax_percentage
   
    def set_tax_type(self, tax_type):
        """Set tax type.

        Args:
            tax_type(str): Tax type.

        """
        self.tax_type = tax_type

    def get_tax_type(self):
        """Get tax type.

        Returns:
            str: Tax type.
 
        """
        return self.tax_type
  
    def set_tax_name(self, tax_name):
        """Set tax name.

        Args:
            tax_name(str): Tax name.
 
        """
        self.tax_name = tax_name

    def get_tax_name(self):
        """Get tax name.

        Returns:
            str: Tax name.

        """
        return self.tax_name

    def set_tax_amount(self, tax_amount):
        """Set tax amount.
 
        Args:
            tax_amount(float): Tax amount.

        """
        self.tax_amount = tax_amount

    def get_tax_amount(self):
        """Get tax amount.

        Returns:
            float: Tax amount.

        """
        return self.tax_amount

    def set_tax_specification(self, tax_specification):
        """Set tax Specification.

        Args:
            tax_specification(str): Tax Specification.

        """
        self.tax_specification = tax_specification

    def get_tax_specification(self):
        """Get tax Specification.

        Returns:
            str: Tax Specification.

        """
        return self.tax_specification

    def to_json(self):
        """This method is used to convert tax object to json format.

        Returns:
            dict: Dictionary containing json object for tax.

        """
        data = {}
        if self.tax_name != '':
            data['tax_name'] = self.tax_name
        if self.tax_percentage > 0:
            data['tax_percentage'] = self.tax_percentage
        if self.tax_type != '':
            data['tax_type'] = self.tax_type
        return data


