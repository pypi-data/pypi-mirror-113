#$Id$#

from books.model.Invoice import Invoice
from books.model.PageContext import PageContext
from books.model.InvoiceList import InvoiceList
from books.model.LineItem import LineItem
from books.model.Tax import Tax
from books.model.CustomField import CustomField
from books.model.Address import Address
from books.model.PaymentGateway import PaymentGateway
from books.model.Email import Email
from books.model.FromEmail import FromEmail
from books.model.ToContact import ToContact
from books.model.EmailTemplate import EmailTemplate
from books.model.Template import Template
from books.model.InvoicePayment import InvoicePayment
from books.model.InvoiceCredited import InvoiceCredited
from books.model.InvoiceCreditedList import InvoiceCreditedList
from books.model.Comment import Comment
from books.model.PaymentAndCredit import PaymentAndCredit
from books.model.CommentList import CommentList
from books.model.PaymentList import PaymentList
from books.model.TemplateList import TemplateList

class InvoicesParser:
    """This class is used to parse the json for Invoices."""
 
    def get_list(self,response):
        """This method parses the given resonse and creates invoice list 
            object.
       
        Args:
            response(dict): Response containing json object for invoice list.

        Returns:
            instance: Invoice list object.

        """
        invoice = response['invoices']
        invoice_list = InvoiceList()
        for value in invoice: 
            invoice_object = Invoice()
            invoice_object.set_invoice_id(value['invoice_id'])
            invoice_object.set_customer_name(value['customer_name'])
            invoice_object.set_customer_id(value['customer_id'])
            invoice_object.set_status(value['status'])
            invoice_object.set_invoice_number(value['invoice_number'])
            invoice_object.set_reference_number(value['reference_number'])
            invoice_object.set_date(value['date'])
            invoice_object.set_due_date(value['due_date'])
            invoice_object.set_due_days(value['due_days'])
            invoice_object.set_currency_id(value['currency_id'])
            invoice_object.set_currency_code(value['currency_code'])
            invoice_object.set_total(value['total'])
            invoice_object.set_balance(value['balance'])
            invoice_object.set_created_time(value['created_time'])
            invoice_object.set_is_emailed(value['is_emailed'])
            invoice_object.set_reminders_sent(value['reminders_sent'])
            invoice_object.set_payment_expected_date(value[\
            'payment_expected_date'])
            invoice_object.set_last_payment_date(value['last_payment_date'])
            invoice_list.set_invoices(invoice_object)
        page_context_object = PageContext()
        page_context = response['page_context']
        page_context_object.set_page(page_context['page'])
        page_context_object.set_per_page(page_context['per_page'])
        page_context_object.set_has_more_page(page_context['has_more_page'])
        page_context_object.set_report_name(page_context['report_name'])
        page_context_object.set_applied_filter(page_context['applied_filter'])
        page_context_object.set_sort_column(page_context['sort_column'])
        page_context_object.set_sort_order(page_context['sort_order'])
        invoice_list.set_page_context(page_context_object)
  
        return invoice_list
     

    def get(self,response):
        """This method parses the given response and returns Invoice object.

        Args:
            response(dict): Request containing json obect for invoices.

        Returns:
            instance: Invoice object.

        """
        invoice = response['invoice']
        invoice_object = Invoice()
        invoice_object.set_invoice_id(invoice['invoice_id'])
        invoice_object.set_invoice_number(invoice['invoice_number'])
        invoice_object.set_date(invoice['date'])
        invoice_object.set_status(invoice['status'])
        invoice_object.set_payment_terms(invoice['payment_terms'])
        invoice_object.set_payment_terms_label(invoice['payment_terms_label'])
        invoice_object.set_due_date(invoice['due_date'])
        invoice_object.set_payment_expected_date(invoice[\
        'payment_expected_date'])
        invoice_object.set_last_payment_date(invoice['last_payment_date'])
        invoice_object.set_reference_number(invoice['reference_number'])
        invoice_object.set_customer_id(invoice['customer_id'])
        invoice_object.set_customer_name(invoice['customer_name'])
        invoice_object.set_contact_persons(invoice['contact_persons_details'])
        invoice_object.set_currency_id(invoice['currency_id'])
        invoice_object.set_currency_code(invoice['currency_code'])
        invoice_object.set_exchange_rate(invoice['exchange_rate'])
        invoice_object.set_discount(invoice['discount'])
        invoice_object.gst_no = invoice['gst_no']
        invoice_object.set_is_discount_before_tax(invoice[\
        'is_discount_before_tax'])
        invoice_object.set_discount_type(invoice['discount_type'])
        invoice_object.set_recurring_invoice_id(invoice[\
        'recurring_invoice_id'])
        line_items = invoice['line_items']
        for value in line_items:
            line_item = LineItem()
            line_item.set_line_item_id(value['line_item_id'])
            line_item.set_item_id(value['item_id'])
            line_item.set_project_id(value['project_id'])
            line_item.set_time_entry_ids(value['time_entry_ids'])
            line_item.set_expense_id(value['expense_id'])
            line_item.set_expense_receipt_name(value['expense_receipt_name'])
            line_item.set_name(value['name'])
            line_item.set_description(value['description'])
            line_item.set_item_order(value['item_order'])
            line_item.set_bcy_rate(value['bcy_rate'])
            line_item.set_rate(value['rate'])
            line_item.set_quantity(value['quantity'])
            line_item.set_unit(value['unit'])
            line_item.set_discount(value['discount'])
            line_item.set_tax_id(value['tax_id'])
            line_item.set_tax_name(value['tax_name'])
            line_item.set_tax_type(value['tax_type'])
            line_item.set_tax_percentage(value['tax_percentage'])
            line_item.set_hsn_or_sac(value['hsn_or_sac'])
            line_item.set_item_total(value['item_total'])
            invoice_object.set_line_items(line_item)
        invoice_object.set_shipping_charge(invoice['shipping_charge'])
        invoice_object.set_adjustment(invoice['adjustment'])
        invoice_object.set_adjustment_description(invoice[\
        'adjustment_description'])
        invoice_object.set_sub_total(invoice['sub_total'])
        invoice_object.set_tax_total(invoice['tax_total'])
        invoice_object.set_total(invoice['total'])
        taxes = invoice['taxes']
        for value in taxes:
            tax = Tax()
            tax.set_tax_name(value['tax_name'])
            tax.set_tax_amount(value['tax_amount'])
            invoice_object.set_taxes(tax)
        invoice_object.set_payment_reminder_enabled(invoice[\
        'payment_reminder_enabled'])
        invoice_object.set_payment_made(invoice['payment_made'])
        invoice_object.set_credits_applied(invoice['credits_applied'])
        invoice_object.set_tax_amount_withheld(invoice['tax_amount_withheld'])
        invoice_object.set_balance(invoice['balance'])
        invoice_object.set_write_off_amount(invoice['write_off_amount'])
        invoice_object.set_allow_partial_payments(invoice[\
        'allow_partial_payments'])
        invoice_object.set_price_precision(invoice['price_precision'])
        payment_gateways = invoice['payment_options']['payment_gateways']
        for value in payment_gateways:
            payment_gateway = PaymentGateway()
            payment_gateway.set_configured(value['configured'])
            payment_gateway.set_additional_field1(value['additional_field1'])
            payment_gateway.set_gateway_name(value['gateway_name'])
            invoice_object.set_payment_options(payment_gateway)
        invoice_object.set_is_emailed(invoice['is_emailed'])
        invoice_object.set_reminders_sent(invoice['reminders_sent'])
        invoice_object.set_last_reminder_sent_date(invoice[\
        'last_reminder_sent_date'])
        billing_address = invoice['billing_address']
        billing_address_object = Address()
        billing_address_object.set_address(billing_address['address'])
        billing_address_object.set_city(billing_address['city'])
        billing_address_object.set_state(billing_address['state'])
        billing_address_object.set_zip(billing_address['zip'])
        billing_address_object.set_country(billing_address['country'])
        billing_address_object.set_fax(billing_address['fax'])
        invoice_object.set_billing_address(billing_address_object)
     
        shipping_address = invoice['shipping_address']
        shipping_address_object = Address()
        shipping_address_object.set_address(shipping_address['address'])
        shipping_address_object.set_city(shipping_address['city'])
        shipping_address_object.set_state(shipping_address['state'])
        shipping_address_object.set_zip(shipping_address['zip'])
        shipping_address_object.set_country(shipping_address['country'])
        shipping_address_object.set_fax(shipping_address['fax'])
        invoice_object.set_shipping_address(shipping_address_object)
        invoice_object.set_notes(invoice['notes'])
        invoice_object.set_terms(invoice['terms'])
        custom_fields = invoice['custom_fields']
        for value in custom_fields:
            custom_field = CustomField() 
            custom_field.set_index(value['index'])
            custom_field.set_show_on_pdf(value['show_on_pdf'])
            custom_field.set_value(value['value'])
            custom_field.set_label(value['label'])
            invoice_object.set_custom_fields(custom_field)
        invoice_object.set_template_id(invoice['template_id'])
        invoice_object.set_template_name(invoice['template_name'])
        invoice_object.set_created_time(invoice['created_time'])
        invoice_object.set_last_modified_time(invoice['last_modified_time'])
        invoice_object.set_attachment_name(invoice['attachment_name'])
        invoice_object.set_can_send_in_mail(invoice['can_send_in_mail'])
        invoice_object.set_salesperson_id(invoice['salesperson_id'])
        invoice_object.set_salesperson_name(invoice['salesperson_name'])
  
        return invoice_object

    def get_message(self,response):
        """This message parses the given response and returns string.

        Args:
            response(dict): Request containing json object.

        Returns:
            str: Success message.
      
        """
        return response['message']
     
    def get_content(self,response): 
        """This message parses the given response and returns email object.
 
        Args:
            response(dict): Request containing json object for email content.

        Returns:
            instance: Email object.

        """
        data = response['data']
        email = Email()
        email.set_gateways_configured(data['gateways_configured'])
        email.set_deprecated_placeholders_used(data[\
        'deprecated_placeholders_used'])
        email.set_body(data['body'])
        email.set_error_list(data['error_list'])
        email.set_subject(data['subject'])
        for value in data['emailtemplates']:
            email_template = EmailTemplate()
            email_template.set_selected(value['selected'])
            email_template.set_name(value['name'])
            email_template.set_email_template_id(value['email_template_id'])
            email.set_email_templates(email_template)
        for value in data['to_contacts']:
            to_contact = ToContact()
            to_contact.set_first_name(value['first_name'])
            to_contact.set_selected(value['selected'])
            to_contact.set_phone(value['phone'])
            to_contact.set_email(value['email'])
            to_contact.set_contact_person_id(value['contact_person_id'])
            to_contact.set_last_name(value['last_name'])
            to_contact.set_salutation(value['salutation'])
            to_contact.set_mobile(value['mobile'])   
            email.set_to_contacts(to_contact)
        email.set_attachment_name(data['attachment_name'])
        email.set_file_name(data['file_name'])

        for value in data['from_emails']:
            from_email = FromEmail()
            from_email.set_user_name(value['user_name'])
            from_email.set_selected(value['selected'])
            from_email.set_email(value['email'])
            email.set_from_emails(from_email)
        email.set_customer_id(data['customer_id'])
        return email

    def payment_reminder_mail_content(self,response):
        """This method parses the given response and returns the email object.

        Args:
            response(dict): Response containing json object for email content.

        Returns:
            instance: Email object.

        """
        data = response['data']
        email = Email()
        email.set_body(data['body'])
        email.set_gateways_associated(data['gateways_associated'])
        email.set_error_list(data['error_list'])
        email.set_subject(data['subject'])
        email.set_attach_pdf(data['attach_pdf'])
        email.set_file_name(data['file_name'])
        for value in data['from_emails']:
            from_email = FromEmail()
            from_email.set_user_name(value['user_name'])
            from_email.set_selected(value['selected'])
            from_email.set_email(value['email'])
            from_email.set_is_org_email_id(value['is_org_email_id'])
            email.set_from_emails(from_email)
        email.set_file_name_without_extension(data[\
        'file_name_without_extension'])
        email.set_deprecated_placeholders_used(data[\
        'deprecated_placeholders_used'])
        email.set_gateways_configured(data['gateways_configured'])
        for value in data['to_contacts']:
            to_contact = ToContact()
            to_contact.set_first_name(value['first_name'])
            to_contact.set_selected(value['selected'])
            to_contact.set_phone(value['phone'])
            to_contact.set_email(value['email'])
            to_contact.set_last_name(value['last_name'])
            to_contact.set_salutation(value['salutation'])
            to_contact.set_contact_person_id(value['contact_person_id'])
            to_contact.set_mobile(value['mobile'])
            email.set_to_contacts(to_contact)
        email.set_attachment_name(data['attachment_name'])
        email.set_customer_id(data['customer_id'])
        return email
   
    def get_billing_address(self,response):
        """This method parses the given response and returns address object for 
            billing address.

        Args:
            response(dict): Resonse containing json object for billing address.
 
        Returns:
            instance: Address object for billing address.
 
        """
        address = response['billing_address']
        address_object = Address()
        address_object.set_address(address['address'])
        address_object.set_city(address['city'])
        address_object.set_state(address['state'])
        address_object.set_zip(address['zip'])
        address_object.set_country(address['country'])
        address_object.set_fax(address['fax'])
        address_object.set_is_update_customer(address['is_update_customer'])
        return address_object

    def get_shipping_address(self,response):
        """This method parses the given response and returns address object 
            for shipping address.
     
        Args:
            response(dict): Response containing json object for shipping 
                address.

        Returns:
            instance: Address object for shipping address.

        """ 
        address = response['shipping_address']
        address_object = Address()
        address_object.set_address(address['address'])
        address_object.set_city(address['city'])
        address_object.set_state(address['state'])
        address_object.set_zip(address['zip'])
        address_object.set_country(address['country'])
        address_object.set_fax(address['fax'])
        address_object.set_is_update_customer(address['is_update_customer'])
        return address_object

    def invoice_template_list(self,response):
        """This method parses the given response and returns list of templates 
            object.

        Args: 
            response(dict): Response containing json object for templates list.

        Returns: 
            list of instances: list of templates object.

        """
        templates = TemplateList()
        for value in response['templates']:
            template = Template()
            template.set_template_name(value['template_name'])
            template.set_template_id(value['template_id'])
            template.set_template_type(value['template_type'])
            templates.set_templates(template)
        return templates

    def payments_list(self,response):
        """This method parses the given response and returns list of invoice 
            payments.

        Args:
            response(dict): Response containing json object for invoice 
                payments list.

        Returns: 
            lsit of instances: List of invoice payments object.

        """
        payments = PaymentList()
        for value in response['payments']:
            payment = InvoicePayment()
            payment.set_payment_id(value['payment_id'])
            payment.set_payment_number(value['payment_number'])
            payment.set_invoice_id(value['invoice_id'])
            payment.set_invoice_payment_id(value['invoice_payment_id'])
            payment.set_payment_mode(value['payment_mode'])
            payment.set_description(value['description'])
            payment.set_date(value['date'])
            payment.set_reference_number(value['reference_number'])
            payment.set_exchange_rate(value['exchange_rate'])
            payment.set_amount(value['amount'])
            payment.set_tax_amount_withheld(value['tax_amount_withheld'])
            payment.set_is_single_invoice_payment(value[\
            'is_single_invoice_payment'])
            payments.set_payments(payment)
        return payments

    def credits_list(self,response):
        """This method parses the given repsonse and returns list of credits.

        Args: 
            response(dict): Response containing json object for credits.

        Returns:
            instance: Invoice credited list object.

        """
        credits = InvoiceCreditedList()
        for value in response['credits']:
            credit = InvoiceCredited()
            credit.set_creditnote_id(value['creditnote_id'])
            credit.set_creditnotes_invoice_id(value['creditnotes_invoice_id'])
            credit.set_credited_date(value['credited_date'])
            credit.set_amount_applied(value['amount_applied'])
            credits.set_invoices_credited(credit)
        return credits

    def apply_credits(self,response):
        """This method parses the given response and returns Payments and 
            credits object.

        Args:
            response(dict): Response containing json object for apply credits.

        Returns:
            instance: Payments and credits object.

        """
        use_credits = response['use_credits']
        payments_and_credits = PaymentAndCredit()
        for value in use_credits['invoice_payments']:
            invoice_payments = InvoicePayment()
            invoice_payments.set_invoice_payment_id(value[\
            'invoice_payment_id'])
            invoice_payments.set_payment_id(value['payment_id'])
            invoice_payments.set_invoice_id(value['invoice_id'])
            invoice_payments.set_amount_used(value['amount_used'])
            payments_and_credits.set_payments(invoice_payments)
        for value in use_credits['apply_creditnotes']:
            credits = InvoiceCredited()
            credits.set_creditnotes_invoice_id(value['creditnotes_invoice_id'])
            credits.set_creditnote_id(value['creditnote_id'])
            credits.set_invoice_id(value['invoice_id'])
            credits.set_amount_applied(value['amount_applied'])
            payments_and_credits.set_apply_creditnotes(credits)
        return payments_and_credits

    def comments_list(self,response):
        """This method parses the given response and returns list of comments.

        Args:
            response(dict): Response containing json object for comments list.

        Returns:
            instance: Comments list object.

        """ 
        comments = CommentList()
        for value in response['comments']:
            comment = Comment()
            comment.set_comment_id(value['comment_id'])
            comment.set_invoice_id(value['invoice_id'])
            comment.set_description(value['description'])
            comment.set_commented_by_id(value['commented_by_id'])
            comment.set_commented_by(value['commented_by'])
            comment.set_comment_type(value['comment_type'])
            comment.set_operation_type(value['operation_type'])
            comment.set_date(value['date'])
            comment.set_date_description(value['date_description'])
            comment.set_time(value['time'])
            comment.set_transaction_id(value['transaction_id'])
            comment.set_transaction_type(value['transaction_type'])
            comments.set_comments(comment)
        return comments

    def get_comment(self,response):
        """This method parses the given response and returns comments object.

        Args:
            response(dict): Response containing json object for comments.

        Returns:
            instance: Comments object.

        """
        comment = response['comment']
        comment_obj = Comment()
        comment_obj.set_comment_id(comment['comment_id'])
        comment_obj.set_invoice_id(comment['invoice_id'])
        comment_obj.set_description(comment['description'])
        comment_obj.set_commented_by_id(comment['commented_by_id'])
        comment_obj.set_commented_by(comment['commented_by'])
        comment_obj.set_date(comment['date'])
        comment_obj.set_date_description(comment['date_description'])
        comment_obj.set_time(comment['time'])
        comment_obj.set_comment_type(comment['comment_type'])
        return comment_obj 
    
     
     
      
     
        
   
