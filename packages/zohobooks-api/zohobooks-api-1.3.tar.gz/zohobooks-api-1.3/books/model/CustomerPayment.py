#$Id$

class CustomerPayment:
    """This class is used to create object for customer payments."""
    def __init__(self):
        """Initialize parameters for customer payments."""
        self.customer_id = ''
        self.invoices = []
        self.payment_mode = ''
        self.description = ''
        self.date = ''
        self.reference_number = ''
        self.exchange_rate = 0.0
        self.amount = 0.0
        self.bank_charges = 0.0
        self.tax_account_id = ''
        self.account_id = ''
        self.payment_id = ''
        self.invoice_id = ''
        self.payment_number = ''
        self.invoice_numbers = ''
        self.bcy_amount = 0
        self.unused_amount = 0
        self.bcy_unused_amount = 0
        self.account_name = ''
        self.customer_name = ''
        self.created_time = ''
        self.last_modified_time = ''
        self.tax_account_name = ''
        self.tax_amount_withheld = 0.0
        self.amount_applied = 0.0
   
    def set_customer_id(self, customer_id):
        """Set customer id.
   
        Args:
            customer_id(str): Customer id.

        """
        self.customer_id = customer_id

    def get_customer_id(self):
        """Get customer id.

        Returns:
            str: Customer id.

        """
        return self.customer_id
  
    def set_invoices(self, invoice):
        """Set invoices.

        Args:
            invoice(list) : List of invoice object.

        """
        self.invoices.extend(invoice)
 
    def get_invoices(self):
        """Get invoices.

        Returns:
            list: List of invoices.

        """ 
        return self.invoices

    def set_payment_mode(self, payment_mode):
        """Set mode of payment for the payment received.

        Args:
            payment_mode(str): Mode of payment.

        """
        self.payment_mode = payment_mode

    def get_payment_mode(self):
        """Get mode of payment of the payment received.

        Returns:
            str: Mode of payment.

        """
        return self.payment_mode

    def set_description(self, description):
        """Set description for the customer payment.
 
        Args:
            description(str): Description for the customer payment.

        """
        self.description = description

    def get_description(self):
        """Get description of the customer payment.

        Returns:
            str: Description of the customer payment.
  
        """
        return self.description
   
    def set_date(self, date):
        """Set date at which the payment is made.

        Args:
            date(str): Date at which payment is made.

        """
        self.date = date
 
    def get_date(self):
        """Get date at which payment is made.

        Returns:
            str: Date at which payment is made.

        """
        return self.date

    def set_reference_number(self, reference_number): 
        """Set reference number for the customer payment.

        Args:
            reference_number(str): Reference number for the customer payment.

        """
        self.reference_number = reference_number

    def get_reference_number(self):
        """Get reference number of the customer payment.

        Returns:
            str: Reference number of the customer payment.

        """
        return self.reference_number
   
    def set_exchange_rate(self,  exchange_rate):
        """Set exchange rate for the currency.

        Args: 
            exchange_rate(float): Exchange rate for thee currency.
 
        """
        self.exchange_rate = exchange_rate

    def get_exchange_rate(self):
        """Get exchange rate of the currency.

        Returns:
            float: Exchange rate of the currency.

        """
        return self.exchange_rate

    def set_amount(self, amount):
        """Set payment amount made by the customer.

        Args: 
            amount(float): Payment amount made by the customer.

        """
        self.amount = amount

    def get_amount(self):
        """Get payment amount made by the customer.

        Returns:
            float: Payment amount made by the customer.

        """
        return self.amount
  
    def set_bank_charges(self, bank_charges):
        """Set bank charges incurred.

        Args:
            bank_charges(float): Bank charges incurred.

        """
        self.bank_charges = bank_charges

    def get_bank_charges(self):
        """Get bank charges incurred.

        Returns:
            float: Bank charges incurred.
      
        """
        return self.bank_charges

    def set_tax_account_id(self, tax_account_id):
        """Set id for the tax account incase of withholding tax.

        Args: 
            tax_account_id(str): Id for the tax account.

        """
        self.tax_account_id = tax_account_id

    def get_tax_account_id(self):
        """Get id of the tax account.

        Returns:
            str: Id of the tax account.

        """
        return self.tax_account_id
  
    def set_account_id(self, account_id):
        """Set ID for the cash/ bank account to which the
               payment has to be deposited.

        Args:
            account_id(str): Id for the cash or bank account.

        """
        self.account_id = account_id

    def get_account_id(self):
        """Get ID of the cash/ bank account to which the 
               payment has to be deposited.

        Returns:
            str: Id of the cash or bank account.

        """
        return self.account_id
 
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
  
    def set_invoice_numbers(self, invoice_numbers):
        """Set invoice numbers.

        Args:
            invoice_numbers(str): invoice_numbers

        """
        self.invoice_numbers = invoice_numbers

    def get_invoice_numbers(self):
        """Get invoice numbers.
       
        Returns: 
            str: Invoice numbers

        """
        return self.invoice_numbers
 
    def set_bcy_amount(self, bcy_amount):
        """Set bcy amount.

        Args:
            bcy_amount(int): bcy amount.

        """
        self.bcy_amount = bcy_amount

    def get_bcy_amount(self):
        """Get bcy amount.

        Returns:
            int: bcy amount.

        """
        return self.bcy_amount
   
    def set_unused_amount(self, unused_amount):
        """Set unused amount.

        Args:
            unused_amount(int): Unused amount.

        """
        self.unused_amount = unused_amount
 
    def get_unused_amount(self):
        """Get unused amount.

        Returns:
            int: Unused amount.

        """
        return self.unused_amount
  
    def set_bcy_unused_amount(self, bcy_unused_amount):
        """Set bcy unused amount.
 
        Args:
            bcy_unused_amount(int): bcy unused amount.

        """
        self.bcy_unused_amount = bcy_unused_amount

    def get_bcy_unused_amount(self):
        """Get bcy unused amount.

        Returns:
            int: bcy unused amount.

        """
        return self.bcy_unused_amount
  
    def set_account_name(self, account_name):
        """Set account name.

        Args:
            account_name(str): Account name.

        """
        self.account_name = account_name

    def get_account_name(self):
        """Get account name.

        Returns:
            str: Account name.

        """
        return self.account_name

    def set_customer_name(self, customer_name):
        """Set customer name.

        customer_name(str): Customer name.

        """
        self.customer_name = customer_name
 
    def get_customer_name(self):
        """Get customer name.

        Returns:
            str: Customer name.

        """
        return self.customer_name

    def set_created_time(self, created_time):
        """Set created time.

        Args:
            created_time(str): Created time.

        """
        self.created_time = created_time
    def get_created_time(self):
        """Get created time.
       
        Returns:
            str: Created time.
        """
        return self.created_time
  
    def set_last_modified_time(self, last_modified_time):
        """Set last modified time.

        Args:
            last_modified_time(str): Last modified time.

        """
        self.last_modified_time = last_modified_time

    def get_last_modified_time(self):
        """Get last modified time.

        Returns:
            str: Last modified time.

        """
        return self.last_modified_time

    def set_tax_account_name(self, tax_account_name):
        """Set tax account name.

        Args:
            tax_account_name(str): Tax Account name.
 
        """
        self.tax_account_name = tax_account_name

    def get_tax_account_name(self):
        """Get tax account name.

        Returns:
            str: Tax account name.
 
        """
        return self.tax_account_name

    def set_tax_amount_withheld(self, tax_amount_withheld):
        """Set amount withheld for tax.

        Args:
            tax_amount_withheld(float): Amount withheld for tax.

        """
        self.tax_amount_withheld = tax_amount_withheld

    def get_tax_amount_withheld(self):
        """Get amount withheld for tax.

        Returns:
            float: Amount withheld for tax.

        """
        return self.tax_amount_withheld

    def to_json(self):
        """This method is used to convert customer payment object to json object.

        Returns:
            dict: Dictionary containing json object for customer payments.

        """
        data = {}
        if self.customer_id != '':
            data['customer_id'] = self.customer_id
        if self.invoices:
            data['invoices'] = []
            for value in self.invoices:
                invoice = value.to_json()
                data['invoices'].append(invoice)
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
        if self.bank_charges > 0:
            data['bank_charges'] = self.bank_charges 
        if self.tax_account_id != '':
            data['tax_account_id'] = self.tax_account_id
        if self.account_id != '':
            data['account_id'] = self.account_id
        if self.invoice_id != '':
            data['invoice_id'] = self.invoice_id
        if self.amount_applied > 0:
            data['amount_applied'] = self.amount_applied
        if self.payment_number != '':
            data['payment_number'] = self.payment_number

        return data
