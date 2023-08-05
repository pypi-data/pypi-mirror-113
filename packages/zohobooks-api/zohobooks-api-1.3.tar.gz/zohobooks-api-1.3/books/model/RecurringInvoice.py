#$Id$

from books.model.Address import Address

class RecurringInvoice:
    """This class is used to creat object for Recurring invoice."""
    def __init__(self):
        """Initialize parameters for Recurring invoice object."""
        self.recurrence_name = ''
        self.customer_id = ''
        self.contact_persons = []
        self.template_id = ''
        self.start_date = ''
        self.end_date = ''
        self.recurrence_frequency = ''
        self.repeat_every = 0
        self.payment_terms = 0
        self.payment_terms_label = ''
        self.exchange_rate = 0.0
        self.payment_options = {
            'payment_gateways': []
            }
        self.discount = ''
        self.is_discount_before_tax = ''
        self.discount_type = ''
        self.line_items = []
        self.salesperson_name = ''
        self.shipping_charge = 0.0
        self.adjustment = 0.0
        self.adjustment_description = ''
        self.notes = ''
        self.terms = ''
        self.recurring_invoice_id = ''
        self.status = ''
        self.total = 0.0
        self.customer_name = ''
        self.last_sent_date = ''
        self.next_invoice_date = ''
        self.created_time = ''
        self.last_modified_time = ''
        self.currency_id = ''
        self.price_precision = 0
        self.currency_code = ''
        self.currency_symbol = ''
        self.late_fee = {}
        self.sub_total = 0.0
        self.tax_total = 0.0
        self.allow_partial_payments = None
        self.taxes = []
        self.billing_address = Address()
        self.shipping_address = Address()
        self.template_name = ''
        self.salesperson_id = ''
        self.custom_fields = []

    def set_custom_fields(self, custom_fields):
        """Set custom fields.

        Args:
            custom_fields(list): List of custom fields.

        """
        self.custom_fields.extend(custom_fields)

    def get_custom_fields(self):
        """Get custom fields.

        Returns:
            list: List of custom fields.

        """
        return self.custom_fields

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
    
    def set_recurrence_name(self, recurrence_name):
        """Set name of the recurring invoice.

        Args:
            recurrence_name(str): Name of the recurring invoice.

        """
        self.recurrence_name = recurrence_name

    def get_recurrence_name(self):
        """Get name of the recurring invoice.

        Returns:
            str: Name of the recurring invoice..

        """
        return self.recurrence_name
  
    def set_customer_id(self, customer_id):
        """Set ID for the customer for which recurring invoice has been 
            created.

        Args: 
            customer_id(str): Customer id for which recurring invoice has been 
                created.

        """
        self.customer_id = customer_id

    def get_customer_id(self):
        """Get ID for the customer for which recurring invoice has been 
            created.

        Returns:
            str: Customer id for which recurring invoice has been created.

        """
        return self.customer_id
   
    def set_contact_persons(self, contact_persons):
        """Set Contact persons associated with the recurring invoice.

        Args:
            contact_persons(list): List of contact persons id.

        """ 
        self.contact_persons.extend(contact_persons)

    def get_contact_persons(self):
        """Get contact persons associated with the recurring invoice.

        Returns:
            list: List of contact persons id.

        """
        return self.contact_persons

    def set_template_id(self, template_id):
        """Set ID of the pdf template associated with the recurring profile.

        Args:
            template_id(str): Template id.

        """
        self.template_id = template_id

    def get_template_id(self):
        """Get ID of the pdf template associated with the recurring profile.

        Returns:
            str: Template id.
 
        """
        return self.template_id
  
    def set_start_date(self, start_date):
        """Set start date for the recurring invoice.

        Args:
            start_date(str): Starting date of the recurring invoice.

        """
        self.start_date = start_date

    def get_start_date(self):
        """Get start date of the recurring invoice.

        Returns:
            str: Starting date of the recurring invoice.

        """
        return self.start_date

    def set_end_date(self, end_date):
        """Set the date at which the recurring invoice has to be expires.

        Args:
            end_date(str): Date on which recurring invoice expires.

        """
        self.end_date = end_date

    def get_end_date(self):
        """Get the date at which the recurring invoice has to be expires.

        Returns:
            str: Date on which recurring invoice expires.

        """
        return self.end_date
   
    def set_recurrence_frequency(self, recurrence_frequency):
        """Set the frequency for the recurring invoice.

        Args:
            recurrence_frequency(str): Frequency for the recurring invoice. 
                Allowed values re days, weeks, months and years.

        """
        self.recurrence_frequency = recurrence_frequency

    def get_recurrence_frequency(self):
        """Get the frequency of the recurring invoice.

        Returns:
            str: Frequency of the recurring invoice.

        """
        return self.recurrence_frequency
  
    def set_repeat_every(self, repeat_every):
        """Set frequency to repeat.

        Args:
            repeat_every(int): Frequency to repeat.

        """
        self.repeat_every = repeat_every

    def get_repeat_every(self):
        """Get frequency to repeat.

        Returns:
            int: Frequency to repeat.

        """
        return self.repeat_every
  
    def set_payment_terms(self, payment_terms):
        """Set payment terms in days. Invoice due date will be calculated 
            based on this.

        Args:
            payment_terms(int): Payment terms in days.Example 15, 30, 60.

        """
        self.payment_terms = payment_terms

    def get_payment_terms(self):
        """Get payment terms.
 
        Returns:
            int: Payment terms in days.

        """
        return self.payment_terms
   
    def set_payment_terms_label(self, payment_terms_label):
        """Set payment terms label.

        Args:
            payment_terms_label(str): Payment terms label. Default value for 15 
                days is "Net 15".
 
        """
        self.payment_terms_label = payment_terms_label

    def get_payment_terms_label(self):
        """Get payment terms label.
        
        Returns:
            str: Payment terms label.
        
        """
        return self.payment_terms_label
  
    def set_exchange_rate(self, exchange_rate):
        """Set exchange rate for the currency.

        Args:
            exchange_rate(float): Exchange rate for currency.

        """
        self.exchange_rate = exchange_rate

    def get_exchange_rate(self):
        """Get exchange rate of the currency.

        Returns:
            float: Exchange rate of the currency.
  
        """
        return self.exchange_rate

    def set_payment_options(self, payment_gateways):
        """Set payment options associated with the recurring invoice, online 
            payment gateways.
         
        Args: 
            payment_gateways(instance): Online payment gateway through which 
                payment can be made.
        
        """ 
        self.payment_options['payment_gateways'].append(payment_gateways)
 
    def get_payment_options(self):
        """Get payment options associated with the recurring invoice, online 
            payment gateways.
   
        Returns:
            dict: Payment options details.

        """   
        return self.payment_options

    def set_discount(self, discount):
        """Set discount applied to the invoice.

        Args:
            discount(str): Discount applied to the invoice. It can be either 
                in % or in amount.

        """
        self.discount = discount

    def get_discount(self):
        """Get discount applied to the invoice.

        Returns:
            str: Discount applied to the invoice.

        """
        return self.discount
   
    def set_is_discount_before_tax(self, is_discount_before_tax):
        """Set whether to discount before tax.

        Args:
            is_discount_before_tax(bool): True to discount befroe tax else 
                False.

        """
        self.is_discount_before_tax = is_discount_before_tax

    def get_is_discount_before_tax(self):
        """Get whether to discount before tax.

        Returns:
            bool: True to discount before tax else False.

        """
        return self.is_discount_before_tax

    def set_discount_type(self, discount_type):
        """Set how the discount is specified.

        Args:
            discount_type(str): Discount type. Allowed values are entity_level 
                and item_level.

        """
        self.discount_type = discount_type

    def get_discount_type(self):
        """Get discount type.

        Returns:
            str: Discount type.

        """
        return self.discount_type
 
    def set_line_items(self, line_item):
        """Set line items for an invoice.

        Args:
            line_items(instance): Line items object.

        """
        self.line_items.append(line_item)

    def get_line_items(self):
        """Get line items of an invoice.

        Returns:
            list: List of line items instance.

        """
        return self.line_items

    def set_salesperson_name(self, salesperson_name):
        """Set name of the salesperson.

        Args: 
            salesperson_name(str): Salesperson name.

        """
        self.salesperson_name = salesperson_name

    def get_salesperson_name(self):
        """Get salesperson name.

        Returns:
            str: Salesperson name.

        """
        return self.salesperson_name
 
    def set_shipping_charge(self, shipping_charge):
        """Set shipping charges applied to the invoice.

        Args: 
            shipping_charge(float): Shipping charges applied to the invoice.

        """
        self.shipping_charge = shipping_charge

    def get_shipping_charge(self):
        """Get shipping charges applied to invoice.

        Returns:
            float: Shipping charges applied to the invoice.

        """
        return self.shipping_charge
  
    def set_adjustment(self, adjustment):
        """Set adjustments made to the invoice.
 
        Args:
            adjustment(float): Adjustments made to the invoice.

        """
        self.adjustment = adjustment

    def get_adjustment(self):
        """Get adjustments made to the invoice.

        Returns:
            float: Adjustments made to the invoice.

        """
        return self.adjustment
 
    def set_adjustment_description(self, adjustment_description):
        """Set the adjustment description.

        Args:
            adjustment_description(str): Adjustment description.

        """
        self.adjustment_description = adjustment_description

    def get_adjustment_description(self):
        """Get adjustment description.

        Returns:
            str: Adjustment description.

        """
        return self.adjustment_description

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

    def set_recurring_invoice_id(self, recurring_invoice_id):
        """Set recurring invoice id.

        Args:
            recurring_invoice_id(str): Recurring invoice id.

        """
        self.recurring_invoice_id = recurring_invoice_id
 
    def get_recurring_invoice_id(self):
        """Get recurring invoice id.
 
        Returns: 
            str: Recurring invoice id.

        """
        return self.recurring_invoice_id

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

    def set_last_sent_date(self, last_sent_date):
        """Set last sent date.

        Args:
            last_sent_date(str): Last sent date.

        """
        self.last_sent_date = last_sent_date

    def get_last_sent_date(self):
        """Get last sent date.

        Returns:
            str: Last sent date.

        """
        return self.last_sent_date

    def set_next_invoice_date(self, next_invoice_date):
        """Set next invoice date.

        Args: 
            next_invoice_date(str): Next invoice date.

        """
        self.next_invoice_date = next_invoice_date
 
    def get_next_invoice_date(self):
        """Get next invoice date.

        Returns:
            str: Next invoice date.

        """
        return self.next_invoice_date
   
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
  
    def set_currency_code(self, currency_code):
        """Set currency code.

        Args: 
            currency_code(str):  Currency code.

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

    def set_late_fee(self, late_fee):
        """Set late fee.

        Args:
            late_fee(dict): Late fee.

        """
        self.late_fee = late_fee

    def get_late_fee(self):
        """Get late fee.
       
        Returns:
            dict: LAte fee.
        
        """
        return self.late_fee

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
            float: Tax total.

        """
        return self.tax_total
    
    def set_allow_partial_payments(self, allow_partial_payments):
        """Set whether to allow partial payments or not.

        Args:
            allow_partial_payments(bool): True to allow partial payments.

        """
        self.allow_partial_payments = allow_partial_payments

    def get_allow_partial_payments(self):
        """Get whether partial payments are allowed or not.

        Returns:
            str: True if partial payments are allowed else False.

        """ 
        return self.allow_partial_payments
   
    def set_taxes(self, taxes): 
        """Set taxes.

        Args:
            taxes(instance): Tax object.

        """
        self.taxes.append(taxes)

    def get_taxes(self):
        """Get taxes.

        Returns:
            list: List of taxes object.

        """
        return self.taxes

    def set_billing_address(self, address):
        """Set billing address.

        Args:
            address(instance): Address object.

        """
        self.billing_address = (address)
 
    def get_billing_address(self):
        """Get billing address.

        Returns: 
            instance: Billing address object.

        """
        return self.billing_address

    def set_shipping_address(self, address):
        """Set shipping address.
  
        Args:
            address(instance): Shipping address.

        """
        self.shipping_address = address

    def get_shipping_address(slef):
        """Get shipping address.

        Returns:
            instance: Shipping address object.

        """
        return self.shipping_address
   
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


    def set_salesperson_id(self, salesperson_id):
        """Set salesperson id.
  
        Args: 
            salesperson_id(str): Salesperson id.

        """
        self.salesperson_id = salesperson_id

    def get_salesperson_id(self):
        """Get salesperson id.

        Returns:
            str: Salesperson id.

        """
        return self.salesperson_id

    def to_json(self):
        """This method is used to convert recurring invoice object to json object.

        Returns:
            dict: Dictionary containing json object for recurring invoice.

        """
        data = {}
        if self.recurrence_name != '':
            data['recurrence_name'] = self.recurrence_name
        if self.customer_id != '':
            data['customer_id'] = self.customer_id
        if self.contact_persons:
            data['contact_persons'] = self.contact_persons
        if self.template_id != '':
            data['template_id'] = self.template_id
        if self.start_date != '':
            data['start_date'] = self.start_date
        if self.end_date != '':
            data['end_date'] = self.end_date
        if self.recurrence_frequency != '':
            data['recurrence_frequency'] = self.recurrence_frequency
        if self.repeat_every != '':
            data['repeat_every'] = self.repeat_every
        if self.payment_terms != '':
            data['payment_terms'] = self.payment_terms
        if self.payment_terms_label != '':
            data['payment_terms_label'] = self.payment_terms_label
        if self.exchange_rate > 0:
            data['exchange_rate'] = self.exchange_rate
        if self.payment_options['payment_gateways']:
            data['payment_options'] = {
                'payment_gateways': []
                }
            for value in self.payment_options['payment_gateways']:
                data['payment_options']['payment_gateways'].append(\
                                        value.to_json())
        if self.discount > 0:
            data['discount'] = self.discount
        if self.is_discount_before_tax is not None:
            data['is_discount_before_tax'] = self.is_discount_before_tax
        if self.discount_type != '':
            data['discount_type'] = self.discount_type
        if self.line_items:
            data['line_items'] = []
            for value in self.line_items:
                line_item = value.to_json()
                data['line_items'].append(line_item)
        if self.notes != '':
            data['notes'] = self.notes
        if self.terms != '':
            data['terms'] = self.terms
        if self.salesperson_name != '':
            data['salesperson_name'] = self.salesperson_name
        if self.shipping_charge > 0:
            data['shipping_charge'] = self.shipping_charge
        if self.adjustment != '':
            data['adjustment'] = self.adjustment
        if self.adjustment_description != '':
            data['adjustment_description'] = self.adjustment_description
        return data
