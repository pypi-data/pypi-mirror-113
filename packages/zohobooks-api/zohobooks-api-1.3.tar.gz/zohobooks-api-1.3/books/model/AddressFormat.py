#$Id$

class AddressFormat: 
    """This class is used to create object for Address Formats."""
    def __init__(self): 
        """Initialize parameters for address formats."""
        self.organization_address_format = ''
        self.customer_address_format = ''

    def set_organization_address_format(self, organization_address_format):
        """Set organization address format.

        Args: 
            organization_address_format(str): Organization address format.

        """
        self.organization_address_format = organization_address_format

    def get_organization_address_foramt(self):
        """Get organization address format.

        Returns:
            str: Organization address format.

        """
        return self.organization_address_format

    def set_customer_address_format(self, customer_address_format):
        """Set customer address format.

        Args:
            customer_address_format(str): Customer address format.

        """
        self.customer_address_format = customer_address_format

    def get_customer_address_format(self):
        """Get customer address format.

        Returns:
            str: Customer address format.

        """
        return self.customer_address_format
