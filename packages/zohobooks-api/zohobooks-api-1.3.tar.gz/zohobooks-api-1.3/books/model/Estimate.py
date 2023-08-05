#$Id$

from books.model.Address import Address

class Estimate:
    """This class is used to create object for estimates."""
    def __init__(self):
        """Initialize parameters for Estimates object."""
        self.estimate_id = ''
        self.estimate_number = ''
        self.date = ''
        self.reference_number = ''
        self.status = ''
        self.customer_id = ''
        self.customer_name = ''
        self.contact_persons = []
        self.currency_id = ''
        self.currency_code = ''
        self.exchange_rate = 0.00
        self.expiry_date = ''
        self.discount = 0.00
        self.is_discount_before_tax = None
        self.discount_type = ''
        self.line_items = []
        self.shipping_charge = 0.00
        self.adjustment = 0.00
        self.adjustment_description = ''
        self.sub_total = 0.0
        self.total = 0.0
        self.tax_total = 0.0
        self.price_precision = 0
        self.taxes = []
        self.billing_address = Address()
        self.shipping_address = Address()
        self.notes = ''
        self.terms = ''
        self.custom_fields = []
        self.template_id = ''
        self.template_name = ''
        self.created_time = ''
        self.last_modified_time = ''
        self.salesperson_id = ''
        self.salesperson_name = ''
        self.accepted_date = ''
        self.declined_date = ''
      
    def set_estimate_id(self, estimate_id):
        """Set estimate id.

        Args:
            estimate_id(str): Estimate id.
 
        """
        self.estimate_id = estimate_id

    def get_estimate_id(self):
        """Get estimate id.

        Returns:
            str: Estimate id.

        """
        return self.estimate_id
  
    def set_estimate_number(self, estimate_number):
        """Set estimate number.

        Args: 
            estimate_number(str): Estimate number.
        
        """
        self.estimate_number = estimate_number

    def get_estimate_number(self):
        """Get estimate number.

        Returns:
            str: Estimate number.
 
        """
        return self.estimate_number
  
    def set_date(self, date):
        """Set the date for estimate.

        Args:
            date(str): Date for estimate.

        """
        self.date = date

    def get_date(self):
        """Get the date of estimate.

        Returns:
            str: Date of estimate.

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
            contact_person(list of instance): List of contact person object.

        """ 
        self.contact_persons.extend(contact_person)
    def get_contact_persons(self):
        """Get contact person.

        Returns:
            list: List of contact person object.
 
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
        """Get currency code.

        Returns:
            str: Currency code.
 
        """
        return self.currency_code
  
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
  
    def set_expiry_date(self, expiry_date):
        """Set expiry date.

        Args:
            expiry_date(str): Expiry date.

        """
        self.expiry_date = expiry_date

    def get_expiry_date(self):
        """Get expiry date.

        Returns:
            str: Expiry date.

        """
        return self.expiry_date
  
    def set_discount(self, discount):
        """Set discount.

        Args:
            discount(float): Discount.

        """
        self.discount = discount

    def get_discount(self):
        """Get discount.

        Returns:
            str: Discount.

        """
        return self.discount
  
    def set_is_discount_before_tax(self, is_discount_before_tax):
        """Set whether to discount before tax or not.

        Args:
            is_discount_before_tax(bool): True to discount before tax.

        """
        self.is_discount_before_tax = is_discount_before_tax

    def get_is_discount_before_tax(self):
        """Get whether to discount before tax or not.

        Returns:
            bool: True to discount before tax.

        """
        return self.is_discount_before_tax
  
    def set_discount_type(self, discount_type):
        """Set type of discount.

        Args:
            discount_type(str): Discount type.

        """
        self.discount_type = discount_type

    def get_discount_type(self):
        """Get type of discount.

        Returns:
            str: Discount type.
   
        """
        return self.discount_type 
  
  
    def set_line_items(self, items):
        """Set line items.
 
        Args:
            items(instance): Line items object.

        """
        self.line_items.append(items)

    def get_line_items(self):
        """Get line items.

        Returns:
            list of instance: List of line items object.

        """
        return self.line_items
      
    def set_shipping_charge(self, shipping_charge):
        """Set shipping charge.

        Args:
            shipping_charge(float): Shipping charge.

        """
        self.shipping_charge = shipping_charge

    def get_shipping_charge(self):
        """Get shipping charge.

        Returns:
            float: Shipping charge.

        """
        return self.shipping_charge
  
    def set_adjustment(self, adjustment):
        """Set adjustment.

        Args:
            adjustment(float): Adjustment.

        """
        self.adjustment = adjustment

    def get_adjustment(self):
        """Get adjustment.

        Returns:
            float: Adjustment.

        """
        return self.adjustment
  
    def set_adjustment_description(self, adjustment_description):
        """Set adjustment description.

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
  
    def set_taxes(self, tax):
        """Set taxes.

        Args:
            taxes(instance): Tax object.

        """
        self.taxes.extend(tax)

    def get_taxes(self):
        """Get taxes.

        Returns:
            list of instance: List of tax object.

        """
        return self.taxes

    def set_billing_address(self, address):
        """Set billing address.

        Args:
            address(instance): Address object.

        """
        self.billing_address = address

    def get_billing_address(self):
        """Get billing address.

        Returns:
            instance: Address object.

        """
        return self.billing_address

    def set_shipping_address(self, address):
        """Set shipping address.

        Args:
            address(instance): Address object.

        """
        self.shipping_address = address

    def get_shipping_address(self):
        """Get shipping address.

        Returns:
            instance: Address object.

        """
        return self.shipping_address
   
    def set_notes(self, notes):
        """Set note.

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
  
    def set_custom_fields(self, custom_field):
        """Set custom fields.

        Args:
            custom_field(instance): Custom field.

        """
        self.custom_fields.append(custom_field)

    def get_custom_fields(self):
        """Get custom field.

        Returns:
             list of instance: List of custom field object.

        """
        return self.custom_fields
 
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
            str: LAst modified time.

        """
        return self.last_modified_time
 
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

    def set_salesperson_name(self, salesperson_name):
        """Set salesperson_name.

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

    def set_accepted_date(self, accepted_date):
        """Set accepted date.

        Args:
            accepted_date(str): Accepted date.

        """
        self.accepted_date = accepted_date

    def get_accepted_date(self):
        """Get accepted date.

        Returns:
            str: Accepted date.

        """
        return self.accepted_date
 
    def set_declined_date(self, declined_date):
        """Set declined date.

        Args: 
            declined_date(str): Declined date.

        """
        self.declined_date = declined_date

    def get_declined_date(self):
        """Get declined date.

        Returns:
            str: Declined date.

        """
        return self.declined_date

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

    def to_json(self):
        """This method is used to comnvert estimates object to json object.

        Returns: 
            dict: Dictionary containing json object for estimates.

        """
        data = {}
        if self.customer_id != '':
            data['customer_id'] = self.customer_id
        if self.estimate_number != '':
            data['estimate_number'] = self.estimate_number
        if self.contact_persons:
            data['contact_persons'] = self.contact_persons
        if self.template_id != '':
            data['template_id'] = self.template_id
        if self.reference_number != '':
            data['reference_number'] = self.reference_number
        if self.date != '':
            data['date'] = self.date
        if self.expiry_date != '':
            data['expiry_date'] = self.expiry_date
        if self.exchange_rate > 0:
            data['exchange_rate'] = self.exchange_rate
        if self.discount > 0:
            data['discount'] = self.discount
        if self.is_discount_before_tax is not None:
            data['is_discount_before_tax'] = self.is_discount_before_tax
        if self.discount_type != '':
            data['discount_type'] = self.discount_type
        if self.salesperson_name != '':
            data['salesperson_name'] = self.salesperson_name
        if self.custom_fields:
            data['custom_fields'] = []
            for value in self.custom_fields:
                custom_field = value.to_json()
                data['custom_fields'].append(custom_field)
        if self.line_items:
            data['line_items'] = []
            for value in self.line_items:
                line_item = value.to_json()
                data['line_items'].append(line_item)
        if self.notes != '':
            data['notes'] = self.notes
        if self.terms != '':
            data['terms'] = self.terms
        if self.shipping_charge > 0:
            data['shipping_charge'] = self.shipping_charge
        if self.adjustment != '':
            data['adjustment'] = self.adjustment
        if self.adjustment_description != '':
            data['adjustment_description'] = self.adjustment_description
        return data

