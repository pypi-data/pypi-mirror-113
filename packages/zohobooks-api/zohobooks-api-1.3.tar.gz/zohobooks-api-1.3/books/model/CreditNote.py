#$Id$

from books.model.Address import Address

class CreditNote:
    """This class creates object for credit notes."""
    def __init__(self):
        """This class is used to create object for credit notes."""
        self.creditnote_id = ''
        self.creditnote_number = ''
        self.date = ''
        self.status = ''
        self.reference_number = ''
        self.customer_id = ''
        self.customer_name = ''
        self.contact_persons = []
        self.currency_id = ''
        self.currency_code = ''
        self.exchange_rate = 0.0
        self.price_precision = 0
        self.template_id = ''
        self.template_name = ''
        self.is_emailed = True
        self.line_items = []
        self.sub_total = 0.0
        self.total = 0.0
        self.total_credits_used = 0.0
        self.total_refunded_amount = 0.0
        self.balance = 0.0
        self.taxes = []
        self.notes = ''
        self.terms = ''
        self.billing_address = Address()
        self.shipping_address = Address()
        self.created_time = ''
        self.last_modified_time = ''
        self.refund_mode = ''
        self.amount = ''
        self.from_account_id = ''
        self.description = ''
  
    def set_creditnote_id(self, creditnote_id):
        """Set creditnote id.
         
        Args:
            creditnote_id(str): Credit note id.

        """
        self.creditnote_id = creditnote_id

    def get_creditnote_id(self):
        """Get creditnote id.

        Returns:
            str: Creditnote id.

        """
        return self.creditnote_id

    def set_creditnote_number(self, creditnote_number):
        """Set creditnote number.

        Args:
            creditnote_number(str):Creditnote number.

        """
        self.creditnote_number = creditnote_number

    def get_creditnote_number(self):
        """Get creditnote number.
      
        Returns:
            str: Creditnote number.
      
        """
        return self.creditnote_number

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
 
    def set_customer_id(self, customer_id):
        """Set customer id.

        Args:
            customer_id(str): Customerid.

        """
        self.customer_id = customer_id

    def get_customer_id(self):
        """Get customer id.

        Returns:
            str: Customer id.

        """
        return self.customer_id
  
    def set_customer_name(self, customer_name):
        """Set customer name.

        Args:
            customer_name(str): Customer name.

        """
        self.customer_name = customer_name
 
    def get_customer_name(self):
        """Get customer name.

        Returns:
            str: Customer name.

        """
        return self.customer_name

    def set_contact_persons(self, contact_person):
        """Set contact person.

        Args:
            contact_person(list): Contact person.

        """
        self.contact_persons.extend(contact_person)

    def get_contact_persons(self):
        """Get contact persons.

        Returns:
            list of instance: List of contact person object.

        """
        return self.contact_persons
  
    def set_currency_id(self, currency_id):
        """Set currency id.

        Args:
            currency_id(str): Currency id.

        """
        self.currency_id = currency_id

    def get_currency_id(self):
        """Get currency id.

        Returns:
            str: Currency id.
 
        """
        return self.currency_id

    def set_currency_code(self, currency_code):
        """Set currency code.

        Args:
            currency_code(str): Currency code.

        """
        self.currency_code = currency_code

    def get_currency_code(self):
        """Get currenccy code.

        Returns:
            str: Currecny code.

        """
        return self.currency_code

    def set_exchange_rate(self, exchange_rate):
        """Set exchange rate.

        Args:
            exchange_rate(float): Exchange ratte.

        """
        self.exchange_rate = exchange_rate

    def get_exchange_rate(self):
        """Get exchange rate.

        Returns:
            float: Exchange rate.

        """
        return self.exchange_rate

    def set_price_precision(self, price_precision):
        """Set price precision.

        Args:
            price_precision(float): Price precision.

        """
        self.price_precision = price_precision

    def get_price_precision(self):
        """Get price precision.

        Returns:
            float: Price precision.

        """
        return self.price_precision

    def set_template_id(self, template_id):
        """Set template id.

        Args:
            template_id(str): Template id.

        """
        self.template_id = template_id

    def get_template_id(self):
        """Get template id.

        Returns:
            str: Template id.

        """
        return self.template_id
 
    def set_template_name(self, template_name):
        """Set template name.

        Args:
            template_name(str): Template name.

        """
        self.template_name = template_name
 
    def get_template_name(self):
        """Get template name.

        Returns:
            str: Template name.

        """
        return self.template_name
  
    def set_is_emailed(self, is_emailed):
        """Set whether is emailed or not.

        Args:
            is_emailed(bool): True if emailed else False.

        """
        self.is_emailed = is_emailed

    def get_is_emailed(self):
        """Get whether is emailed or not.

        Returns:
            bool: True if emailed else False.

        """
        return self.is_emailed
  
    def set_line_items(self, line_items):
        """Set line items.

        Args:
            line_items(instance): Line items object.

        """
        self.line_items.append(line_items)

    def get_line_items(self):
        """Get line items.

        Returns:
            list of instance: List of lineitems object.

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

    def set_total_credits_used(self, total_credits_used):
        """Set total credits used.
 
        Args:
            total_credits_used(float): Total credits used.

        """
        self.total_credits_used = total_credits_used

    def get_total_credits_used(self):
        """Get total credits used.

        Returns:
            float: Total credits used.
 
        """
        return self.total_credits_used

    def set_total_refunded_amount(self, total_refunded_amount):
        """Set total refunded amount.
 
        Args:
            total_refunded_amount(float): Total refunded amount.

        """
        self.total_refunded_amount = total_refunded_amount

    def get_total_refunded_amount(self):
        """Get total refunded amount.

        Returns:
            float: Total refunded amount.

        """
        return self.total_refunded_amount

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

    def set_taxes(self, taxes):
        """Set taxes.

        Args:
            taxes(list of instance): List of tax object.

        """
        self.taxes.extend(taxes)

    def get_taxes(self):
        """Get taxes.
   
        Returns:
            list: List of objects.

        """
        return self.taxes

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

    def set_shipping_address(self, address):
        """Set shipping address.

        Arg:
           address(instance): Address object.

        """
        self.shipping_address = address

    def get_shipping_address(self):
        """Get shipping address.

        Returns:
            instance: Address object.

        """
        return self.shipping_address
 
    def set_billing_address(self, address):
        """Set billing address.
 
        Args:
            address: Address object.

        """
        self.billing_address = address

    def get_billing_address(self):
        """Get billing address.

        Returns:
            instance: Address object.

        """
        return self.billing_address

    def set_created_time(self, created_time):
        """Set created time.

        Args:
            created_time(str): Created time.

        """
        self.created_time = created_time

    def get_created_time(self):
        """Get created time.

        Returns:
            str: Created ime.

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
            str: Last modifiedd time.
      
        """
        return self.last_modified_time

    def set_refund_mode(self, refund_mode):
        """Set refund mode.
 
        Args:
            refund_mode(str): Refund mode.

        """
        self.refund_mode = refund_mode

    def get_refund_mode(self):
        """Get refund mode.

        Returns:
            str: Refund mode.

        """
        return self.refund_mode

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

    def set_from_account_id(self, from_account_id):
        """Set from account id.

        Args:
            from_account_id(str): From account id.

        """ 
        self.from_account_id = from_account_id

    def get_from_account_id(self):
        """Get from account id.

        Returns:
            str: From account id.

        """
        return self.from_account_id

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

    def to_json(self):
        """This method is used to convert credit notes object to json object.

        Returns:
            dict: Dictionary containing json object for credit notes.

        """
        data = {}
        if self.customer_id != '':
            data['customer_id'] = self.customer_id
        if self.contact_persons:
            data['contact_persons'] = self.contact_persons
        if self.reference_number != '':
            data['reference_number'] = self.reference_number
        if self.template_id != '':
            data['template_id'] = self.template_id
        if self.date != '':
            data['date'] = self.date
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
        if self.creditnote_number != '':
            data['creditnote_number'] = self.creditnote_number
        return data
