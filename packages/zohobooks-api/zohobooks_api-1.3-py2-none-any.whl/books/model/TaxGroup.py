#$Id$

class TaxGroup:
    """This class is used to create object for tax group."""
    def __init__(self):
        """Initialize parameters for tax group. """
        self.tax_group_id = ''
        self.tax_group_name = ''
        self.tax_group_percentage = 0
        self.taxes = ''

    def set_tax_group_id(self, tax_group_id):
        """Set tax group id.

        Args:
            tax_group_id(str): Tax group id.

        """
        self.tax_group_id = tax_group_id

    def get_tax_group_id(self):
        """Get tax group id.

        Returns:
            str: Tax group id.

        """
        return self.tax_group_id

    def set_tax_group_name(self, tax_group_name):
        """Set tax group name.

        Args:
            tax_group_name(str): Tax group name.

        """
        self.tax_group_name = tax_group_name

    def get_tax_group_name(self):
        """Get tax group name.

        Returns:
            str: Tax group name.

        """
        return self.tax_group_name

    def set_tax_group_percentage(self, tax_group_percentage):
        """Set tax group percentage.

        Args:
            tax_group_percentage(int): Tax group percentage.

        """ 
        self.tax_group_percentage = tax_group_percentage

    def get_tax_group_percentage(self):
        """Get tax group percentage.

        Returns:
            int: Tax group percentage.

        """
        return self.tax_group_percentage

    def set_taxes(self, taxes):
        """Set taxes.

        Args:
            taxes(str): Taxes.

        """
        self.taxes = taxes

    def get_taxes(self):
        """Get taxes.

        Returns:
            str: Taxes.

        """ 
        return self.taxes
 
    def to_json(self):
        """This method is used to create json object for tax group.

        Returns:
            dict: Dictionary containing json object for tax group.

        """
        data = {}
        if self.tax_group_name != '':
            data['tax_group_name'] = self.tax_group_name
        if self.taxes != '':
            data['taxes'] = self.taxes
        return data
