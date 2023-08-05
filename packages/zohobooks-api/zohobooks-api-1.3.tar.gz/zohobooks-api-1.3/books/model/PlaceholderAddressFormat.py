#$Id$

from books.model.Organization import Organization
from books.model.Customer import Customer

class PlaceholderAddressFormat:
    """This class is used to create object for Palceholders Address Format."""
    def __init__(self):
        """Initialize parameters for placeholders address format."""
        self.organization = Organization()
        self.customer = Customer()

    def set_organization(self, organization):
        """Set organization.

        Args:
            organization(instance): Organization object.

        """
        self.organization = Organization()
 
    def get_organization(self):
        """Get organization.

        Returns:
            instance: Organization object.

        """ 
        return self.organization

    def set_customer(self, customer):
        """Set customer.

        Args:
            customer(instance):Customer object.

        """
        self.customer = customer

    def get_customer(self):
        """Get customer.

        Returns:
            instance: Customer object.

        """
        return self.customer

