#$Id$#

from books.model.Contact import Contact
from books.model.Email import Email
from books.model.Address import Address
from books.model.ContactPerson import ContactPerson
from books.model.ContactPersonList import ContactPersonList
from books.model.CustomField import CustomField
from books.model.DefaultTemplate import DefaultTemplate
from books.model.PageContext import PageContext
from books.model.ContactList import ContactList
from books.model.ToContact import ToContact
from books.model.FromEmail import FromEmail
from books.model.CommentList import CommentList
from books.model.Comment import Comment
from books.model.CreditNoteRefundList import CreditNoteRefundList
from books.model.CreditNoteRefund import CreditNoteRefund

class ContactParser:
    """This class is used to parse the json for contact."""

    def get_contact(self, resp):
        """This method parses the given response and creates a contact object.

        Args:
            resp(dict): Response containing json object for contact.

        Returns:
            instance: Contact object.
 
        """
        contact = Contact()
        response = resp['contact']
        contact.set_contact_id(response['contact_id'])
        contact.set_contact_name(response['contact_name'])
        contact.set_company_name(response['company_name'])
        contact.set_contact_salutation(response['contact_salutation'])
        contact.set_price_precision(response['price_precision'])
        contact.set_has_transaction(response['has_transaction'])
        contact.set_contact_type(response['contact_type'])
        contact.set_is_crm_customer(response['is_crm_customer'])
        contact.set_primary_contact_id(response['primary_contact_id'])
        contact.set_payment_terms(response['payment_terms'])
        contact.set_payment_terms_label(response['payment_terms_label'])
        contact.set_currency_id(response['currency_id'])
        contact.set_currency_code(response['currency_code'])
        contact.set_currency_symbol(response['currency_symbol'])
        contact.set_gst_treatment(response['gst_treatment'])
        contact.set_gst_no(response['gst_no'])
        contact.set_place_of_contact(response['place_of_contact'])
        contact.set_outstanding_receivable_amount(response[\
            'outstanding_receivable_amount'])
        contact.set_outstanding_receivable_amount_bcy(response[\
            'outstanding_receivable_amount_bcy'])
        contact.set_outstanding_payable_amount(response[\
            'outstanding_payable_amount'])
        contact.set_outstanding_payable_amount_bcy(response[\
            'outstanding_payable_amount_bcy'])
        contact.set_unused_credits_receivable_amount(response[\
            'unused_credits_receivable_amount'])
        contact.set_unused_credits_receivable_amount_bcy(response[\
            'unused_credits_receivable_amount_bcy'])
        contact.set_unused_credits_payable_amount(response[\
            'unused_credits_payable_amount'])
        contact.set_unused_credits_payable_amount_bcy(response[\
            'unused_credits_payable_amount_bcy'])
        contact.set_status(response['status'])
        contact.set_payment_reminder_enabled(response[\
            'payment_reminder_enabled'])

        for value in response['custom_fields']:
            custom_field = CustomField()
            custom_field.set_index(value['index'])
            custom_field.set_value(value['value'])
            custom_field.set_label(value['label'])
            contact.set_custom_fields(custom_field)
    
        billing_address = Address()
        billing_address.set_address(response['billing_address']['address'])
        billing_address.set_city(response['billing_address']['city'])
        billing_address.set_state(response['billing_address']['state'])
        billing_address.set_zip(response['billing_address']['zip'])
        billing_address.set_country(response['billing_address']['country'])
        billing_address.set_fax(response['billing_address']['fax'])
        contact.set_billing_address(billing_address)
    
        shipping_address = Address()
        shipping_address.set_address(response['shipping_address']['address'])
        shipping_address.set_city(response['shipping_address']['city'])
        shipping_address.set_state(response['shipping_address']['state'])
        shipping_address.set_zip(response['shipping_address']['zip'])
        shipping_address.set_country(response['shipping_address']['country'])
        shipping_address.set_fax(response['shipping_address']['fax'])
        contact.set_shipping_address(shipping_address)

        contact_persons = []
        for value in response['contact_persons']:
            contact_person = ContactPerson()
            contact_person.set_contact_person_id(value['contact_person_id'])
            contact_person.set_salutation(value['salutation'])
            contact_person.set_first_name(value['first_name'])
            contact_person.set_last_name(value['last_name'])
            contact_person.set_email(value['email'])
            contact_person.set_phone(value['phone'])
            contact_person.set_mobile(value['mobile'])
            contact_person.set_is_primary_contact(value['is_primary_contact'])
            contact_persons.append(contact_person)
        contact.set_contact_persons(contact_persons)
  
        default_templates = DefaultTemplate()
        default_templates.set_invoice_template_id(response[
            'default_templates']['invoice_template_id'])
        default_templates.set_invoice_template_name(response[\
            'default_templates']['invoice_template_name'])
        default_templates.set_estimate_template_id(response[\
            'default_templates']['estimate_template_id'])
        default_templates.set_estimate_template_name(response[\
            'default_templates']['estimate_template_name'])
        default_templates.set_creditnote_template_id(response[\
            'default_templates']['creditnote_template_id'])
        default_templates.set_creditnote_template_name(response[\
            'default_templates']['creditnote_template_name'])
        default_templates.set_invoice_email_template_id(response[\
            'default_templates']['invoice_email_template_id'])
        default_templates.set_invoice_email_template_name(response[\
            'default_templates']['invoice_email_template_name'])
        default_templates.set_estimate_email_template_id(response[\
            'default_templates']['estimate_email_template_id'])
        default_templates.set_estimate_email_template_name(response[\
            'default_templates']['estimate_email_template_name']) 
        default_templates.set_creditnote_email_template_id(response[\
            'default_templates']['creditnote_email_template_id'])
        default_templates.set_creditnote_email_template_name(response[\
            'default_templates']['creditnote_email_template_name'])
    
        contact.set_default_templates(default_templates)
        contact.set_notes(response['notes'])
        contact.set_created_time(response['created_time'])
        contact.set_last_modified_time(response['last_modified_time'])
        return contact
 
    def get_contacts(self, resp):
        """This method parses the given response and creates a contact 
            list object.
  
        Args:
            resp(dict): Response containing json object for contact list.

        Returns:
            instance: Contact list object.
 
        """
        contacts_list = ContactList()
        response = resp['contacts']
        for value in resp['contacts']:
            contact = Contact()
            contact.set_contact_id(value['contact_id'])
            contact.set_contact_name(value['contact_name'])
            contact.set_company_name(value['company_name'])
            contact.set_gst_treatment(value['gst_treatment'])
            contact.set_gst_no(value['gst_no'])
            contact.set_place_of_contact(value['place_of_contact'])
            contact.set_contact_type(value['contact_type'])
            contact.set_status(value['status'])
            contact.set_payment_terms(value['payment_terms'])
            contact.set_payment_terms_label(value['payment_terms_label'])
            contact.set_currency_id(value['currency_id'])
            contact.set_currency_code(value['currency_code'])
            contact.set_outstanding_receivable_amount(value[\
                'outstanding_receivable_amount'])
            contact.set_outstanding_payable_amount(value[\
                'outstanding_payable_amount'])
            contact.set_unused_credits_receivable_amount(value[\
                'unused_credits_receivable_amount'])
            contact.set_unused_credits_payable_amount(value[\
                'unused_credits_payable_amount'])
            contact.set_first_name(value['first_name'])
            contact.set_last_name(value['last_name'])
            contact.set_email(value['email'])
            contact.set_phone(value['phone'])
            contact.set_mobile(value['mobile'])
            contact.set_created_time(value['created_time'])
            contact.set_last_modified_time(value['last_modified_time'])
            contacts_list.set_contacts(contact)
        page_context_object = PageContext()
        page_context = resp['page_context']
        page_context_object.set_page(page_context['page'])
        page_context_object.set_per_page(page_context['per_page'])
        page_context_object.set_has_more_page(page_context['has_more_page'])
        page_context_object.set_applied_filter(page_context['applied_filter'])
        page_context_object.set_sort_column(page_context['sort_column']) 
        page_context_object.set_sort_order(page_context['sort_order']) 
    
        contacts_list.set_page_context(page_context_object)
        return contacts_list

    def get_contact_person(self, resp):
        """This method parses the given response and creates a contact person 
            object.
 
        Args:
            resp(dict): Response containing json object for contact person.

        Returns:
            instance: Contact person object.

        """
        contact_person = ContactPerson() 
        response = resp['contact_person']
        contact_person.set_contact_id(response['contact_id'])
        contact_person.set_contact_person_id(response['contact_person_id'])
        contact_person.set_salutation(response['salutation'])
        contact_person.set_first_name(response['first_name'])
        contact_person.set_last_name(response['last_name'])
        contact_person.set_email(response['email'])
        contact_person.set_phone(response['phone'])
        contact_person.set_mobile(response['mobile'])
        contact_person.set_is_primary_contact(response['is_primary_contact'])
     
        return contact_person

    def get_contact_persons(self, response):
        """This method parses the given repsonse and creates contact persons 
            list object.

        Args: 
            response(dict): Response containing json object for contact 
                                persons list.

        Returns: 
            instance: Contact person list object.

        """
        resp = response['contact_persons']
        contact_person_list = ContactPersonList()
        for value in resp:
            contact_person = ContactPerson()
            contact_person.set_contact_person_id(value['contact_person_id'])
            contact_person.set_salutation(value['salutation'])
            contact_person.set_first_name(value['first_name'])
            contact_person.set_last_name(value['last_name'])
            contact_person.set_email(value['email'])
            contact_person.set_phone(value['phone'])
            contact_person.set_mobile(value['mobile'])
            contact_person.set_is_primary_contact(value['is_primary_contact'])    
            contact_person_list.set_contact_persons(contact_person)
        page_context_object = PageContext()
        page_context = response['page_context']
        page_context_object.set_page(page_context['page'])
        page_context_object.set_per_page(page_context['per_page'])
        page_context_object.set_has_more_page(page_context['has_more_page'])
        page_context_object.set_sort_column(page_context['sort_column'])
        page_context_object.set_sort_order(page_context['sort_order'])
    
        contact_person_list.set_page_context(page_context_object)
        return contact_person_list


    def get_message(self, response):
        """This method parses the given response and returns the message.

        Args: 
            response(dict): Response containing json object.

        Returns: 
            str: Success message.

        """
        return response['message']

    def get_mail_content(self, response):
        """This method parses the give response and creates object for email.

        Args:
            response(dict): Response containing json object for email .

        Returns:
            instance: Email object.

        """   
        email = Email()
        data = response['data']
        email.set_body(data['body'])
        email.set_contact_id(data['contact_id'])
        email.set_subject(data['subject'])
        for to_contact in data['to_contacts']:
            to_contacts = ToContact()
            to_contacts.set_first_name(to_contact['first_name'])
            to_contacts.set_selected(to_contact['selected'])
            to_contacts.set_phone(to_contact['phone'])
            to_contacts.set_email(to_contact['email'])
            to_contacts.set_last_name(to_contact['last_name'])
            to_contacts.set_salutation(to_contact['salutation'])
            to_contacts.set_contact_person_id(to_contact['contact_person_id'])
            to_contacts.set_mobile(to_contact['mobile'])
            email.set_to_contacts(to_contacts)
        email.set_file_name(data['file_name'])
        for value in data['from_emails']:
            from_emails = FromEmail()
            from_emails.set_user_name(value['user_name'])
            from_emails.set_selected(value['selected'])
            from_emails.set_email(value['email'])
            from_emails.set_is_org_email_id(value['is_org_email_id'])
            email.set_from_emails(from_emails)

        return email

    def get_comment_list(self, response):
        """This method parses the given response and creates object for 
            comments list.

        Args:
            response(dict): Response containing json object for comments list.

        Returns:
            instance: cComments list object.

        """
        comment_list = CommentList()
        contact_comments = response['contact_comments']
        for value in contact_comments:
            contact_comment = Comment() 
            contact_comment.set_comment_id(value['comment_id'])
            contact_comment.set_contact_id(value['contact_id'])
            contact_comment.set_contact_name(value['contact_name'])
            contact_comment.set_description(value['description'])
            contact_comment.set_commented_by_id(value['commented_by_id'])
            contact_comment.set_commented_by(value['commented_by'])
            contact_comment.set_date(value['date'])
            contact_comment.set_date_description(value['date_description'])
            contact_comment.set_time(value['time'])
            contact_comment.set_transaction_id(value['transaction_id'])
            contact_comment.set_transaction_type(value['transaction_type'])
            contact_comment.set_is_entity_deleted(value['is_entity_deleted'])
            contact_comment.set_operation_type(value['operation_type'])
            comment_list.set_comments(contact_comment)
        page_context = response['page_context']
        page_context_object = PageContext()
        page_context_object.set_page(page_context['page'])
        page_context_object.set_per_page(page_context['per_page'])
        page_context_object.set_has_more_page(page_context['has_more_page'])
        page_context_object.set_applied_filter(page_context['applied_filter'])
        page_context_object.set_sort_column(page_context['sort_column'])
        page_context_object.set_sort_order(page_context['sort_order'])
        comment_list.set_page_context(page_context_object)
    
        return comment_list

    def get_refund_list(self, response):
        """This method parses the given response and creates refund list 
            object.

        Args:
            response(dict): Response containing json object for refund list.

        Returns:
            instance: Refund list object.

        """
        list_refund = CreditNoteRefundList()
        creditnote_refunds = response['creditnote_refunds']
        for value in creditnote_refunds:
            creditnote_refund = CreditNoteRefund()
            creditnote_refund.set_creditnote_refund_id(value[\
                'creditnote_refund_id'])
            creditnote_refund.set_creditnote_id(value['creditnote_id'])
            creditnote_refund.set_date(value['date'])
            creditnote_refund.set_refund_mode(value['refund_mode'])
            creditnote_refund.set_reference_number(value['reference_number'])
            creditnote_refund.set_creditnote_number(value['creditnote_number'])
            creditnote_refund.set_customer_name(value['customer_name'])
            creditnote_refund.set_description(value['description'])
            creditnote_refund.set_amount_bcy(value['amount_bcy'])
            creditnote_refund.set_amount_fcy(value['amount_fcy'])
            list_refund.set_creditnote_refunds(creditnote_refund)
        page_context = response['page_context']
        page_context_object = PageContext()
        page_context_object.set_page(page_context['page'])
        page_context_object.set_per_page(page_context['per_page'])
        page_context_object.set_has_more_page(page_context['has_more_page'])
        page_context_object.set_report_name(page_context['report_name'])
        page_context_object.set_sort_column(page_context['sort_column'])
        page_context_object.set_sort_order(page_context['sort_order'])    
        list_refund.set_page_context(page_context_object)

        return list_refund

  
