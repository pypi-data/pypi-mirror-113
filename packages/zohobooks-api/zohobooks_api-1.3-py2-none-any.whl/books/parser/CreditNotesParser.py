#$Id$#

from books.model.CreditNote import CreditNote
from books.model.PageContext import PageContext
from books.model.CreditNoteList import CreditNoteList
from books.model.LineItem import LineItem
from books.model.Address import Address
from books.model.EmailHistory import EmailHistory
from books.model.Email import Email
from books.model.EmailTemplate import EmailTemplate
from books.model.ToContact import ToContact
from books.model.FromEmail import FromEmail
from books.model.Template import Template
from books.model.InvoiceCredited import InvoiceCredited
from books.model.InvoiceCreditedList import InvoiceCreditedList
from books.model.Invoice import Invoice
from books.model.InvoiceList import InvoiceList
from books.model.CreditNoteRefund import CreditNoteRefund
from books.model.CreditNoteRefundList import CreditNoteRefundList
from books.model.Comment import Comment
from books.model.CommentList import CommentList

class CreditNotesParser:
    """This class is used to parse the json for credit notes."""
 
    def creditnotes_list(self,response):
        """This method parses the given response and creates a creditnotes 
            list object.

        Args:
            response(dict):Response containing json object for credit notes 
                list.

        Returns:
            instance: Creditnotes list object.

        """
        credit_notes_list=CreditNoteList()
        credit_notes=[]
        for value in response['creditnotes']:
            credit_note=CreditNote()
            credit_note.set_creditnote_id(value['creditnote_id'])
            credit_note.set_creditnote_number(value['creditnote_number'])
            credit_note.set_status(value['status'])
            credit_note.set_reference_number(value['reference_number'])
            credit_note.set_date(value['date'])
            credit_note.set_total(value['total'])
            credit_note.set_balance(value['balance'])
            credit_note.set_customer_id(value['customer_id'])
            credit_note.set_customer_name(value['customer_name'])
            credit_note.set_currency_id(value['currency_id'])
            credit_note.set_currency_code(value['currency_code'])
            credit_note.set_created_time(value['created_time'])
            credit_note.set_last_modified_time(value['last_modified_time'])
            credit_note.set_is_emailed(value['is_emailed'])
            credit_notes.append(credit_note)
        credit_notes_list.set_creditnotes(credit_notes)
        page_context_obj=PageContext()
        page_context=response['page_context']
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_applied_filter(page_context['applied_filter'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        credit_notes_list.set_page_context(page_context_obj)
        return credit_notes_list

    def get_creditnote(self,response):
        """This method parses the given response and returns credit note 
            object.

        Args:
            response(dict): Response containing json object for credit note.

        Returns:
            instance: Credit note object.

        """
        creditnote=response['creditnote']
        credit_note=CreditNote()
        credit_note.set_creditnote_id(creditnote['creditnote_id'])
        credit_note.set_creditnote_number(creditnote['creditnote_number'])
        credit_note.set_date(creditnote['date'])
        credit_note.set_status(creditnote['status'])
        credit_note.set_reference_number(creditnote['reference_number'])
        credit_note.set_customer_id(creditnote['customer_id'])
        credit_note.set_customer_name(creditnote['customer_name'])
        credit_note.set_contact_persons(creditnote['contact_persons'])
        credit_note.set_currency_id(creditnote['currency_id'])
        credit_note.set_currency_code(creditnote['currency_code'])
        credit_note.set_exchange_rate(creditnote['exchange_rate'])
        credit_note.set_price_precision(creditnote['price_precision'])
        credit_note.set_template_id(creditnote['template_id'])
        credit_note.set_template_name(creditnote['template_name'])
        credit_note.set_is_emailed(creditnote['is_emailed'])
        for value in creditnote['line_items']:
            line_item=LineItem()
            line_item.set_item_id(value['item_id'])
            line_item.set_line_item_id(value['line_item_id'])
            line_item.set_account_id(value['account_id'])
            line_item.set_account_name(value['account_name'])
            line_item.set_name(value['name'])
            line_item.set_description(value['description'])
            line_item.set_item_order(value['item_order'])
            line_item.set_quantity(value['quantity'])
            line_item.set_unit(value['unit'])
            line_item.set_bcy_rate(value['bcy_rate'])
            line_item.set_rate(value['rate'])
            line_item.set_tax_id(value['tax_id'])
            line_item.set_tax_name(value['tax_name'])
            line_item.set_tax_type(value['tax_type'])
            line_item.set_tax_percentage(value['tax_percentage'])
            line_item.set_item_total(value['item_total'])
            credit_note.set_line_items(line_item)
        credit_note.set_sub_total(creditnote['sub_total'])
        credit_note.set_total(creditnote['total'])
        credit_note.set_total_credits_used(creditnote['total_credits_used'])   
        credit_note.set_total_refunded_amount(\
        creditnote['total_refunded_amount'])
        credit_note.set_balance(creditnote['balance'])
        taxes=[]
        for value in creditnote['taxes']:
            tax=Tax()
            tax.set_tax_name(value['tax_name'])
            tax.set_tax_amount(value['tax_amount'])
            taxes.append(tax)
        credit_note.set_taxes(taxes)
        billing_address=creditnote['billing_address']
        billing_address_obj=Address()
        billing_address_obj.set_address(billing_address['address'])
        billing_address_obj.set_city(billing_address['city'])
        billing_address_obj.set_state(billing_address['state'])
        billing_address_obj.set_zip(billing_address['zip'])
        billing_address_obj.set_country(billing_address['country'])
        billing_address_obj.set_fax(billing_address['fax'])
        credit_note.set_billing_address(billing_address_obj)
        shipping_address=creditnote['shipping_address']
        shipping_address_obj=Address()
        shipping_address_obj.set_address(shipping_address['address'])
        shipping_address_obj.set_city(shipping_address['city'])
        shipping_address_obj.set_state(shipping_address['state'])
        shipping_address_obj.set_zip(shipping_address['zip'])
        shipping_address_obj.set_country(shipping_address['country'])
        shipping_address_obj.set_fax(shipping_address['fax'])
        credit_note.set_shipping_address(shipping_address_obj)
        credit_note.set_created_time(creditnote['created_time'])
        credit_note.set_last_modified_time(creditnote['last_modified_time'])
        return credit_note

    def get_message(self,response):
        """This method parses the json object and returns string message.

        Args:
            response(dict): Response containing json object.

        Returns:
            str: Success message.

        """
        return response['message']
 
    def email_history(self,response):
        """This method parses the json object and returns list of email \
            history object.

        Args:
            response(dict): Response containing json object for email history.

        Returns:
            list of instance: List of email history object.
  
        """
        email_history=[]
        for value in response['email_history']:
            email_history_obj=EmailHistory()
            email_history_obj.set_mailhistory_id(value['mailhistory_id'])
            email_history_obj.set_from(value['from'])
            email_history_obj.set_to_mail_ids(value['to_mail_ids'])
            email_history_obj.set_subject(value['subject'])
            email_history_obj.set_date(value['date'])
            email_history_obj.set_type(value['type'])
            email_history.append(email_history_obj)
        return email_history
 
    def email(self,response):
        """This method parses the response and returns email object.

        Args:
            response(dict):  Response containing json object for email.

        Returns:
            instance: Email object.

        """
        data=response['data']
        email=Email()
        email.set_body(data['body'])
        email.set_error_list(data['error_list'])
        email.set_subject(data['subject'])
        for value in data['emailtemplates']:
            email_template=EmailTemplate()
            email_template.set_selected(value['selected'])
            email_template.set_name(value['name'])
            email_template.set_email_template_id(value['email_template_id'])
            email.set_email_templates(email)
        for value in data['to_contacts']:
            to_contact=ToContact()
            to_contact.set_first_name(value['first_name'])
            to_contact.set_selected(value['selected'])
            to_contact.set_phone(value['phone'])
            to_contact.set_email(value['email'])
            to_contact.set_last_name(value['last_name'])
            to_contact.set_salutation(value['salutation'])
            to_contact.set_contact_person_id(value['contact_person_id'])
            to_contact.set_mobile(value['mobile'])
            email.set_to_contacts(to_contact)
        email.set_file_name(data['file_name'])
        email.set_file_name_without_extension(\
        data['file_name_without_extension'])
        for value in data['from_emails']:
            from_email=FromEmail()
            from_email.set_user_name(value['user_name'])
            from_email.set_selected(value['selected'])
            from_email.set_email(value['email'])
            from_email.set_is_org_email_id(value['is_org_email_id']) 
        email.set_from_emails(from_email)
        email.set_customer_id(data['customer_id'])
        return email

    def get_billing_address(self,response): 
        """This method parses the response containing json object for billing 
            address.

        Args:
            response(dict): Response containing json object for billing address.

        Returns:
            instance: Address object.

        """
        billing_address=response['billing_address']
        billing_address_obj=Address()
        billing_address_obj.set_address(billing_address['address'])
        billing_address_obj.set_city(billing_address['city'])
        billing_address_obj.set_state(billing_address['state'])
        billing_address_obj.set_zip(billing_address['zip'])
        billing_address_obj.set_country(billing_address['country'])
        billing_address_obj.set_fax(billing_address['fax'])
        billing_address_obj.set_is_update_customer(\
        billing_address['is_update_customer'])
        return billing_address_obj

    def get_shipping_address(self,response):
        """This method parses the json object and returns shipping address \
            object.

        Args:
            response(dict): Response containing json object for shipping \
                address.

        Returns:
            instance: Shipping address object.

        """
        shipping_address=response['shipping_address']
        shipping_address_obj=Address()
        shipping_address_obj.set_address(shipping_address['address'])    
        shipping_address_obj.set_city(shipping_address['city'])
        shipping_address_obj.set_state(shipping_address['state'])
        shipping_address_obj.set_zip(shipping_address['zip'])
        shipping_address_obj.set_country(shipping_address['country'])
        shipping_address_obj.set_fax(shipping_address['fax'])
        shipping_address_obj.set_is_update_customer(\
        shipping_address['is_update_customer'])
        return shipping_address_obj
 
    def list_templates(self,response):
        """This method parses the json object and returns templates list.

        Args:
            response(dict): Response containing json object for templates list.

        Returns:
            lsit of instance: Lsit of templates object.

        """
        templates=[]
        for value in response['templates']:
            template=Template()
            template.set_template_name(value['template_name'])
            template.set_template_id(value['template_id'])
            template.set_template_type(value['template_type'])
            templates.append(template)
        return templates

    def list_invoices_credited(self,response):
        """This method parses the json object and returns list of invoices 
            credited.

        Args:
            response(dict): Response containing json object for invoices 
                credited.

        Returns:
            instance: Invoices credited list object.

        """
        invoices_credited = InvoiceCreditedList()
        for value in response['invoices_credited']:
            invoice_credited = InvoiceCredited()
            invoice_credited.set_creditnote_id(value['creditnote_id'])
            invoice_credited.set_invoice_id(value['invoice_id'])
            invoice_credited.set_creditnotes_invoice_id(\
            value['creditnote_invoice_id'])
            invoice_credited.set_date(value['date'])
            invoice_credited.set_invoice_number(value['invoice_number'])
            invoice_credited.set_creditnotes_number(value['creditnote_number'])
            invoice_credited.set_credited_amount(value['credited_amount'])
            invoices_credited.set_invoices_credited(invoice_credited)
        return invoices_credited

    def credit_to_invoice(self,response):
        """This method parses the given response and returns invoices object.
 
        Args:
            response(dict): Responses containing json object for credit to 
                invoice.

        Returns:
            instance: Invoice List object.

        """
        invoices = InvoiceList()
        for value in response['apply_to_invoices']['invoices']:
            invoice=Invoice()
            invoice.set_invoice_id(value['invoice_id'])
            invoice.set_amount_applied(value['amount_applied'])
            invoices.set_invoices(invoice)
        return invoices

    def creditnote_refunds(self,response):
        """This method parses the given response and returns credit notes 
            refund list.

        Args:
            response(dict): Repsonse containing json object for credit notes 
                list.

        Returns:
            instance: Creditnote list object.

        """
        creditnotes_refund_list=CreditNoteRefundList()
        for value in response['creditnote_refunds']:
            creditnotes_refund=CreditNoteRefund()
            creditnotes_refund.set_creditnote_refund_id(\
            value['creditnote_refund_id'])
            creditnotes_refund.set_creditnote_id(value['creditnote_id'])   
            creditnotes_refund.set_date(value['date'])
            creditnotes_refund.set_refund_mode(value['refund_mode'])
            creditnotes_refund.set_reference_number(value['reference_number'])
            creditnotes_refund.set_creditnote_number(\
            value['creditnote_number'])
            creditnotes_refund.set_customer_name(value['customer_name'])
            creditnotes_refund.set_description(value['description'])
            creditnotes_refund.set_amount_bcy(value['amount_bcy'])
            creditnotes_refund.set_amount_fcy(value['amount_fcy'])
            creditnotes_refund_list.set_creditnote_refunds(creditnotes_refund)
        page_context=response['page_context']
        page_context_obj=PageContext()
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        creditnotes_refund_list.set_page_context(page_context_obj)
        return creditnotes_refund_list

    def get_creditnote_refund(self,response):
        """This method parses the given repsonse and returns credit note 
            refund object.

        Args:
            response(dict): Response containing json object for credit note 
                refund.

        Returns:
            isntacne: Credit note object.

        """
        creditnote_refund=response['creditnote_refund']
        creditnote_refund_obj=CreditNoteRefund()
        creditnote_refund_obj.set_creditnote_refund_id(\
        creditnote_refund['creditnote_refund_id'])
        creditnote_refund_obj.set_creditnote_id(\
        creditnote_refund['creditnote_id'])
        creditnote_refund_obj.set_date(creditnote_refund['date'])
        creditnote_refund_obj.set_refund_mode(creditnote_refund['refund_mode'])
        creditnote_refund_obj.set_reference_number(\
        creditnote_refund['reference_number'])
        creditnote_refund_obj.set_amount(creditnote_refund['amount'])
        creditnote_refund_obj.set_exchange_rate(\
        creditnote_refund['exchange_rate'])
        creditnote_refund_obj.set_from_account_id(\
        creditnote_refund['from_account_id'])
        creditnote_refund_obj.set_from_account_name(\
        creditnote_refund['from_account_name'])
        creditnote_refund_obj.set_description(creditnote_refund['description'])
        return creditnote_refund_obj

    def comments_list(self,response):
        """This method parses the given response and returns the comments list.

        Args:
            response(dict): Response containing json object for comments list.
 
        Returns:
            list of instance: List of comments object.

        """ 
        comments_list = CommentList()
        for value in response['comments']:
            comment = Comment() 
            comment.set_comment_id(value['comment_id'])
            comment.set_creditnote_id(value['creditnote_id'])
            comment.set_description(value['description'])
            comment.set_commented_by_id(value['commented_by_id'])
            comment.set_commented_by(value['commented_by'])
            comment.set_comment_type(value['comment_type'])
            comment.set_date(value['date'])
            comment.set_date_description(value['date_description'])
            comment.set_time(value['time'])
            comment.set_operation_type(value['operation_type'])
            comment.set_transaction_id(value['transaction_id'])
            comment.set_transaction_type(value['transaction_type'])
            comments_list.set_comments(comment)
        return comments_list

    def get_comment(self,response):
        """This method parses the given response and returns comments object.

        Args:
            response(dict): Response containing json object for comments.

        Returns:
            instance: Comments object.

        """
        comment=response['comment']
        comment_obj=Comment()
        comment_obj.set_comment_id(comment['comment_id'])
        comment_obj.set_creditnote_id(comment['creditnote_id'])
        comment_obj.set_description(comment['description'])
        comment_obj.set_commented_by_id(comment['commented_by_id'])
        comment_obj.set_commented_by(comment['commented_by'])
        comment_obj.set_date(comment['date'])
        return comment_obj
     
      





















          
