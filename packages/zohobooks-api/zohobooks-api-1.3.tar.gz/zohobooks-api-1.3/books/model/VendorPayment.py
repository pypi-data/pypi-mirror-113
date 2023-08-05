#$Id$

class VendorPayment:
    """This class is used to create object for Vendor payments."""
    def __init__(self):
        """Initialize parameters for Vendor payments."""
        self.payment_id = ''
        self.vendor_id = ''
        self.vendor_name = ''
        self.payment_mode = ''
        self.description = ''
        self.date = ''
        self.reference_number = ''
        self.exchange_rate = 0.0
        self.amount = 0.0
        self.currency_symbol = ''
        self.paid_through_account_id = ''
        self.paid_through_account_name = ''
        self.bills = []
        self.balance = 0.0
  
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

    def set_currency_symbol(self, currency_symbol):
        """Set currency symbol.

        Args:
            currency_symbol(str): Currency symbol.

        """
        self.currency_symbol = currency_symbol

    def get_currency_symbol(self):
        """Get currency symbol.

        Returns:
            str: Currency symbol.

        """
        return self.currency_symbol

    def set_paid_through_account_id(self, paid_through_account_id):
        """Set paid through account id.

        Args:
            paid_through_account_id(str): Paid through account id.

        """
        self.paid_through_account_id = paid_through_account_id

    def get_paid_through_account_id(self):
        """Get paid through account id.

        Returns:
            str: Paid through acount id.

        """
        return self.paid_through_account_id
  
    def set_paid_through_account_name(self, paid_through_account_name):
        """Set paid through account name.

        Args:
            paid_through_account_name(str): Paid through account name.

        """
        self.paid_through_account_name = paid_through_account_name

    def get_paid_through_account_name(self):
        """Get paid through account name.
 
        Returns:
            str: Paid through account name.

        """
        return self.paid_through_account_name
  
    def set_bills(self, bill): 
        """Set bills.

        Args:
            bills(instance): Bills object.

        """
        self.bills.append(bill)

    def get_bills(self):
        """Get bills.

        Returns:
            list of instance: List of bills object.

        """
        return self.bills
    
    def set_balance(self, balance):
        """Set balance.

        Args: 
            balance(float): Balance.

        """
        self.balance = balance

    def get_balance(self):
        """Get balance.

        Returns:
            float: Balance.

        """
        return self.balance

    def to_json(self):
        """This method is used to convert vendor payments object to json object.

        Returns:
            dict: Dictionary containing json object for vendor payments.

        """ 
        data = {}
        if self.vendor_id != '':
            data['vendor_id'] = self.vendor_id
        if self.bills:
            data['bills'] = []
            for value in self.bills:
                bill = value.to_json()
                data['bills'].append(bill)
        if self.payment_mode != '':
            data['payment_mode'] = self.payment_mode
        if self.description != '': 
            data['description'] = self.description
        if self.date != '':
            data['date'] = self.date
        if self.reference_number != '':
            data['reference_number'] = self.reference_number
        if self.exchange_rate > 0:
            data['exchange_rate'] = self.exchange_rate
        if self.amount > 0:
            data['amount'] = self.amount
        if self.paid_through_account_id != '':
           data['paid_through_account_id'] = self.paid_through_account_id
        return data


