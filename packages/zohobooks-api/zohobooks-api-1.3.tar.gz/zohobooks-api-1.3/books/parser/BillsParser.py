#$Id$#

from books.model.Bill import Bill
from books.model.BillList import BillList
from books.model.LineItem import LineItem
from books.model.Address import Address
from books.model.Tax import Tax
from books.model.BillPayment import BillPayment
from books.model.PageContext import PageContext
from books.model.Comment import Comment
from books.model.CommentList import CommentList

class BillsParser:
    """This class is used to parse the json for Bills"""
    
    def get_list(self, resp):
        """This method parses the given response and returns  bill list object.

        Args:
            resp(dict): Response containing json object for bill list.

        Returns: 
            instance: Bill list object.

        """
        bill_list = BillList()
        for value in resp['bills']:
            bill = Bill()
            bill.set_bill_id(value['bill_id'])
            bill.set_vendor_id(value['vendor_id'])
            bill.set_vendor_name(value['vendor_name'])
            bill.set_status(value['status'])
            bill.set_bill_number(value['bill_number'])
            bill.set_reference_number(value['reference_number'])
            bill.set_date(value['date'])
            bill.set_due_date(value['due_date'])
            bill.set_due_days(value['due_days'])
            bill.set_currency_id(value['currency_id'])
            bill.set_currency_code(value['currency_code'])
            bill.set_total(value['total'])
            bill.set_balance(value['balance'])
            bill.set_created_time(value['created_time'])
            bill_list.set_bills(bill)
        page_context_obj = PageContext()
        page_context = resp['page_context']
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page']) 
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_applied_filter(page_context['applied_filter'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        bill_list.set_page_context(page_context_obj)
        return bill_list

    def get_bill(self, resp):
        """This method parses the given response and returns bills object.

        Args:
            resp(dict): Response containing json object for bill object.

        Returns:
            instance: Bill object.

        """
        bill = resp['bill']
        bill_obj = Bill()
        bill_obj.set_bill_id(bill['bill_id'])
        bill_obj.set_vendor_id(bill['vendor_id'])
        bill_obj.set_vendor_name(bill['vendor_name'])
        bill_obj.set_unused_credits_payable_amount(bill[\
        'unused_credits_payable_amount'])
        bill_obj.set_status(bill['status'])
        bill_obj.set_bill_number(bill['bill_number'])
        bill_obj.set_date(bill['date'])
        bill_obj.set_due_date(bill['due_date'])
        bill_obj.set_reference_number(bill['reference_number'])
        bill_obj.set_due_by_days(bill['due_by_days'])
        bill_obj.set_due_in_days(bill['due_in_days'])
        bill_obj.set_currency_id(bill['currency_id'])
        bill_obj.set_currency_code(bill['currency_code'])
        bill_obj.set_currency_symbol(bill['currency_symbol'])
        bill_obj.set_price_precision(bill['price_precision'])
        bill_obj.set_exchange_rate(bill['exchange_rate'])
        for value in bill['line_items']:
            line_item = LineItem()
            line_item.set_line_item_id(value['line_item_id'])
            line_item.set_account_id(value['account_id'])
            line_item.set_account_name(value['account_name'])
            line_item.set_description(value['description'])
            line_item.set_bcy_rate(value['bcy_rate'])
            line_item.set_rate(value['rate'])
            line_item.set_quantity(value['quantity'])
            line_item.set_tax_id(value['tax_id'])
            line_item.set_tax_name(value['tax_name'])
            line_item.set_tax_type(value['tax_type'])
            line_item.set_tax_percentage(value['tax_percentage'])
            line_item.set_item_total(value['item_total'])
            line_item.set_item_order(value['item_order'])
            bill_obj.set_line_items(line_item)
        bill_obj.set_sub_total(bill['sub_total'])
        bill_obj.set_tax_total(bill['tax_total'])
        bill_obj.set_total(bill['total'])
        for value in bill['taxes']:
            tax = Tax()
            tax.set_tax_name(value['tax_name'])
            tax.set_tax_amount(value['tax_amount'])
            bill_obj.set_taxes(tax)
        bill_obj.set_payment_made(bill['payment_made'])
        bill_obj.set_balance(bill['balance'])
        billing_address = bill['billing_address']
        billing_address_obj = Address()
        billing_address_obj.set_address(billing_address['address'])
        billing_address_obj.set_city(billing_address['city'])
        billing_address_obj.set_state(billing_address['state'])
        billing_address_obj.set_zip(billing_address['zip'])
        billing_address_obj.set_country(billing_address['country'])
        billing_address_obj.set_fax(billing_address['fax'])
        bill_obj.set_billing_address(billing_address_obj)
        for value in bill['payments']:
            payments = BillPayment()
            payments.set_payment_id(value['payment_id'])
            payments.set_bill_id(value['bill_id'])
            payments.set_bill_payment_id(value['bill_payment_id'])
            payments.set_payment_mode(value['payment_mode'])
            payments.set_description(value['description'])
            payments.set_date(value['date'])
            payments.set_reference_number(value['reference_number'])
            payments.set_exchange_rate(value['exchange_rate'])
            payments.set_amount(value['amount'])
            payments.set_paid_through_account_id(value[\
            'paid_through_account_id'])
            payments.set_paid_through_account_name(value[\
            'paid_through_account_name'])
            payments.set_is_single_bill_payment(value[\
            'is_single_bill_payment'])
            billing_address_obj.set_payments(payments)
        bill_obj.set_created_time(bill['created_time'])
        bill_obj.set_last_modified_time(bill['last_modified_time'])
        bill_obj.set_reference_id(bill['reference_id'])
        bill_obj.set_notes(bill['notes'])
        bill_obj.set_terms(bill['terms'])
        bill_obj.set_attachment_name(bill['attachment_name'])
        return bill_obj

    def get_message(self, resp): 
        """This method parses the given response and returns string message.

        Args:
            resp(dict): Response containing json object for success message.
 
        Returns:
            str: Success message.

        """
        return resp['message']
 
    def get_payments_list(self, resp):
        """This method parses the given response and returns payments list 
            object.

        Args:
            resp(dict): Response containing json object for payments list.

        Returns:
            list of instance: List of payments object.

        """
        payments = []
        for value in resp['payments']:
            payment = BillPayment()
            payment.set_payment_id(value['payment_id'])
            payment.set_bill_id(value['bill_id'])
            payment.set_bill_payment_id(value['bill_payment_id'])
            payment.set_vendor_id(value['vendor_id'])
            payment.set_vendor_name(value['vendor_name'])
            payment.set_payment_mode(value['payment_mode'])
            payment.set_description(value['description'])
            payment.set_date(value['date'])
            payment.set_reference_number(value['reference_number'])
            payment.set_exchange_rate(value['exchange_rate'])
            payment.set_amount(value['amount'])
            payment.set_paid_through(value['paid_through'])
            payment.set_is_single_bill_payment(value['is_single_bill_payment'])
            payments.append(payment)
        return payments

    def get_comments(self, resp):
        comments = CommentList()
        for value in resp['comments']:
            comment = Comment()
            comment.set_comment_id(value['comment_id'])
            comment.set_bill_id(value['bill_id'])
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

    def get_comment(self, resp):
        comment = resp['comment']
        comment_obj = Comment()
        comment_obj.set_comment_id(comment['comment_id'])
        comment_obj.set_bill_id(comment['bill_id'])
        comment_obj.set_description(comment['description']) 
        comment_obj.set_commented_by_id(comment['commented_by_id'])
        comment_obj.set_commented_by(comment['commented_by'])
        comment_obj.set_comment_type(comment['comment_type'])
        comment_obj.set_date(comment['date'])
        comment_obj.set_date_description(comment['date_description'])
        comment_obj.set_time(comment['time'])
        comment_obj.set_comment_type(comment['comment_type'])
        return comment_obj

