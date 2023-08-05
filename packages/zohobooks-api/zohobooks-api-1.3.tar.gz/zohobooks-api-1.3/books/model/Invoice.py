#$Id$

class Invoice:
    """This class is used to create object for invoice."""
    def __init__(self):
        """Initialize parameters for Invoice object."""
        self.invoice_id = ''
        self.invoice_number = ''
        self.date = ''
        self.status = ''
        self.payment_terms = 0
        self.payment_terms_label = ''
        self.due_date = ''
        self.payment_expected_date = ''
        self.last_payment_date = ''
        self.reference_number = ''
        self.customer_id = ''
        self.customer_name = ''
        self.contact_persons = []
        self.currency_id = ''
        self.currency_code = ''
        self.exchange_rate = 0.00
        self.discount = ''
        self.is_discount_before_tax = None
        self.discount_type = ''
        self.recurring_invoice_id = ''
        self.line_items = []
        self.shipping_charge = 0.00
        self.adjustment = 0.0
        self.adjustment_description = ''
        self.sub_total = 0.0
        self.tax_total = 0.0
        self.total = 0.0
        self.taxes = []
        self.payment_reminder_enabled = None
        self.payment_made = 0.0
        self.credits_applied = 0.0
        self.tax_amount_withheld = 0.0
        self.balance = 0.0
        self.write_off_amount = 0.0
        self.allow_partial_payments = None
        self.price_precision = 2
        self.payment_options = {
            'payment_gateways': []
            }
        self.is_emailed = False
        self.reminders_sent = 0
        self.last_reminder_sent_date = ''
        self.billing_address = ''
        self.shipping_address = ''
        self.notes = ''
        self.terms = ''
        self.custom_fields = []
        self.template_id = ''
        self.template_name = ''
        self.created_time = ''
        self.last_modified_time = ''
        self.attachment_name = ''
        self.can_send_in_mail = None
        self.salesperson_id = ''
        self.salesperson_name = ''
        self.invoice_url = ''
        self.invoice_payment_id = ''
        self.due_days = ''
        self.custom_body = ''
        self.custom_subject = ''
        self.invoiced_estimate_id = ''
        self.amount_applied = ''
        self.name = ''
        self.value = ''
        self.gst_no = ''
        self.reason = ''

    
    def set_name(self, name):
        """Set name.

        Args:
            name(str): Name.

        """
        self.name = name

    def get_name(self):
        """Get name.

        Returns:
            str: Name.

        """
        return self.name

    def set_value(self,value):
        """Set value.

        Args:
            value(str): Value.

        """
        self.value = value

    def get_value(self):
        """Get value.

        Returns:
            str: Value.

        """
        return self.value
  
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
 
    def set_invoice_number(self, invoice_number):
        """Set invoice number.

        Args:
            invoice_numeber(str): Invoice number.
 
        """
        self.invoice_number = invoice_number
 
    def get_invoice_number(self):
        """Get invoice number.
        
        Returns:
            str: Invoice number.
  
        """
        return self.invoice_number

    def set_date(self, date):
        """Set date at which the invoice is created.
 
        Args:
            date(str): Date at which invoice is created.

        """
        self.date = date

    def get_date(self):
        """Get date at which invoice is created.

        Returns:
            str:  Date at which invoice is created.

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

    def set_payment_terms(self, payment_terms):
        """Set payment terms in days.Invoice due date will be calculated based on this.
      
        Args:
            payment_terms(int): Payment terms in days.Eg 15, 30, 60.

        """ 
        self.payment_terms = payment_terms

    def get_payment_terms(self):
        """Get payment terms.

        Returns:
            int: Payment terms in days.

        """
        return self.payment_terms

    def set_payment_terms_label(self, payment_terms_label):
        """Set Payments terms label. 

        Args:
            payment_terms_label(str): Payment terms label. Default value for 15 days is  "Net 15".

        """         
        self.payment_terms_label = payment_terms_label

    def get_payment_terms_label(self):
        """Get payment terms label.

        Returns:
            str: PAyment terms label.

        """
        return self.payment_terms_label
  
    def set_due_date(self, due_date):
        """Set due date for invoice.

        Args:
            due_date(str): Due date for invoice. Format is yyyy-mm-dd.

        """
        self.due_date = due_date

    def get_due_date(self):
        """Get due date of invoice.

        Returns:
            str: Due date dor invoice.

        """
        return self.due_date
   
    def set_payment_expected_date(self, payment_expected_date):
        """Set payment expected date.

        Args:
            payment_expected_date(str): Payment expected date.

        """
        self.payment_expected_date = payment_expected_date

    def get_payment_expected_date(self): 
        """Get payment expected date.

        Returns:
            str: Payment expected date.

        """
        return self.payment_expected_date

    def set_last_payment_date(self, last_payment_date):
        """Set last payment date.
 
        Args:
            last_payment_date(str): last_payment_date

        """
        self.last_payment_date = last_payment_date

    def get_last_payment_date(self):
        """Get last payment date.
 
        Returns:
            str: last payment date.

        """
        return self.last_payment_date
   
    def set_reference_number(self, reference_number):
        """Set reference number for the customer payment.
 
        Args:
            reference_number(str): Reference number.

        """
        self.reference_number = reference_number
 
    def get_reference_number(self): 
        """Get reference number for the customer payment.

        Returns:
            str: Reference number.

        """
        return self.reference_number

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
        """Set the list of ID of contact persons for which thank you mail has to be sent.

        Args:
            contact_peson(list): Id of contact persons for which thank you mail has to be sent.

        """
        self.contact_persons.extend(contact_person)

    def get_contact_persons(self):
        """Get the Id of contact persons for which thank you mail has to be sent.

        Returns: 
            list: List of ID of contact persons.

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
        """Set exchange rate for the currency.
  
        Args:
            exchange_rate(int): Exchange rate.
        
        """  
        self.exchange_rate = exchange_rate

    def get_exchange_rate(self):
        """Get exchange rate of the currency.
        
        Returns:
            int: Exchange rate.

        """
        return self.exchange_rate

    def set_discount(self, discount):
        """Set discount applied to the invoice.
         
        Args: 
            discount(str): Discount. It can be either in % or in amount.
   
        """
        self.discount = discount

    def get_discount(self):
        """Get discount applied to the invoice.
 
        Returns:
            str: Discount.
        
        """
        return self.discount

    def set_is_discount_before_tax(self, is_discount_before_tax):
        """Set whether to discount before tax or after tax.

        Args:
            is_discount_before_tax(bool): True to discount before tax else False to discount after tax.

        """
        self.is_discount_before_tax = is_discount_before_tax
     
    def get_is_discount_before_tax(self):
        """Get whether to discount before tax or after tax.
 
        Returns:
            bool: True to discount before tax else False to discount after tax.

        """
        return self.is_discount_before_tax
   
    def set_discount_type(self, discount_type):
        """Set how the discount should be specified.
 
        Args:
            discount_type: Discount type. Allowed values are entity_level or item_level

        """
        self.discount_type = discount_type

    def get_discount_type(self):
        """Get discount type.
        
        Returns:
            str: Discount type.
 
        """
        return self.discount_type
   
    def set_recurring_invoice_id(self, recurring_invoice_id):
        """Set id of the recurring invoice from which the invoice is created.
 
        Args:
            recurring_invoice_id(str): Recurring invoice id.
 
        """
        self.recurring_invoice_id = recurring_invoice_id

    def get_recurring_invoice_id(self):
        """Get id of the recurring invoice from which the invoice is created.

        Returns:
            str: Recurring invoice id.
 
        """
        return self.recurring_invoice_id

    def set_line_items(self, line_item):
        """Set line items for an invoice.
        
        Args: 
            instance: Line item object.

        """
        self.line_items.append(line_item)

    def get_line_items(self):
        """Get line items of an invoice.
        
        Returns:
            list: List of line items object

        """
        return self.line_items
   
    def set_shipping_charge(self, shipping_charge):
        """Set shipping charge for the invoice.
 
        Args:
            shipping_charge(float): Shipping charge.

        """
        self.shipping_charge = shipping_charge
 
    def get_shipping_charge(self):
        """Get shipping charge for the invoice.

        Returns: 
            float: Shipping charge.

        """
        return self.shipping_charge
   
    def set_adjustment(self, adjustment):
        """Set adjustments made to the invoice.
     
        Args:
            adjustment(float): Adjustments made.

        """
        self.adjustment = adjustment

    def get_adjustment(self):
        """Get adjustments made to the invoice.
        
        Returns:
            float: Adjustments made.

        """
        return self.adjustment
   
    def set_adjustment_description(self, adjustment_description):
        """Set to customize adjustment description.
        
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
  
    def set_total(self, total):
        """Set total.
    
        Args:
            total(float): Total amount.
 
        """
        self.total = total

    def get_total(self):
        """Get total.
      
        Returns:
            float: Total amount.
 
        """
        return self.total
  
    def set_taxes(self, tax):
        """Set taxes.

        Args:
            tax(instance): Tax.

        """ 
        self.taxes.append(tax)
 
    def get_taxes(self):
        """Get taxes.
        
        Returns:
            list: List of tax objects.

        """
        return self.taxes

    def set_payment_reminder_enabled(self, payment_reminder_enabled):
        """Set whether to enable payment reminder or not.

        Args:
            payment_reminder_enabled(bool): True to enable payment reminder else False.

        """
        self.payment_reminder_enabled = payment_reminder_enabled

    def get_payment_reminder_enabled(self):
        """Get whether payment reminder is enabled or not.

        Returns:
            bool: True if payment reminder is enabled else False.

        """
        return self.payment_reminder_enabled

    def set_payment_made(self, payment_made):
        """Set payment made.

        Args:
            payment_made(float): Payments made.

        """
        self.payment_made = payment_made

    def get_payment_made(self):
        """Get payments made.

        Returns:
            float: Payments made.

        """
        return self.payment_made
 
    def set_credits_applied(self, credits_applied):
        """Set credits applied.

        Args: 
            credits_applied(float): Credits applied.
 
        """
        self.credits_applied = credits_applied

    def get_credits_applied(self): 
        """Get credits applied.
    
        Returns:
            float: Credits applied.
      
        """
        return self.credits_applied

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

    def set_write_off_amount(self, write_off_amount):
        """Set write off amount.
     
        Args:
            write_off_amount(float): Write off amount.

        """ 
        self.write_off_amount = write_off_amount
 
    def get_write_off_amount(self):
        """Get write off amount.
 
        Returns:
            float: Write off amount.
      
        """
        return self.write_off_amount

    def set_allow_partial_payments(self, allow_partial_payments):
        """Set whether to allow partial payments or not.

        Args:
            allow_partial_payments(bool): True to allow partial payments else False.
  
        """
        self.allow_partial_payments = allow_partial_payments

    def get_allow_partial_payments(self):
        """Get whether to allow partial payments.
  
        Returns:
            bool: True if partial payments are allowed else False.

        """
        return self.allow_partial_payments

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

    def set_payment_options(self, payment_gateways):
        """Set payment options.

        Args: 
            payment_gateways(instance): Online payment gateways through which payment can be made.
        
        """
        self.payment_options['payment_gateways'].append(payment_gateways)

    def get_payment_options(self):
        """Get payment options.
 
        Returns:
            dict: Payment options for the invoice.

        """
        return self.payment_options
  
    def set_is_emailed(self, is_emailed):
        """Set whether to email or not.
        
        Args: 
            is_emailed(bool): True to email else False.

        """
        self.is_emailed = is_emailed

    def get_is_emailed(self):
        """Get whether to email.
        
        Returns:
            bool: True to email else False.
 
        """
        return self.is_emailed
   
    def set_reminders_sent(self, reminders_sent):
        """Set reminders sent. 
      
        Args:
            reminders_sent(int): Reminders sent.

        """
        self.reminders_sent = reminders_sent

    def get_reminders_sent(self):
        """Get reminders sent.

        Returns:
            int: Reminders sent.

        """
        return self.reminders_sent

    def set_last_reminder_sent_date(self, last_reminder_sent_date):
        """Set last reminder sent date.
     
        Args:
            last_reminder_sent_date(str): Last reminder sent date

        """
        self.last_reminder_sent_date = last_reminder_sent_date

    def get_last_reminder_sent_date(self):
        """Get last reminder sent date.

        Returns:
            str: Last reminder sent date.
 
        """
        return self.last_reminder_sent_date

    def set_billing_address(self, billing_address):
        """Set billing address.

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
    
    def set_shipping_address(self, shipping_address):
        """Set shipping address.
 
        Args:
            shipping_address(instance): Shipping address object.
 
        """
        self.shipping_address = shipping_address
 
    def get_shipping_address(self):
        """Get shipping address.

        Returns:
            instance: Shipping address object.

        """
        return self.shipping_address

    def set_notes(self, notes):
        """Set notes.

        Args: 
            notes(str): Notes.

        """
        self.notes = notes

    def get_notes(self):
        """Get notes.

        Returns: 
            str: Notes

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
            custom_field(instance): custom field object.
 
        """
        self.custom_fields.append(custom_field)
 
    def get_custom_fields(self):
        """Get custom field.

        Returns: 
            instance: custom field object.
 
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
            str: Last modified time.

        """
        return self.last_modified_time
  
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

    def set_can_send_in_mail(self, can_send_in_mail):
        """Set whether the invoice can be sent in mail or not.

        Args:
            can_send_in_mail(bool): True if it can be sent in mail else False.

        """
        self.can_send_in_mail = can_send_in_mail

    def get_can_send_in_mail(self):
        """Get whether the invoice can be sent in mail or not.

        Returns:
            bool: True if it can be sent in mail else False.

        """
        return self.can_send_in_mail
  
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
        """Set salesperson name.

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

    def set_invoice_url(self, invoice_url):
        """Set invoice url.

        Args:
            invoice_url(str): Invoice url.
 
        """
        self.invoice_url = invoice_url
 
    def get_invoice_url(self):
        """Get invoice url.
       
        Returns:
            str: Invoice url.

        """
        return self.invoice_url
  
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

    def set_custom_body(self, custom_body):
        """Set custom body.

        Args:
            custom_body(str): Custom body.

        """
        self.custom_body = custom_body
 
    def get_custom_body(self):
        """Get custom body.

        Returns:
            str: Custom body.

        """
        return self.custom_body

    def set_custom_subject(self, custom_subject):
        """Set custom subject.

        Args:
            custom_subject(str): Custom subject.

        """
        self.custom_subjecct = custom_subject
 
    def get_custom_subject(self):
        """Get custom subject.

        Returns:
            str: Custom subject.

        """
        return self.custom_subject

    def set_invoiced_estimate_id(self, invoiced_estimate_id):
        """Set invoiced estimate id.
 
        Args:
            invoiced_estimate_id(str): Invoiced estimate id.

        """
        self.invoiced_estimate_id = invoiced_estimate_id

    def get_invoiced_estimate_id(self): 
        """Get invoiced estimate id.

        Returns:
            str: Invoiced estimate id.

        """
        return self.invoiced_estimate_id
   
    def set_amount_applied(self, amount_applied):
        """Set amount applied.
  
        Args: 
            amount_applied(str): Amount applied.
 
        """
        self.amount_applied = amount_applied

    def get_amount_applied(self):
        """Get amount applied.

        Returns:
            str: Amount applied.

        """
        return self.amount_applied
 
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

    def to_json(self):
        """This method is used to convert invoice object to json object.

        Returns:
            dict: Dictionary containing json object for invoices.

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
        if self.payment_terms > 0:
            data['payment_terms'] = self.payment_terms
        if self.payment_terms_label != '':
            data['payment_terms_label'] = self.payment_terms_label
        if self.due_date != '':
            data['due_date'] = self.due_date
        if self.discount != '':
            data['discount'] = self.discount
        if self.is_discount_before_tax is not None:
            data['is_discount_before_tax'] = self.is_discount_before_tax 
        if self.discount_type != '':
            data['discount_type'] = self.discount_type
        if self.exchange_rate > 0:
            data['exchange_rate'] = self.exchange_rate
        if self.recurring_invoice_id != '':
            data['recurring_invoice_id'] = self.recurring_invoice_id
        if self.invoiced_estimate_id != '':
            data['invoiced_estimate_id'] = self.invoiced_estimate_id
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
        if self.payment_options['payment_gateways']:
            data['payment_options'] = {'payment_gateways':[]}
            for value in self.payment_options['payment_gateways']:
                payment_gateway = value.to_json()
                data['payment_options']['payment_gateways'].append(payment_gateway)
        if self.allow_partial_payments != None:
            data['allow_partial_payments'] = self.allow_partial_payments
        if self.custom_body != '':
            data['custom_body'] = self.custom_body
        if self.custom_subject != '':
            data['custom_subject'] = self.custom_subject
        if self.notes != '':
            data['notes'] = self.notes
        if self.terms != '':
            data['terms'] = self.terms
        if self.shipping_charge > 0:
            data['shipping_charge'] = self.shipping_charge
        if self.adjustment > 0: 
            data['adjustment'] = self.adjustment
        if self.adjustment_description != '':
            data['adjustment_description'] = self.adjustment_description
        if self.invoice_number != '':
            data['invoice_number'] = self.invoice_number
        if self.reason != '':
            data['reason'] = self.reason
        if self.invoice_id != '':
            data['invoice_id'] = self.invoice_id
        if self.amount_applied != '':
            data['amount_applied'] = self.amount_applied
        if self.total != '':
            data['total'] = self.total
        return data
