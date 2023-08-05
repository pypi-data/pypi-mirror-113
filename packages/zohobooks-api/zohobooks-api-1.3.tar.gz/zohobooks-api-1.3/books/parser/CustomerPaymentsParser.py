#$Id$#

from books.model.CustomerPayment import CustomerPayment
from books.model.CustomerPaymentList import CustomerPaymentList
from books.model.CreditNoteRefund import CreditNoteRefund
from books.model.CreditNoteRefundList import CreditNoteRefundList
from books.model.PageContext import PageContext
from books.model.Invoice import Invoice

class CustomerPaymentsParser:
    """This class is used to parse the json for customer payments."""
 
    def customer_payments(self,response):
        """This method parses the given response and returns customer payments 
            list object.

        Args:
            response(dict): Response containing json object for customer 
                payments list.
      
        Returns:
            instance: Customer payments list object.
        
        """
        customer_payment_list=CustomerPaymentList()
        for value in response['customerpayments']:
            customer_payment=CustomerPayment()
            customer_payment.set_payment_id(value['payment_id'])
            customer_payment.set_payment_number(value['payment_number'])
            customer_payment.set_invoice_numbers(value['invoice_numbers'])
            customer_payment.set_date(value['date'])
            customer_payment.set_payment_mode(value['payment_mode'])
            customer_payment.set_amount(value['amount'])
            customer_payment.set_bcy_amount(value['bcy_amount'])
            customer_payment.set_unused_amount(value['unused_amount'])
            customer_payment.set_bcy_unused_amount(value['bcy_unused_amount'])
            customer_payment.set_account_id(value['account_id'])
            customer_payment.set_account_name(value['account_name'])
            customer_payment.set_description(value['description'])
            customer_payment.set_reference_number(value['reference_number'])
            customer_payment.set_customer_id(value['customer_id'])
            customer_payment.set_customer_name(value['customer_name'])
            customer_payment.set_created_time(value['created_time'])
            customer_payment.set_last_modified_time(\
            value['last_modified_time'])
            customer_payment_list.set_customer_payments(customer_payment)
        page_context=response['page_context']
        page_context_obj=PageContext()
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_applied_filter(page_context['applied_filter'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        customer_payment_list.set_page_context(page_context_obj)
        return customer_payment_list

    def payment_refunds(self,response):
        """This method parses the given response and returns credit notes
            refund list.

        Args:
            response(dict): Repsonse containing json object for credit notes
                list.

        Returns:
            instance: Creditnote list object.

        """
        payment_refunds_list=CreditNoteRefundList()
        if 'payment_refunds' not in response:
            response['payment_refunds'] = [response['payment_refund']]
        for value in response['payment_refunds']:
            payment_refund=CreditNoteRefund()
            payment_refund.set_creditnote_refund_id(value['payment_refund_id'])
            payment_refund.set_creditnote_id(value['payment_id'])
            payment_refund.set_date(value['date'])
            payment_refund.set_refund_mode(value['refund_mode'])
            payment_refund.set_reference_number(value['reference_number'])
            payment_refund.set_description(value['description'])
            payment_refund.set_amount(value['amount'])
            payment_refunds_list.set_creditnote_refunds(payment_refund)
        if 'page_context' in response:
            page_context=response['page_context']
            page_context_obj=PageContext()
            page_context_obj.set_page(page_context['page'])
            page_context_obj.set_per_page(page_context['per_page'])
            page_context_obj.set_has_more_page(page_context['has_more_page'])
            page_context_obj.set_report_name(page_context['report_name'])
            page_context_obj.set_sort_column(page_context['sort_column'])
            page_context_obj.set_sort_order(page_context['sort_order'])
            payment_refunds_list.set_page_context(page_context_obj)
        return payment_refunds_list


    def get_customer_payment(self,response):
        """This method parses the given response and returns customer payments 
            object.

        Args: 
            response(dict): Response containing json object for customer 
                payments.
      
        Returns:
            instance: Customer payments object.
        
        """
        payment=response['payment']
        customer_payment=CustomerPayment()
        customer_payment.set_payment_id(payment['payment_id'])
        customer_payment.set_customer_id(payment['customer_id'])
        customer_payment.set_customer_name(payment['customer_name'])
        customer_payment.set_payment_mode(payment['payment_mode'])
        customer_payment.set_date(payment['date'])
        customer_payment.set_account_id(payment['account_id'])
        customer_payment.set_account_name(payment['account_name'])
        customer_payment.set_exchange_rate(payment['exchange_rate'])
        customer_payment.set_amount(payment['amount'])
        customer_payment.set_bank_charges(payment['bank_charges'])
        customer_payment.set_tax_account_id(payment['tax_account_id'])
        customer_payment.set_tax_account_name(payment['tax_account_name'])
        customer_payment.set_tax_amount_withheld(\
        payment['tax_amount_withheld'])
        customer_payment.set_description(payment['description'])
        customer_payment.set_reference_number(payment['reference_number'])
        invoices=[]
        for value in payment['invoices']:
            invoice=Invoice()
            invoice.set_invoice_number(value['invoice_number'])
            invoice.set_invoice_payment_id(value['invoice_payment_id'])
            invoice.set_invoice_id(value['invoice_id'])
            invoice.set_amount_applied(value['amount_applied'])
            invoice.set_tax_amount_withheld(value['tax_amount_withheld'])
            invoice.set_total(value['total'])
            invoice.set_balance(value['balance'])
            invoice.set_date(value['date'])
            invoice.set_due_date(value['due_date'])
            invoices.append(invoice)
        customer_payment.set_invoices(invoices) 
        return customer_payment 

    def get_message(self,response): 
        """This method parses the given response and returns the message.
        
        Args:
            response(dict): Response containing json object.
 
        Returns:
            str: Success message.

        """
        return response['message']

