#$Id$

class PlaceHolder:
    """This class is used to create object for place holders."""
    def __init__(self):
        """Initialize parameters for place holders."""
        self.invoice = []
        self.customer = []
        self.organization = []

    def set_invoice(self, invoice):
        """Set invoice.

        Args:
            invoice(instance): Invoice object.

        """
        self.invoice.append(invoice)

    def get_invoice(self):
        """Get invoice.

        Returns:
            List of instance: List of Invoice object.

        """
        return self.invoice

    def set_customer(self, customer):
        """Set customer.

        Args:
            customer(instance): Customer object.

        """
        self.customer.append(customer)

    def get_customer(self):
        """Get customer.

        Returns:        
            List of instance: List of customer object.

        """
        return self.customer

    def set_organization(self, organization):
        """Set organization.

        Args:
            organization(instance): Organization object.

        """
        self.organization.append(organization)

    def get_organization(self):
        """Get organization.
       
        Returns:
            List of instance: List of organization object.

        """
        return self.organization

