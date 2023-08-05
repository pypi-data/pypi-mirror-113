#$Id$

class BillPayment:
    """This class is used to create object for payments."""
    def __init__(self):
        """Initialize parameters for Payments object."""
        self.payment_id = ''
        self.bill_id = ''
        self.bill_payment_id = ''
        self.payment_mode = ''
        self.description = ''
        self.date = ''
        self.reference_number = ''
        self.exchange_rate = 0.0
        self.amount = 0.0
        self.paid_through_account_id = ''
        self.paid_through_account_name = ''
        self.is_single_bill_payment = None
        self.amount_applied = 0.0
        self.vendor_id = ''
        self.vendor_name = ''
        self.paid_through = ""
      
    def set_paid_through(self, paid_through):
        """Set paid through.

        Args:
            paid_through(str): Paid through.

        """
        self.paid_through = paid_through

    def get_paid_through(self):
        """Get paid through.

        Returns:
            str: Paid through.

        """
        return self.paid_through
    
    def set_vendor_name(self, vendor_name):
        """Set vendor name.

        Args:
            vendor_name(str): Vendor name.
 
        """
        self.vendor_name = vendor_name

    def get_vendor_name(self):
        """Get vendor name.

        Returns:
            str: Vendor name.
 
        """
        return self.vendor_name

    def set_vendor_id(self, vendor_id):
        """Set vendor id.

        Args:
            vendor_id(str): Vendor id.

        """
        self.vendor_id = vendor_id
     
    def get_vendor_id(self):
        """Get vendor id.

        Returns:
            str: Vendor id.

        """
        return self.vendor_id

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
  
    def set_bill_id(self, bill_id):
        """Set bill id.

        Args:
            bill_id(str): Bill id.

        """
        self.bill_id = bill_id

    def get_bill_id(self):
        """Get bill id.

        Returns:
            str: Bill id.

        """
        return bill_id
  
    def set_bill_payment_id(self, bill_payment_id):
        """Set bill payment id.

        Args:
            bill_payment_id(str): Bill payment id.

        """
        self.bill_payment_id = bill_payment_id

    def get_bill_payment_id(self):
        """Get bill payment id.

        Returns:
            str: Bill payment id.

        """
        return self.bill_payment_id
  
    def set_payment_mode(self, payment_mode):
        """Set payment id.

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
            reerence_number(str): Refference number.

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

    def set_paid_through_account_id(self, paid_through_account_id):
        """Set paid through account id.

        Args:
            paid_through_account_id(str): Paid through account id.

        """
        self.paid_through_account_id = paid_through_account_id
 
    def get_paid_through_account_id(self):
        """Get paid through account id.

        Returns:
            str: Paid through account id.

        """
        return self.paid_through_account_id

    def set_paid_through_account_name(self, paid_through_account_name):
        """Set paid through account name.

        Args:
            paid_through_account_name(str): Paid through account name.

        """
        self.paid_through_account_name = paid_through_account_name

    def get_paid_through_account_name(self, paid_through_acount_name):
        """Get paid through account name.

        Returns:
            str: Paid through account name.

        """
        return self.paid_through_account_name

    def set_is_single_bill_payment(self, is_single_bill_payment):
        """Set whether it is single payment bill.

        Args:
            is_single_bill_payment(bool): True if it is single bill payment.

        """
        self.is_single_bill_payment = is_single_bill_payment

    def get_is_single_bill_payment(self):
        """Get whether it is single payment bill.

        Returns:
            bool: True if it is single bill payment.

        """
        return self.is_single_bill_payment



