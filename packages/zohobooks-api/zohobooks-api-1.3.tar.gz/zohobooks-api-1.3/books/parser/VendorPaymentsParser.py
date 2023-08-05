#$Id$#

from books.model.VendorPayment import VendorPayment
from books.model.VendorPaymentList import VendorPaymentList
from books.model.Bill import Bill

class VendorPaymentsParser:
    """This class is used to parse the json response for Vendor payments."""

    def get_list(self, resp):
        """This method parses the given response and returns vendor payments 
            list object.

        Args:
            resp(dict): Dictionary containing json object for vendor payments 
                list.

        Returns:
            instance: Vendor payments list object.

        """
        vendor_payments_list = VendorPaymentList()
        for value in resp['vendorpayments']:
            vendor_payment = VendorPayment()
            vendor_payment.set_payment_id(value['payment_id'])
            vendor_payment.set_vendor_id(value['vendor_id'])
            vendor_payment.set_vendor_name(value['vendor_name'])
            vendor_payment.set_payment_mode(value['payment_mode'])
            vendor_payment.set_description(value['description'])
            vendor_payment.set_date(value['date'])
            vendor_payment.set_reference_number(value['reference_number'])
            vendor_payment.set_exchange_rate(value['exchange_rate'])
            vendor_payment.set_amount(value['amount'])
            vendor_payment.set_paid_through_account_id(value[\
            'paid_through_account_id'])
            vendor_payment.set_paid_through_account_name(value[\
            'paid_through_account_name'])
            vendor_payment.set_balance(value['balance'])
            vendor_payments_list.set_vendor_payments(vendor_payment)
        return vendor_payments_list

    def get_vendor_payment(self, resp):
        """This method is used to parse the given response and returns vendor 
            payments object.

        Args: 
            resp(dict): Dictionary containing json object for vendor payments.

        Returns:
            instance: Vendor payments object.

        """
        vendor_payment_obj = VendorPayment()
        vendor_payment = resp['vendorpayment']
        vendor_payment_obj.set_payment_id(vendor_payment['payment_id'])
        vendor_payment_obj.set_vendor_id(vendor_payment['vendor_id'])
        vendor_payment_obj.set_vendor_name(vendor_payment['vendor_name'])
        vendor_payment_obj.set_payment_mode(vendor_payment['payment_mode'])
        vendor_payment_obj.set_description(vendor_payment['description'])
        vendor_payment_obj.set_date(vendor_payment['date'])
        vendor_payment_obj.set_reference_number(vendor_payment[\
        'reference_number'])
        vendor_payment_obj.set_exchange_rate(vendor_payment['exchange_rate'])
        vendor_payment_obj.set_amount(vendor_payment['amount'])
        vendor_payment_obj.set_currency_symbol(vendor_payment[\
        'currency_symbol'])
        vendor_payment_obj.set_paid_through_account_id(vendor_payment[\
        'paid_through_account_id'])
        vendor_payment_obj.set_paid_through_account_name(vendor_payment[\
        'paid_through_account_name'])
        for value in vendor_payment['bills']:
            bill = Bill()
            bill.set_bill_number(value['bill_number'])
            bill.set_bill_payment_id(value['bill_payment_id'])
            bill.set_bill_id(value['bill_id'])
            bill.set_total(value['total'])
            bill.set_balance(value['balance'])
            bill.set_amount_applied(value['amount_applied'])
            bill.set_date(value['date'])
            bill.set_due_date(value['due_date'])
            vendor_payment_obj.set_bills(bill)
        return vendor_payment_obj

    def get_message(self, resp):
        """This message parses the given response and returns message string.
    
        Args:
            resp(dict): Response containing json object for message.

        Returns:
            str: Success message.

        """
        return resp['message']
       
