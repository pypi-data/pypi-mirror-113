#$Id$#

class InvoiceCreditedList:
    """This class is used to create object for invoice credited list."""
    
    def __init__(self):
        """Initialize parameters for invoice credited list object."""
        self.invoices_credited = [] 

    def set_invoices_credited(self, invoice_credited):
        """Set invoices credited.

        Args:
            invoice_credited(instance): Invoice credited.

        """
        self.invoices_credited.append(invoice_credited)

    def get_invoices_credited(self):
        """Get invoices credited.

        Returns:
            list of instance: List of invoice credited.

        """
        return self.invoices_credited
