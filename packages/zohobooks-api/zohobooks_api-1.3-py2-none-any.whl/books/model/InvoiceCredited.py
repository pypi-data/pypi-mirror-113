#$Id$

class InvoiceCredited:
    """This class is used to create objecctfor Invoices Credited."""
    def __init__(self): 
        """Initialize parameters for Invoices credited."""
        self.creditnote_id = ''
        self.invoice_id = ''
        self.creditnotes_invoice_id = ''
        self.date = ''
        self.invoice_number = ''
        self.creditnotes_number = ''
        self.credited_amount = 0.0
        self.credited_date = ''
        self.amount_applied = 0.0

    def set_creditnote_id(self, creditnote_id):
        """Set credit note id.
      
        Args:
            creditnote_id(str): Credit note id.

        """
        self.creditnote_id = creditnote_id

    def get_creditnote_id(self):
        """Get credit note id.

        Returns:
            str: Credit note id.

        """
        return self.creditnote_id
  
    def set_invoice_id(self, invoice_id):
        """Set invoice id.

        Args:
            invoice_id(str): Invoice id.

        """
        self.invoice_id = invoice_id

    def get_invoice_id(self):
        """Get invoice id.

        Returns:
            str: Invoice id.

        """
        return self.invoice_id

    def set_creditnotes_invoice_id(self, creditnotes_invoice_id):
        """Set credit note invoice id.

        Args:
            creditnotes_invoice_id(str): Credditnote invoice id.

        """
        self.creditnotes_invoice_id = creditnotes_invoice_id
 
    def get_creditnotes_invoice_id(self):
        """Get creditnotes invoice id.

        Returns:
            str: Creditnotes invoice id.

        """
        return self.creditnotes_invoice_id

    def set_date(self, date):
        """Set date.

        Args:
            date(str): Date.

        """
        self.date = date
 
    def get_date(self):
        """Get date.

        Returns:
            str: Date.

        """
        return self.date

    def set_invoice_number(self, invoice_number):
        """Set invoice number.

        Args:
            invoice_number(str): Invoice number.

        """
        self.invoice_number = invoice_number

    def get_invoice_number(self):
        """Get invoice number.
        
        Returns:
            str: Invoice number.

        """
        return self.invoice_number
 
    def set_creditnotes_number(self, creditnotes_number):
        """Set creditnote number.

        Args:
            creditnote_number(str): Creditnote number.

        """
        self.creditnotes_number = creditnotes_number
 
    def get_creditnotes_number(self):
        """Get creditnote number.

        Returns:
            str: Creditnote number.

        """
        return self.creditnotes_number

    def set_credited_amount(self, credited_amount):
        """Set credited amount.

        Args:
            credited_amount(float): Credited amount.

        """
        self.credited_amount = credited_amount

    def get_credited_amount(self):
        """Get credited amount.

        Returns:
            float: Credited amount.
 
        """
        return self.credited_amount

    def set_credited_date(self, credited_date):
        """Set credited date.

        Args:
            credited_date(str): Credited date.

        """
        self.credited_date = credited_date

    def get_credited_date(self):
        """Get credited date.

        Returns: 
            str: Credited date.

        """
        return self.credited_date

    def set_amount_applied(self, amount_applied):
        """Set amount applied.

        Args:
            amount_applied(float): Amount applied.

        """
        self.amount_applied = amount_applied

    def get_amount_applied(self):
        """Get amount applied.

        Returns:
            float: Amount applied.

        """
        return self.amount_applied

   
