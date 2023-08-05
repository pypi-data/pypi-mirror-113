#$Id$#

from books.model.Estimate import Estimate
from books.model.EstimateList import EstimateList
from books.model.Address import Address
from books.model.Email import Email
from books.model.ContactPerson import ContactPerson
from books.model.LineItem import LineItem
from books.model.PageContext import PageContext
from books.model.Tax import Tax
from books.model.CustomField import CustomField
from books.model.Email import Email
from books.model.EmailTemplate import EmailTemplate
from books.model.ToContact import ToContact
from books.model.FromEmail import FromEmail
from books.model.Template import Template
from books.model.Comment import Comment
from books.model.CommentList import CommentList
from books.model.TemplateList import TemplateList

class EstimatesParser:
    """This class is used to parse the json for estimates."""

    def get_list(self, response):
        """This method parses the given response and returns estimates list 
            object.
  
        Args:
            response(dict): Response containing json object for estimates.

        Returns:
            instance: Estimates list object.

        """
        resp = response['estimates']
        estimate_list = EstimateList()
        for value in resp:
            estimates = Estimate()
            estimates.set_estimate_id(value['estimate_id'])
            estimates.set_customer_name(value['customer_name'])
            estimates.set_customer_id(value['customer_id'])
            estimates.set_status(value['status'])
            estimates.set_estimate_number(value['estimate_number'])
            estimates.set_reference_number(value['reference_number'])
            estimates.set_date(value['date'])
            estimates.set_currency_id(value['currency_id'])
            estimates.set_currency_code(value['currency_code'])
            estimates.set_total(value['total'])
            estimates.set_created_time(value['created_time'])
            estimates.set_accepted_date(value['accepted_date'])
            estimates.set_declined_date(value['declined_date'])
            estimates.set_expiry_date(value['expiry_date'])
            estimate_list.set_estimates(estimates)
        page_context_object = PageContext()
        page_context = response['page_context']
        page_context_object.set_page(page_context['page'])
        page_context_object.set_per_page(page_context['per_page'])
        page_context_object.set_has_more_page(page_context['has_more_page'])
        page_context_object.set_report_name(page_context['report_name'])
        page_context_object.set_applied_filter(page_context['applied_filter'])
        page_context_object.set_sort_column(page_context['sort_column'])
        page_context_object.set_sort_order(page_context['sort_order'])
        estimate_list.set_page_context(page_context_object)
        return estimate_list


    def get_estimate(self, response):
        """This method parses the given response and returns Estimate object.

        Args:
            response(dict): Response containing json object for estimate.

        Returns:
            instance: Estimate object.

        """
        estimate = Estimate()
        resp = response['estimate']
        estimate.set_estimate_id(resp['estimate_id'])
        estimate.set_estimate_number(resp['estimate_number'])
        estimate.set_date(resp['date'])
        estimate.set_reference_number(resp['reference_number'])
        estimate.set_status(resp['status'])
        estimate.set_customer_id(resp['customer_id'])
        estimate.set_customer_name(resp['customer_name'])
        estimate.set_contact_persons(resp['contact_persons'])
        estimate.set_currency_id(resp['currency_id'])
        estimate.set_currency_code(resp['currency_code'])
        estimate.set_exchange_rate(resp['exchange_rate'])
        estimate.set_expiry_date(resp['expiry_date'])
        estimate.set_discount(resp['discount'])
        estimate.set_is_discount_before_tax(resp['is_discount_before_tax'])
        estimate.set_discount_type(resp['discount_type'])
        line_items = resp['line_items']
        for value in line_items:
            line_item = LineItem()
            line_item.set_item_id(value['item_id'])
            line_item.set_line_item_id(value['line_item_id'])
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
            line_item.set_item_total(value['item_total'])
            estimate.set_line_items(line_item)
        estimate.set_shipping_charge(resp['shipping_charge'])
        estimate.set_adjustment(resp['adjustment'])
        estimate.set_adjustment_description(resp['adjustment_description'])
        estimate.set_sub_total(resp['sub_total'])
        estimate.set_total(resp['total'])
        estimate.set_tax_total(resp['tax_total'])
        estimate.set_price_precision(resp['price_precision'])
        taxes = resp['taxes']
        for value in taxes:
            tax = Tax()
            tax.set_tax_name(value['tax_name'])
            tax.set_tax_amount(value['tax_amount'])
            estimate.set_taxes(tax)
        billing_address = resp['billing_address']
        billing_address_object = Address()
        billing_address_object.set_address(billing_address['address'])
        billing_address_object.set_city(billing_address['city'])
        billing_address_object.set_state(billing_address['state'])
        billing_address_object.set_zip(billing_address['zip']) 
        billing_address_object.set_country(billing_address['country'])   
        billing_address_object.set_fax(billing_address['zip'])
        estimate.set_billing_address(billing_address_object)

        shipping_address = resp['shipping_address']
        shipping_address_object = Address()
        shipping_address_object.set_address(shipping_address['address'])
        shipping_address_object.set_city(shipping_address['city'])
        shipping_address_object.set_state(shipping_address['state'])
        shipping_address_object.set_zip(shipping_address['zip']) 
        shipping_address_object.set_country(shipping_address['country'])   
        shipping_address_object.set_fax(shipping_address['zip'])
        estimate.set_shipping_address(shipping_address_object)

        estimate.set_notes(resp['notes'])
        estimate.set_terms(resp['terms'])
        custom_fields = resp['custom_fields']
        for value in custom_fields:
            custom_field = CustomField()
            custom_field.set_index(value['index'])
            custom_field.set_show_on_pdf(value['show_on_pdf'])
            custom_field.set_value(value['value'])
            custom_field.set_label(value['label'])
            estimate.set_custom_fields(custom_field)
        estimate.set_template_id(resp['template_id'])
        estimate.set_template_name(resp['template_name'])
        estimate.set_created_time(resp['created_time'])
        estimate.set_last_modified_time(resp['last_modified_time'])
        estimate.set_salesperson_id(resp['salesperson_id'])
        estimate.set_salesperson_name(resp['salesperson_name'])
        return estimate

    def get_message(self, response):
        """This method parses the given response and returns success message.

        Args:
            response(dict): Response containing json object.

        Returns:
            str: Success message.

        """
        return response['message']

    def get_email_content(self, response):
        """This method parses the given response and returns email object.

        Args:
            response(dict): Response containing json object for email content.

        Returns:
            instance: Email object.

        """
        email = Email()
        data = response['data']
        email.set_body(data['body'])
        email.set_error_list(data['error_list'])
        email.set_subject(data['subject'])
        for value in data['emailtemplates']:
            email_templates = EmailTemplate()
            email_templates.set_selected(value['selected'])
            email_templates.set_name(value['name'])
            email_templates.set_email_template_id(value['email_template_id'])
            email.set_email_templates(email_templates)
        to_contacts = data['to_contacts']
        for value in to_contacts:
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
        email.set_file_name(data['file_name'])
        from_emails = data['from_emails']
        for value in from_emails:
            from_email = FromEmail()
            from_email.set_user_name(value['user_name'])
            from_email.set_selected(value['selected'])
            from_email.set_email(value['email'])
            email.set_from_emails(from_email)
        email.set_customer_id(data['customer_id'])
        return email

    def get_billing_address(self, response):
        """This method parses the given response and returns billing address object.

        Args:
            response(dict): Response containing json object for billing address.

        Returns:
            instacne: Billing address object.

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

    def get_shipping_address(self, response):
        """This method parses the given response and returns shipping address 
            object.

        Args:
            response(dict): Response containing json object for shipping 
                address.
 
        Returns:
            instance: Shipping address object.

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

    def estimate_template_list(self, response):
        """This method parses the given response and returns estimate template 
            list object.

        Args:
            response(dict): Response containing json object for estimate 
                template list.


        Returns:
            instance: Template list object.

        """
        template_list = TemplateList()
        resp = response['templates']
        for value in resp:
            template = Template()
            template.set_template_name(value['template_name'])
            template.set_template_id(value['template_id'])
            template.set_template_type(value['template_type'])
            template_list.set_templates(template)
        return template_list
      
    def get_comments(self, response):
        """This method parses the given response and returns comments list 
            object.
 
        Args:
            response(dict): Response containing json object for comments list.

        Returns:
            instance: Comments list object.

        """        
        comments = response['comments']
        comments_list = CommentList()
        for value in comments:
            comment = Comment()
            comment.set_comment_id(value['comment_id'])
            comment.set_estimate_id(value['estimate_id'])
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

    def get_comment(self, response):
        """This method parses the given response and returns comments object.

        Args:
            response(dict): Response containing json object for comments 
                object.

        Returns:
            instance: Comments object.

        """
        comment = response['comment']
        comment_object = Comment()
        comment_object.set_comment_id(comment['comment_id'])
        comment_object.set_estimate_id(comment['estimate_id'])
        comment_object.set_description(comment['description'])
        comment_object.set_commented_by_id(comment['commented_by_id'])
        comment_object.set_commented_by(comment['commented_by'])
        comment_object.set_date(comment['date'])
        comment_object.set_date_description(comment['date_description'])
        comment_object.set_time(comment['time'])
        comment_object.set_comment_type(comment['comment_type'])
        return comment_object


