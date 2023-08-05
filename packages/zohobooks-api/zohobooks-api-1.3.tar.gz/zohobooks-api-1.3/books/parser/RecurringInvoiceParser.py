#$Id$#

from books.model.RecurringInvoice import RecurringInvoice
from books.model.RecurringInvoiceList import RecurringInvoiceList
from books.model.PageContext import PageContext
from books.model.LineItem import LineItem
from books.model.CustomField import CustomField
from books.model.Address import Address
from books.model.PaymentGateway import PaymentGateway
from books.model.Comment import Comment
from books.model.CommentList import CommentList

class RecurringInvoiceParser:
    """This class is used to parse the json for Recurring invoice."""
    def recurring_invoices(self, response):
        """This method parses the given response and creates recurring 
            invoices list object.
      
        Args:
            response(dict): Response containing json object for recurring 
                invoice list.
 
        Returns:
            instance: Recurring invoice list object.

        """
        recurring_invoices_list = RecurringInvoiceList()
        recurring_invoices = []
        for value in response['recurring_invoices']:
            recurring_invoice = RecurringInvoice()
            recurring_invoice.set_recurring_invoice_id(\
            value['recurring_invoice_id'])
            recurring_invoice.set_recurrence_name(value['recurrence_name'])
            recurring_invoice.set_status(value['status'])
            recurring_invoice.set_total(value['total'])
            recurring_invoice.set_customer_id(value['customer_id'])
            recurring_invoice.set_customer_name(value['customer_name'])
            recurring_invoice.set_start_date(value['start_date'])
            recurring_invoice.set_end_date(value['end_date'])
            recurring_invoice.set_last_sent_date(value['last_sent_date'])
            recurring_invoice.set_next_invoice_date(value['next_invoice_date'])
            recurring_invoice.set_recurrence_frequency(\
            value['recurrence_frequency'])
            recurring_invoice.set_repeat_every(value['repeat_every'])
            recurring_invoice.set_created_time(value['created_time'])
            recurring_invoice.set_last_modified_time(\
            value['last_modified_time'])
            recurring_invoices.append(recurring_invoice)
        recurring_invoices_list.set_recurring_invoices(recurring_invoices)

        page_context = response['page_context']
        page_context_obj = PageContext()
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_applied_filter(page_context['applied_filter'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        recurring_invoices_list.set_page_context(page_context_obj)

        return recurring_invoices_list

    def recurring_invoice(self, response):
        """This method parses the response and creates recurring invoice 
            object.
  
        Args:
            response(dict): Response containing json object for recurring 
                invoice.

        Returns:
            instance: Recurring invoice object.

        """
        recurring_invoice = response['recurring_invoice']
        recurring_invoice_obj = RecurringInvoice()
        recurring_invoice_obj.set_recurring_invoice_id(\
        recurring_invoice['recurring_invoice_id'])
        recurring_invoice_obj.set_recurrence_name(\
        recurring_invoice['recurrence_name'])
        recurring_invoice_obj.set_status(recurring_invoice['status'])
        recurring_invoice_obj.set_recurrence_frequency(\
        recurring_invoice['recurrence_frequency'])
        recurring_invoice_obj.set_repeat_every(\
        recurring_invoice['repeat_every'])
        recurring_invoice_obj.set_start_date(recurring_invoice['start_date'])
        recurring_invoice_obj.set_end_date(recurring_invoice['end_date'])
        recurring_invoice_obj.set_last_sent_date(\
        recurring_invoice['last_sent_date'])
        recurring_invoice_obj.set_next_invoice_date(\
        recurring_invoice['next_invoice_date'])
        recurring_invoice_obj.set_payment_terms(\
        recurring_invoice['payment_terms'])
        recurring_invoice_obj.set_payment_terms_label(\
        recurring_invoice['payment_terms_label'])
        recurring_invoice_obj.set_customer_id(recurring_invoice['customer_id'])
        recurring_invoice_obj.set_customer_name(\
        recurring_invoice['customer_name'])
        recurring_invoice_obj.set_contact_persons(\
        recurring_invoice['contact_persons'])
        recurring_invoice_obj.set_currency_id(recurring_invoice['currency_id'])
        recurring_invoice_obj.set_price_precision(\
        recurring_invoice['price_precision'])
        recurring_invoice_obj.set_currency_code(\
        recurring_invoice['currency_code'])
        recurring_invoice_obj.set_currency_symbol(\
        recurring_invoice['currency_symbol'])
        recurring_invoice_obj.set_exchange_rate(\
        recurring_invoice['exchange_rate'])
        recurring_invoice_obj.set_discount(recurring_invoice['discount'])
        recurring_invoice_obj.set_is_discount_before_tax(\
        recurring_invoice['is_discount_before_tax'])
        recurring_invoice_obj.set_discount_type(\
        recurring_invoice['discount_type'])
        line_items = []
        for value in recurring_invoice['line_items']:
            line_item = LineItem()
            line_item.set_item_id(value['item_id'])
            line_item.set_line_item_id(value['line_item_id'])
            line_item.set_name(value['name'])
            line_item.set_description(value['description'])
            line_item.set_item_order(value['item_order'])
            line_item.set_rate(value['rate'])
            line_item.set_quantity(value['quantity'])
            line_item.set_unit(value['unit'])
            line_item.set_discount_amount(value['discount_amount'])
            line_item.set_discount(value['discount'])
            line_item.set_tax_id(value['tax_id'])
            line_item.set_tax_name(value['tax_name'])
            line_item.set_tax_type(value['tax_type'])
            line_item.set_tax_percentage(value['tax_percentage'])
            line_item.set_item_total(value['item_total'])
            line_items.append(line_item)
        recurring_invoice_obj.set_line_items(line_items)
        recurring_invoice_obj.set_shipping_charge(\
        recurring_invoice['shipping_charge'])
        recurring_invoice_obj.set_adjustment(recurring_invoice['adjustment'])
        recurring_invoice_obj.set_adjustment_description(\
        recurring_invoice['adjustment_description'])
        recurring_invoice_obj.set_late_fee(recurring_invoice['late_fee'])
        recurring_invoice_obj.set_sub_total(recurring_invoice['sub_total'])
        recurring_invoice_obj.set_total(recurring_invoice['total'])
        recurring_invoice_obj.set_tax_total(recurring_invoice['tax_total'])
        recurring_invoice_obj.set_allow_partial_payments(\
        recurring_invoice['allow_partial_payments'])
        taxes = []
        for value in recurring_invoice['taxes']:
            tax = Tax()
            tax.set_tax_name(value['tax_name'])
            tax.set_tax_amount['value_tax_amount']
            taxes.append(tax)
        recurring_invoice_obj.set_taxes(taxes)
        custom_fields = []
        for value in recurring_invoice['custom_fields']:
            custom_field = CustomField()
            custom_field.set_index(value['index'])
            custom_field.set_value(value['value'])
            custom_fields.append(custom_field)
        recurring_invoice_obj.set_custom_fields(custom_fields)
        payment_gateways = recurring_invoice['payment_options'][\
                           'payment_gateways']
        for value in payment_gateways:
            payment_gateway = PaymentGateway()
            payment_gateway.set_configured(value['configured'])
            payment_gateway.set_additional_field1(value['additional_field1'])
            payment_gateway.set_gateway_name(value['gateway_name'])
            recurring_invoice_obj.set_payment_options(payment_gateway)
        billing_address = recurring_invoice['billing_address']
        billing_address_obj = Address()
        billing_address_obj.set_address(billing_address['address'])
        billing_address_obj.set_city(billing_address['city'])
        billing_address_obj.set_state(billing_address['state'])
        billing_address_obj.set_zip(billing_address['zip'])
        billing_address_obj.set_country(billing_address['country'])
        billing_address_obj.set_fax(billing_address['fax'])
        recurring_invoice_obj.set_billing_address(billing_address_obj)
        shipping_address = recurring_invoice['shipping_address']
        shipping_address_obj = Address()
        shipping_address_obj.set_address(shipping_address['address'])
        shipping_address_obj.set_city(shipping_address['city'])
        shipping_address_obj.set_state(shipping_address['state'])
        shipping_address_obj.set_zip(shipping_address['zip'])
        shipping_address_obj.set_country(shipping_address['country'])
        shipping_address_obj.set_fax(shipping_address['fax'])
        recurring_invoice_obj.set_shipping_address(shipping_address_obj)
        recurring_invoice_obj.set_template_id(recurring_invoice['template_id'])
        recurring_invoice_obj.set_template_name(\
        recurring_invoice['template_name'])
        recurring_invoice_obj.set_notes(recurring_invoice['notes'])
        recurring_invoice_obj.set_terms(recurring_invoice['terms'])
        recurring_invoice_obj.set_salesperson_id(\
        recurring_invoice['salesperson_id'])
        recurring_invoice_obj.set_salesperson_name(\
        recurring_invoice['salesperson_name'])
        recurring_invoice_obj.set_created_time(\
        recurring_invoice['created_time'])
        recurring_invoice_obj.set_last_modified_time(\
        recurring_invoice['last_modified_time'])

        return recurring_invoice_obj

    def get_message(self, response):
        """This method parses the json object and returns the message string.

        Args:
            response(dict): Response containing json object.
 
        Returns:
            string: Success message.

        """
        return response['message']

    def recurring_invoice_history_list(self, response):
        """This method parses the json object and returns list of comments 
            object.

        Args: 
            response(dict): Response containing json object.
 
        Returns:
            instance: Comments list object.

        """
        comments = CommentList()
        for value in response['comments']:
            comment = Comment()
            comment.set_comment_id(value['comment_id'])
            comment.set_recurring_invoice_id(value['recurring_invoice_id'])
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
            comments.set_comments(comment)
        return comments
  
     
