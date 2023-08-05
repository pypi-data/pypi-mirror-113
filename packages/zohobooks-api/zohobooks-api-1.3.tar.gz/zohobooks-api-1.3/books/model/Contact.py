#$Id$

from books.model.Address import Address
from books.model.DefaultTemplate import DefaultTemplate

class Contact:
    """This class is used to create object for contacts."""
    def __init__(self):
        """Initialize the parameters for contacts object."""
        self.contact_id = ''
        self.contact_name = ''
        self.company_name = ''
        self.contact_salutation = ''
        self.has_transaction = None
        self.contact_type = ''
        self.is_crm_customer = None
        self.primary_contact_id = ''
        self.price_precision = 0
        self.payment_terms = 0
        self.payment_terms_label = ''
        self.currency_id = ''
        self.currency_code = ''
        self.currency_symbol = ''
        self.outstanding_receivable_amount = 0.00
        self.outstanding_receivable_amount_bcy = 0.00
        self.outstanding_payable_amount = 0.00
        self.outstanding_payable_amount_bcy = 0.00
        self.unused_credits_receivable_amount = 0.00
        self.unused_credits_receivable_amount_bcy = 0.00
        self.unused_credits_payable_amount = 0.00
        self.unused_credits_payable_amount_bcy = 0.00
        self.status = ''
        self.payment_reminder_enabled = None
        self.notes = ''
        self.created_time = ''
        self.last_modified_time = ''
        self.first_name = ''
        self.last_name = ''
        self.email = ''
        self.phone = ''
        self.mobile = ''
        self.custom_fields = []
        self.track_1099 =  None   
        self.tax_id_type =  ''
        self.tax_id_value =  ''
        self.billing_address = Address()
        self.shipping_address = Address()
        self.contact_persons = []
        self.default_templates = DefaultTemplate()
        self.gst_treatment = ''
        self.place_of_contact = ''
        self.gst_no = ''
    
    def set_gst_no(self, gst_no):
        """Set gst_no for the contact.
 
        Args: 
            gst_no(str): gst_no of the contact.
        
        """
        self.gst_no = gst_no
 
    def get_gst_no(self):
        """Get gst_no of the contact.
       
        Returns:
            str: gst_no of the contact.
   
        """
        return self.gst_no

    def set_place_of_contact(self, place_of_contact):
        """Set place_of_contact for the contact.

        Args:
            place_of_contact(str): place_of_contact of the contact.

        """
        self.place_of_contact = place_of_contact

    def get_place_of_contact(self):
        """Get place_of_contact of the contact.

        Returns:
            str: place_of_contact of the contact.

        """
        return self.place_of_contact

    def set_gst_treatment(self, gst_treatment):
        """Set gst_treatment for the contact.

        Args:
            gst_treatment(str): gst_treatment of the contact.

        """
        self.gst_treatment = gst_treatment

    def get_gst_treatment(self):
        """Get gst_treatment of the contact.

        Returns:
            str: gst_treatment of the contact.

        """
        return self.gst_treatment

    def set_contact_id(self, contact_id):
        """Set contact id for the contact.

        Args:
            contact_id(str): Contact id of the contact.

        """
        self.contact_id = contact_id

    def get_contact_id(self):
        """Get contact_id of the contact.

        Returns:
            str: Contact id of the contact.

        """
        return self.contact_id

    def set_contact_name(self, contact_name):
        """Set contact name for the contact.
        
        Args:
            contact_name(str): Contact name of the contact.
         
        """
        self.contact_name = contact_name

    def get_contact_name(self):
        """Get contact name of the contact.
          
        Returns:
            str: Contact name of the contact.
      
        """ 
        return self.contact_name
      
    def set_has_transaction(self, has_transaction):
        """Set whether the contact has transaction or not.
        
        Args:
            has_transaction(bool): True if the contact has transactions 
                else False.
         
        """
        self.has_transaction = has_transaction
 
    def get_has_transaction(self):
        """Get whether the contact has transaction or not.
        
        Returns:
            bool: True if the contact has transactions else False.
      
        """
        return self.has_transaction

    def set_contact_type(self, contact_type):
        """Set contact type of the contact.
      
        Args:
            contact_type(str): Contact type of the contact.
  
        """
        self.contact_type = contact_type
 
    def get_contact_type(self):
        """Get contact type of the contact.
        
        Returns:
            str: Contact type of the contact.
          
        """
        return self.contact_type

    def set_is_crm_customer(self, is_crm_customer):
        """Set whether the contact is crm customer or not.
     
        Args:
            is_crm_customer(bool): True if the contact is crm customer else 
                False.
        
        """
        self.is_crm_customer = is_crm_customer

    def get_is_crm_customer(self):
        """Get whether the contact is crm customer or not.
     
        Returns:
            bool: True if the contact is crm customer else False .
        
        """
        return self.is_crm_customer

    def set_primary_contact_id(self, primary_contact_id):
        """Set primary contact id for the contact.
       
        Args:
            primary_contact_id(str): Primary contact id for the contact.
         
        """
        self.primary_conatact_id = primary_contact_id
 
    def get_primary_conatact_id(self):
        """Get primary contact id for the contact.
 
        Returns:
            str: Primary contact id for the contact.

        """ 
        return self.primary_conatact_id

    def set_payment_terms(self, payment_terms):
        """Set payment terms for the contact.
 
        Args:
            payment_terms(int): Payment terms for the contact.
 
        """
        self.payment_terms = payment_terms

    def get_payment_terms(self):
        """Get payment terms of the contact.
         
        Returns:
            int: Payment terms of the contact.
 
        """
        return self.payment_terms

    def set_payment_terms_label(self, payment_terms_label):
        """Set payment terms label for the contact.
     
        Args:
            payment_terms_label(str): Payment terms for the contact.
  
        """
        self.payment_terms_label = payment_terms_label

    def get_payment_terms_label(self):
        """Get payment terms label of the contact.
 
        Returns:
            str: Payment terms label of the contact.
 
        """
        return self.payment_terms_label

    def set_currency_id(self, currency_id):
        """ Set currency id for the contact.
        
        Args:
            currency_id(str): Currency id for the contact.
        
        """
        self.currency_id = currency_id
 
    def get_currency_id(self):
        """Get currency id of the contact.

        Args:
            currency_id(str): Currency id for the contact.
 
        """
        return self.currency_id

    def set_currency_code(self, currency_code):
        """Set currency code for the contact.
         
        Args: 
            currency_code(str): Currency code for the contact.
 
        """
        self.currency_code = currency_code 
 
    def get_currency_code(self):
        """Get currency code of the contact.

        Returns:
            str: Currency code of the contact.
 
        """
        return self.currency_code

    def set_currency_symbol(self, currency_symbol):
        """Set currency symbol for the contact.
        
        Args:
            currency_symbol(str): Currency symbol for the contact.
 
        """
        self.currency_symbol = currency_symbol

    def get_currency_symbol(self):
        """Get currency symbol of the contact.
      
        Returns:
            str: Currency symbol of the contact.
 
        """
        return self.currency_symbol

    def set_outstanding_receivable_amount(self, outstanding_receivable_amount):
        """Set outstanding receivable amount for the contact.

        Args: 
            outstanding_receivable_amount(float): Outstanding receivable amount
                 for the contact.
     
        """
        self.outstanding_receivable_amount = outstanding_receivable_amount

    def get_outstanding_receivable_amount(self):
        """Get outstanding receivable amount of the contact.
       
        Returns:
            float: Outstanding receivable amount of the contact.

        """
        return self.outstanding_receivable_amount 

    def set_outstanding_receivable_amount_bcy(self, \
        outstanding_receivable_amount_bcy):
        """Set outstanding receivable amount bcy for the contact.
 
        Args:
            outstanding_receivable_amount_bcy(float): Outstanding receivable 
                amount bcy for the contact.
   
        """
        self.outstanding_receivable_amount_bcy = \
        outstanding_receivable_amount_bcy

    def get_outstanding_receivable_amount_bcy(self):
        """Get the outstanding receivable amount bcy of the contact.
        
        Returns:
            float: Outstanding receivable amount bcy of the contact.

        """
        return self.outstanding_receivable_amount_bcy

    def set_outstanding_payable_amount(self, outstanding_payable_amount):
        """Set the outstanding payable amount for the contact.
        
        Args:
            outstanding_payable_amount(float): Outstanding payable amount for 
                the contact.

        """
        self.outstanding_payable_amount = outstanding_payable_amount
 
    def get_outstanding_payable_amount(self):
        """Get the outstanding payable amount of the contact.
      
        Returns:
            float: Outstanding payable amount of the contact.
         
        """
        return self.outstanding_payable_amount

    def set_outstanding_payable_amount_bcy(self, \
        outstanding_payable_amount_bcy):
        """Set outstanding payable amount bcy for the contact.
       
        Args:
            outstanding_payable_amount_bcy(float): Outstanding payable amount 
                bcy for the contact.
  
        """
        self.outstanding_payable_amount_bcy = outstanding_payable_amount_bcy

    def get_outstanding_payable_amount_bcy(self):
        """Get outstanding payable amount bcy of the contact.
         
        Returns:
            float: Outstanding payable amount bcy of the contact.

        """
        return self.outstanding_payable_amount_bcy

    def set_unused_credits_receivable_amount(self, \
        unused_credits_receivable_amount):
        """Set unused credits receivable amount for the contact.
 
        Args: 
            unused_credits_receivable_amount(float): Unused credits receivable 
                amount for the contact.
       
        """
        self.unused_credits_receivable_amount = \
        unused_credits_receivable_amount

    def get_unused_credits_receivable_amount(self):
        """Get unused credits receivable amount of the contact.
 
        Returns:
            float: Unused credits receivable amount for the contact.
         
        """
        return self.unused_credits_receivable_amount

    def set_unused_credits_receivable_amount_bcy(self, \
        unused_credits_receivable_amount_bcy):
        """Set unused credits receivable amount bcy for the contact.
        
        Args:
            unused_credits_receivable_amount_bcy(float): Unused credits 
                receivable amount bcy for the contact.
 
        """
        self.unused_credits_receivable_amount_bcy = \
        unused_credits_receivable_amount_bcy

    def get_unused_credits_receivable_amount_byc(self):
        """Get unused credits receivable amount bcy of the contact.
        
        Returns:
            float: Unused credits receivable amount bcy of the contact.
    
        """
        return self.unused_credits_receivable_amount_bcy

    def set_unused_credits_payable_amount(self, unused_credits_payable_amount):
        """Set unused credits payable amount for the contact.
        
        Args:
            unused_credits_payable_amount(float): Unused credits payable 
                amount for the contact.

        """
        self.unused_credits_payable_amount = unused_credits_payable_amount

    def get_unused_credits_payable_amount(self):
        """Get unused payable amount of the contact.
         
        Returns:
            float: Unused payable amount of the contact.

        """
        return self.unused_credits_payable_amount

    def set_unused_credits_payable_amount_bcy(self, \
        unused_credits_payable_amount_bcy):
        """Set unused credits payable amount bcy for the contact.
        
        Args:
            unused_credits_payable_amount_bcy(float): Unused credits payable 
                amount bcy for the contact.
 
        """
        self.unused_credits_payable_amount_bcy = \
        unused_credits_payable_amount_bcy

    def get_unused_credits_payable_amount_bcy(self):
        """Get unused credits payable amount bcy of the contact.
 
        Returns:
            float: Unused credits payable amount bcy of the contact.

        """
        return self.unused_credits_payable_amount_bcy

    def set_status(self, status):
        """Set status for the contact.
       
        Args:
            status(str): Status of the contact.
        
        """
        self.status = status
 
    def get_status(self):
        """Get status of the contact.
        
        Returns:
            str: Status of the contact.
         
        """
        return self.status

    def set_payment_reminder_enabled(self, payment_reminder_enabled):
        """Set whether to enabe payment reminder for the contact.
       
        Args: 
            payment_reminder_enabled(bool): True if enable payment reminder 
                else false.

        """
        self.payment_reminder_enabled = payment_reminder_enabled
  
    def get_payment_reminder_enabled(self):
        """Get whether the payment reminder is enabled or not
 
        Returns:
            bool: True if payment reminder is enabled else false.

        """
        return self.payment_reminder_enabled   

    def set_notes(self, notes):
        """Set notes for the contact.
   
        Args:
            notes(str): Notes for contact.
   
        """
        self.notes = notes
 
    def get_notes(self):
        """Get notes of the contact.
 
        Returns:
            str: Notes of the contact.
  
        """
        return self.notes

    def set_created_time(self, created_time):
        """Set created time for the contact.
        
        Args:
            created_time(str): Created time for the contact.
 
        """
        self.created_time = created_time

    def get_created_time(self):
        """Get created of the contact.
       
        Returns:
            str: Created time of the contact.
 
        """
        return self.created_time

    def set_last_modified_time(self, last_modified_time):
        """Set last modified time for the contact.
        
        Args:
            last_modified_time(str): Last modified time for the contact.

        """
        self.last_modified_time = last_modified_time  

    def get_last_modified_time(self):
        """Get last modified time of the contact.
        
        Returns:
            str: Last modified time of the contact.
      
        """
        return self.last_modified_time
 
    def set_billing_address(self, billing_address):
        """Set billing address for the contact.
        
        Args:
            billing_address(Address): Billing address for the contact.
    
        """
        self.billing_address = billing_address
  
    def get_billing_address(self):
        """Get billing address of the contact.
         
        Returns:
            Address: Billing address of the contact.

        """
        return self.billing_address

    def set_shipping_address(self, shipping_address):
        """Set shipping address for the contact.
        
        Args:
            shipping_address(Address): Shipping address for the contact.

        """
        self.shipping_address = shipping_address

    def get_shipping_address(self):
        """Get shipping address of the contact.
         
        Returns:
            Address: Shipping address of the contact.

        """
        return self.shipping_address
   
    def set_contact_persons(self, contact_person):
        """Set contact persons for the contact.
        
        Args:
            contact_person(list): List of contact persons object.
        
        """
        self.contact_persons.extend(contact_person)
 
    def get_contact_persons(self):
        """Get contact persons of a contact.
        
        Returns:
            list: List of contact persons.

        """
        return self.contact_persons

    def set_default_templates(self, default_templates):
        """Set default templates for the contact.
        
        Args:
            default_templates(instance): Default templates object.
        
        """
        self.default_templates = default_templates
 
    def get_default_templates(self):
        """Get default templates of the contact.
        
        Returns:
            instance: Default templates instance.
  
        """
        return self.default_templates
  

    def set_custom_fields(self, custom_field):
        """Set custom fields for a contact.
       
        Args: 
            custom_field(instance): Custom field object.
  
        """
        self.custom_fields.append(custom_field)

    def get_custom_fields(self):
        """Get custom fields of the contact.
        
        Returns:
            instance: Custom field of the contact.
 
        """
        return self.custom_fields

    def set_company_name(self, company_name):
        """Set company name for the contact.
        
        Args:
            company_name(str): Company name of the contact.

        """
        self.company_name = company_name
 
    def get_company_name(self):
        """Get company name of the contact.
        
        Returns:
            str: cCompany name of the contact.
        """
        return self.company_name

    def set_contact_salutation(self, contact_salutation):
        """Set salutation for the contact.
        
        Args: 
            contact_salutation(str): Salutation of the contact.
       
        """
        self.contact_salutation = contact_salutation
 
    def get_contact_salutation(self):
        """Get salutation of the contact.
      
        Returns:
            str: Salutation of the contact
  
        """
        return self.contact_salutation

    def set_price_precision(self, price_precision):
        """Set price precision for the contact.
        
        Args:
            price_precision(int): Price precision for the contact.
       
        """
        self.price_precision = price_precision
 
    def get_price_precision(self):
        """Get price precision of the contact.
 
        Returns:
            int: Price precision of the contact.
 
        """
        return self.price_precision

    def set_track_1099(self, track_1099):
        """Set to track a contact for 1099 reporting.
        
        Args:
            track_1099(bool): True to track a contact for 1099 reporting else 
                False.
 
        """
        self.track_1099 = track_1099
 
    def get_track_1099(self):
        """Get whether a contact is set for 1099 tracking.
          
        Returns:
            bool: True if a contact is set for 1099 tracking else False.
 
        """
        return self.track_1099 

    def set_tax_id_type(self, tax_id_type):
        """Set tax id type for a contact.
      
        Args: 
            tax_id_type(str): tax id type for a contact
 
        """
        self.tax_id_type = tax_id_type

    def get_tax_id_type(self):
        """Get tax id type of a contact.
        
        Returns:
            str: Tax id type for a contact.
    
        """
        return self.tax_id_type

    def set_tax_id_value(self, tax_id_value):
        """Set tax id value for a contact.
        
        Args:
            tax_id_value(str): Tax id value for a contact.
 
        """
        self.tax_id_value = tax_id_value

    def get_tax_id_value(self):
        """Get tax id value of a contact.
        
        Returns:
            str: Tax id value of a contact.

        """
        return self.tax_id_value

    def set_first_name(self, first_name): 
        """Set first name.
 
        Args:
            first_name = First name.    
     
        """
        self.first_name = first_name
       
    def get_first_name(self):
        """Get first name.
 
        Returns:
            str: First name.
 
        """
        return self.first_name

    def set_last_name(self, last_name):
        """Set last name.

        Args:
            last_name = Last name.
       
        """
        self.last_name = last_name

    def get_last_name(self):
        """Get last name.

        Returns:
            str: Last name.
  
        """
        return self.last_name

    def set_email(self, email):
        """Set email.
 
        Args:
            email(str): Email.

        """
        self.email = email

    def get_email(self):
        """Get email.

        Returns:
            str: Email.
 
        """
        return self.email

    def set_phone(self, phone):
        """Set phone.
     
        Args: 
            phone(str): Phone.

        """
        self.phone = phone

    def get_phone(self):
        """Get phone.

        Returns:
            str: Phone.

        """
        return self.phone

    def set_mobile(self, mobile):
        """Set mobile.
 
        Args:
            mobile(str): Mobile.

        """
        self.mobile = mobile

    def to_json(self):
        """This method is used to convert the contact object to JSON object.

        Returns:
            dict: Dictionary containing details of contact object.

        """
        data = {}
        data['email'] = self.email
        if self.company_name != '':
            data['company_name'] = self.company_name
        if self.contact_name != '':
            data['contact_name'] = self.contact_name
        if self.payment_terms != '':
            data['payment_terms'] = self.payment_terms
        if self.payment_terms_label != '':
            data['payment_terms_label'] = self.payment_terms_label
        if self.currency_id != '':
            data['currency_id'] = self.currency_id
        if self.billing_address is not None: 
            billing_address = self.billing_address
            data['billing_address'] = billing_address.to_json()
        if self.shipping_address is not None:
            shipping_address = self.shipping_address
            data['shipping_address'] = shipping_address.to_json()
        if self.gst_no != '':
            data['gst_no'] = self.gst_no
        if self.place_of_contact != '':
            data['place_of_contact'] = self.place_of_contact
        if self.gst_treatment != '':
            data['gst_treatment'] = self.gst_treatment
        if self.contact_persons:
            data['contact_persons'] = []
            for value in self.contact_persons:
                data['contact_persons'].append(value.to_json())
        if self.notes != '':
            data['notes'] = self.notes
        return data
