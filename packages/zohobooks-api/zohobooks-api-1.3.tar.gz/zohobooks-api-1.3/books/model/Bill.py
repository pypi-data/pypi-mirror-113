#$Id$

from books.model.Address import Address

class Bill:
    """This class is used to create an object for Bills."""
    def __init__(self):
        """Initialize the parameters for bills object."""
        self.bill_id = ''
        self.bill_payment_id = ''
        self.vendor_id = ''
        self.vendor_name = ''
        self.unused_credits_payable_amount = 0.0
        self.status = ''
        self.bill_number = ''
        self.date = ''
        self.due_date = ''
        self.due_days = ''
        self.reference_number = ''
        self.due_by_days = 0
        self.due_in_days = ''
        self.currency_id = ''
        self.currency_code = ''
        self.currency_symbol = ''
        self.price_precision = 0
        self.exchange_rate = 0.0
        self.line_items = []
        self.sub_total = 0.0
        self.tax_total = 0.0
        self.total = 0.0
        self.taxes = []
        self.amount_applied = 0.0
        self.payment_made = 0.0
        self.balance = 0.0
        self.billing_address = Address()
        self.payments = []
        self.created_time = ''
        self.last_modified_time = ''
        self.reference_id = ''
        self.attachment_name = ''
        self.account_id = ''
        self.description = ''
        self.rate = 0.0
        self.quantity = 0.0
        self.tax_id = ''
        self.notes = ''
        self.terms = ''
        self.is_inclusive_tax = False
   
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
        return self.bill_id
  
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

    def set_vendor_id(self, vendor_id):
        """Set vendor id.

        Args:
            vendor_id(str): Vendor id.

        """
        self.vendor_id = vendor_id

    def set_is_inclusive_tax(self, is_inclusive_tax):
        """Set vendor id.

        Args:
            is_inclusive_tax(bool): is_inclusive_tax.

        """
        self.is_inclusive_tax = is_inclusive_tax

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

    def set_unused_credits_payable_amount(self, unused_credits_payable_amount):
        """Set unused amount payable amount.

        Args:
            unused_credits_payable_amount(float): Unused amount payable amount.

        """
        self.unused_credits_payable_amount = unused_credits_payable_amount

    def get_unused_payable_amount(self):
        """Get unused amount payable amount.

        Returns:
            float: Unused amount payable amount.
 
        """
        return self.unused_credits_payable_amount
 
    def set_status(self, status):
        """Set status.

        Args: 
            status(str): Status.

        """
        self.status = status

    def get_status(self):
        """Get status.

        Returns:
            str: Status.

        """
        return self.status

    def set_bill_number(self, bill_number):
        """Set bill number.

        Args: 
            bill_number(str): Bill number.

        """
        self.bill_number = bill_number

    def get_bill_number(self):
        """Get bill number.

        Returns:
            str: Bill number.

        """
        return self.bill_number

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

    def set_due_date(self, due_date):
        """Set due date.

        Args: 
            due_date(str): Due date.

        """
        self.due_date = due_date

    def get_due_date(self):
        """Get due date.

        Returns:
            str: Due date.

        """
        return self.due_date
  
    def set_due_by_days(self, due_by_days):
        """Set due by days.
 
        Args:
            due_by_days(int): Due by days.

        """
        self.due_by_days = due_by_days

    def get_due_by_days(self): 
        """Get due by days.

        Returns: 
            int: Due by days.

        """
        return self.due_by_days
  
    def set_due_in_days(self, due_in_days):
        """Set due in days.

        Args:
            due_in_days(str): Due in days.

        """
        self.due_in_days = self.due_in_days

    def get_due_in_days(self): 
        """Get due in days.

        Returns:
            str: Due in days.

        """
        return self.due_in_days
  
    def set_currency_id(self, currency_id):
        """Set currency_id.

        Args:
            currency_id(str): Currency id.

        """
        self.currency_id = currency_id

    def get_currency_id(self):
        """Get currency id.

        Returns:
            str: Currency id.

        """
        return currency_id

    def set_currency_code(self, currency_code):
        """Set currency code.

        Args:
            currency_code(str): Currency code.

        """
        self.currency_code = currency_code

    def get_currency_code(self):
        """Get currency code.

        Returns:
            str: Currency code.

        """
        return self.currency_code

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
  
    def set_price_precision(self, price_precision):
        """Set price precision.

        Args: 
            price_precision(int): Price precision.

        """
        self.price_precision = price_precision

    def get_price_precision(self):
        """Get price precision.

        Returns:
            int: Price precision.

        """
        return self.price_precision
  
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
  
    def set_line_items(self, line_item):
        """Set line items.

        Args:
            line_item(instance): Line item object.
  
        """
        self.line_items.append(line_item)
 
    def get_line_items(self):
        """Get line items.

        Returns:
            list of instance: List of line items object.

        """
        return self.line_items
  
    def set_sub_total(self, sub_total):
        """Set sub total.

        Args:
            sub_total(float): Sub total.

        """
        self.sub_total = sub_total

    def get_sub_total(self):
        """Get sub total.

        Returns:
            float: Sub total.

        """
        return self.sub_total

    def set_tax_total(self, tax_total):
        """Set tax total.

        Args:
            tax_total(float): Tax total.

        """
        self.tax_total = tax_total

    def get_tax_total(self):
        """Get tax total.
 
        Returns:
            tax_total(float): Tax total.

        """
        return self.tax_total
 
    def set_total(self, total):
        """Set total.

        Args:
            total(float): Total.

        """
        self.total = total

    def get_total(self):
        """Get total.

        Returns:
            float: Total.
   
        """
        return self.total
  
    def set_taxes(self, tax):
        """Set taxes.

        Args:
            tax(instance): Tax object.

        """
        self.taxes.append(tax)

    def get_taxes(self):
        """Get taxes.

        Returns:
            list of instance: List of tax object.

        """
        return self.taxes

    def set_payment_made(self, payment_made):
        """Set payment made.

        Args:
            payment_made(float): Payment made.

        """
        self.payment_made = payment_made
 
    def get_payment_made(self):
        """Get payment made.

        Returns:
            float: Payment made.

        """
        return self.payment_made
  
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
  
    def set_billing_address(self, billing_address):
        """Set billling address,

        Args:
            billing_address(instance): Billing address object.

        """
        self.billing_address = billing_address

    def get_billing_address(self): 
        """Get billing address.

        Returns:
            instance: Billing address object.

        """
        return self.billing_address
  
    def set_payments(self, payments):  
        """Set payments.

        Args:
            payments(instance): Payments object.
 
        """
        self.payments.append(payment)

    def get_payments(self): 
        """Get payments.
 
        Returns:
            list of instance: List of payments object.

        """
        return self.payments
   
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
  
    def set_reference_id(self, reference_id):
        """Set reference id.

        Args:
            reference_id(str): Reference id.

        """
        self.reference_id = reference_id
 
    def get_reference_id(self):
        """Get reference id.

        Returns: 
            str: Reference id.

        """
        return self.reference_id

    def set_notes(self, notes):
        """Set notes.

        Args:
            notes(str): Notes.

        """
        self.notes = notes

    def get_notes(self):
        """Get notes.

        Returns:
            str: Notes.

        """
        return self.notes
  
    def set_terms(self, terms):
        """Set terms.

        Args:
            terms(str): Terms.

        """
        self.terms = terms

    def get_terms(self): 
        """Get terms.

        Returns: 
            str: Terms.

        """
        return self.terms
 
    def set_attachment_name(self, attachment_name):
        """Set attachment name.

        Args:
            attachment_name(str): Attachment name.
 
        """
        self.attachment_name = attachment_name
 
    def get_attachment_name(self):
        """Get attachment name.

        Returns:
            str: Attachment name.

        """
        return self.attachment_name
   
    def set_account_id(self, account_id):
        """Set account id.

        Args:
            account_id(str): Account id.

        """
        self.account_id = account_id

    def get_account_id(self):
        """Get account id.
 
        Returns:
            str: Account id.

        """
        return self.account_id  
  
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
  
    def set_rate(self, rate):
        """Set rate.
 
        Args:
            rate(float): Rate.

        """
        self.rate = rate

    def get_rate(self): 
        """Get rate.

        Returns:
            float: Rate.

        """
        return self.rate

    def set_quantity(self, quantity):
        """Set quantity.

        Args:
            quantity(float): Quantity.

        """
        self.quantity = quantity

    def get_quantity(self):
        """Get quantity.

        Returns:
            float: Quantity.

        """   
        return self.quantity
  
    def set_tax_id(self, tax_id):
        """Set tax id.

        Args: 
            tax_id(str): Tax id.

        """
        self.tax_id = tax_id

    def get_tax_id(self):
        """Get tax id.

        Returns:
            str: Tax id.

        """
        return self.tax_id

    def set_due_days(self, due_days):
        """Set due days.

        Args:
            due_days(str): Due days.

        """
        self.due_days = due_days

    def get_due_days(self):
        """Get due days.

        Returns:
            str: Due days.
  
        """
        return self.due_days
    
    def to_json(self):
        """This method is used to convert bill object to json object.

        Returns:
            dict: Dictionary containing json object for Bills.

        """
        data = {}
        if self.bill_id != '': 
            data['bill_id'] = self.bill_id
        if self.amount_applied > 0: 
            data['amount_applied'] = self.amount_applied
        if self.vendor_id != '':
            data['vendor_id'] = self.vendor_id
        if self.is_inclusive_tax:
            data['is_inclusive_tax'] = self.is_inclusive_tax
        if self.bill_number != '':
            data['bill_number'] = self.bill_number
        if self.reference_number != '':
            data['reference_number'] = self.reference_number
        if self.date != '':
            data['date'] = self.date
        if self.due_date != '':
            data['due_date'] = self.due_date
        if self.exchange_rate > 0:
            data['exchange_rate'] = self.exchange_rate
        if self.line_items:
            data['line_items'] = []
            for value in self.line_items:
                line_item = value.to_json()
                data['line_items'].append(line_item)
        if self.notes != '':
            data['notes'] = self.notes
        if self.terms != '': 
            data['terms'] = self.terms
        return data
 




  


