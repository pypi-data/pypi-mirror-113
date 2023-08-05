#$Id$

class Term:
    """This class is used to create object for terms."""
    def __init__(self):
        """Initialize parameters for terms."""
        self.invoice_terms = ''
        self.estimate_terms = ''
        self.creditnotes_terms = ''

    def set_invoice_terms(self, invoice_terms):
        """Set invoice terms.

        Args:
            invoice_terms(str): Invoice terms.

        """
        self.invoice_terms = invoice_terms

    def get_invoice_terms(self): 
        """Get invoice terms.

        Returns: 
            str: Invoice terms.

        """ 
        return self.invoice_terms

    def set_estimate_terms(self, estimate_terms):
        """Set estimate terms.

        Args:
            estimate_terms(str): Estimate terms.

        """
        self.estimate_terms = estimate_terms

    def set_creditnote_terms(self, creditnote_terms):
        """Set creditnote terms.

        Args:
            creditnote_terms(str): Creditnote terms.

        """
        self.creditnote_terms = creditnote_terms

    def get_creditnote_terms(self):
        """Get creditnote terms.

        Returns:
            str: Creditnote terms.

        """
        return self.creditnote_terms

