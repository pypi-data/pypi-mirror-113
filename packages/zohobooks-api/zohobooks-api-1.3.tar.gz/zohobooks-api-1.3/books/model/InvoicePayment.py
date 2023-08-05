#$Id$

class InvoicePayment:
    """This class is used to create object for Invoice Payments."""
    def __init__(self):
        """Initialize parameters for Invoice payments."""
        self.invoice_payment_id = ''  
        self.payment_id = ''
        self.invoice_id = ''
        self.amount_used = 0.0
        self.amount_applied = 0.0 
        self.payment_number = ''
        self.payment_mode = ''
        self.description = ''
        self.date = ''
        self.reference_number = ''
        self.exchange_rate = 0.00
        self.amount = 0.00
        self.tax_amount_withheld = 0.0
        self.is_single_invoice_payment = None
    
    def set_invoice_payment_id(self, invoice_payment_id):
        """Set invoice payment id.

        Args:
            invoice_payment_id(str): Invoice payment id.

        """
        self.invoice_payment_id = invoice_payment_id

    def get_invoice_payment_id(self):
        """Get invoice payment id.

        Returns:
            str: Invoice payment id.

        """
        return self.invoice_payment_id
   
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

    def set_payment_id(self, payment_id):
        """Set payment id.

        Args:
            payment_id(str): Payment id.

        """
        self.payment_id = payment_id

    def get_payment_id(self):
        """Get payment id.

        Returns:
            str: Payment id.

        """
        return self.payment_id
    
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

    def set_amount_used(self, amount_used):
        """Set amount used.

        Args:
            amount_used(float): Amount used.

        """
        self.amount_used = amount_used
 
    def get_amount_used(self): 
        """Get amount used.

        Returns:
            float: Amount used.

        """
        return self.amount_used

    def set_payment_number(self, payment_number):
        """Set payment number.

        Args:
            payment_number(str): Payment number.

        """
        self.payment_number = payment_number

    def get_payment_number(self): 
        """Get payment number.

        Returns:
            str: Payment number.

        """
        return self.payment_number
   
    def set_payment_mode(self, payment_mode):
        """Set payment mode.

        Args: 
            payment_mode(str): Payment mode.

        """
        self.payment_mode = payment_mode

    def get_payment_mode(self):
        """Get payment mode.

        Returns:
            str: Payment mode.

        """
        return self.payment_mode

    def set_description(self, description):
        """Set description.

        Args:
            description(str): Description.

        """
        self.description = description

    def get_description(self):
        """Get description.

        Returns:
            str: Description.

        """
        return self.description

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

    def set_reference_number(self, reference_number):
        """Set reference number.

        Args:
            reference_number(str): Reference number.

        """
        self.reference_number = reference_number

    def get_reference_number(self):
        """Get reference number.

        Returns: 
            str: Reference number.

        """
        return self.reference_number
  
    def set_exchange_rate(self, exchange_rate):
        """Set exchange rate.

        Args: 
            exchange_rate(float): Exchange rate.

        """
        self.exchange_rate = exchange_rate

    def get_exchange_rate(self):
        """Get exchange rate.

        Returns:
            float: Exchange rate.

        """
        return self.exchange_rate
    
    def set_amount(self, amount):
        """Set amount.

        Args:
            amount(float): Amount.

        """
        self.amount = amount

    def get_amount(self):
        """Get amount.
    
        Returns:
            float: Amount.
 
        """ 
        return self.amount

    def set_tax_amount_withheld(self, tax_amount_withheld):
        """Set tax amount withheld.

        Args:
            tax_amount_withheld(float): Tax amount withheld.

        """
        self.tax_amount_withheld = tax_amount_withheld

    def get_tax_amount_withheld(self):
        """Get tax amount withheld.

        Returns:
            float: Tax amount withheld.

        """
        return self.tax_amount_withheld
 
    def set_is_single_invoice_payment(self, is_single_invoice_payment):
        """Set whether it is single invoice payment.

        Args:
            is_single_invoice_payment(bool): True if it is single invoice 
                 payment else False.

        """
        self.is_single_invoice_payment = is_single_invoice_payment

    def get_is_single_invoice_payment(self):
        """Get whether it is single invoice payment.

        Returns:
            bool: True if it is single invoice payment else False.

        """
        return self.is_single_invoice_payment
  
