#$Id$

from books.model.Term import Term
from books.model.AddressFormat import AddressFormat

class Preference:
    """This class is used to create object for preferences."""
    def __init__(self):
        """Initialize parameters for Preferences object."""
        self.convert_to_invoice = None
        self.attach_pdf_for_email = ''
        self.estimate_approval_status = ''
        self.notify_me_on_online_payment = None
        self.send_payment_receipt_acknowledgement = None
        self.auto_notify_recurring_invoice = None
        self.snail_mail_include_payment_stub = None
        self.is_show_powered_by = None
        self.attach_expense_receipt_to_invoice = None
        self.is_estimate_enabled = None
        self.is_project_enabled = None
        self.is_purchaseorder_enabled = None
        self.is_salesorder_enabled = None
        self.is_salesorder_enabled = None
        self.is_pricebooks_enabled = None
        self.attach_payment_receipt_with_acknowledgement = None
        self.auto_reminders = []
        self.terms = Term()
        self.address_formats = AddressFormat()
        self.allow_auto_categorize = ''
   
    def set_allow_auto_categorize(self, allow_auto_categorize):
        """Set allow auto categorize.

        Args:
            allow_auto_categorize(str): Allow auto categorize.

        """
        self.allow_auto_categorize = allow_auto_categorize

    def get_allow_auto_categorize(self):
        """Get allow auto categorize.

        Returns:
            str: Allow auto categorize.

        """
        return self.allow_auto_categorize

    def set_convert_to_invoice(self, convert_to_invoice):
        """Set whether to convert to invoice.
 
        Args:
            convert_to_invoice(bool): True to Convert to invoice else False.

        """
        self.convert_to_invoice = convert_to_invoice

    def get_convert_to_invoice(self):
        """Get whether to convert to invoice.

        Returns:
            bool: True to Convert to invoice else false.
        """
        return self.convert_to_invoice

    def set_attach_pdf_for_email(self, attach_pdf_for_email):
        """Set whether to attach pdf for email.

        Args:
            attach_pdf_for_email(bool): True to attach pdf for email.

        """
        self.attach_pdf_for_email = attach_pdf_for_email

    def get_attach_pdf_for_email(self):
        """Get whether to attach pdf for email.

        Returns:
            bool: True to attach pdf for email.

        """
        return self.attach_pdf_for_email 

    def set_estimate_approval_status(self, estimate_approval_status):
        """Set estimate approval status.

        Args:
            estimate_approval_status(bool): Estimate approval status.

        """
        self.estimate_approval_status = estimate_approval_status

    def get_estimate_approval_status(self):
        """Get estimate approval status.

        Returns:
            bool: Estimate approval status.

        """
        return self.estimate_approval_status

    def set_notify_me_on_online_payment(self, notify_me_on_online_payment):
        """Set whether to notify me on online payment.

        Args:
            notify_me_on_online(bool): True to notify online payment else 
                false.

        """
        self.notify_me_on_online_payment = notify_me_on_online_payment

    def get_notify_me_on_online_payment(self):
        """Get whether to notify me on online payment.

        Returns:
            bool: True to notify online payment else False.

        """
        return self.notify_me_on_online_payment

    def set_send_payment_receipt_acknowledgement(self, \
        send_payment_receipt_acknowledgement):
        """Set whether to send payment receipt acknowledgement.

        Args:
            send_payment_receipt_acknowledgement(bool): True to send payment 
                receipt acknowledgemnt else False.

        """
        self.send_payment_receipt_acknowledgement = \
             send_payment_receipt_acknowledgement

    def get_send_payment_receipt_acknowledgement(self):
        """Get whether to send payment receipt acknowledgement.

        Returns:
            bool: True to send payment receipt acknowledgemnt else False.

        """
        return self.send_payment_receipt_acknowledgement

    def set_auto_notify_recurring_invoice(self, auto_notify_recurring_invoice):
        """Set whether to notify invoice automatically or not.

        Args:
            auto_notify_recurring_invoice(bool): True to auto notify recurring 
                invoice else false.
 
        """
        self.auto_notify_recurring_invoice = auto_notify_recurring_invoice

    def get_auto_notify_recurring_invoice(self):
        """Get whether to notify invoice automatically or not.

        Returns: 
            bool: True if auto notify is enabled else false.

        """
        return self.auto_notify_recurring_invoice

    def set_snail_mail_include_payment_stub(self, \
        snail_mail_include_payment_stub):
        """Set snail mail include payment stub.

        Args:
            snail_mail_include_payment_stub(bool): Snail mail paymanet stub.

        """
        self.snail_mail_include_payment_stub = snail_mail_include_payment_stub

    def get_snail_mail_include_payment_stub(self):
        """Get snail mail payment include stub.

        Returns: 
            bool: Snail mail payment include stub.

        """
        return self.snail_mail_include_payment_stub

    def set_is_show_powered_by(self, is_show_powered_by):
        """Set whether to show powered by.

        Args:
            is_show_powered_by(bool): True to show powered by.

        """
        self.is_show_powered_by = is_show_powered_by

    def get_is_show_powered_by(self):
        """Get whether to show powered by.

        Returns:
            bool: True to show powered by else false.

        """
        return self.is_show_powered_by
 
    def set_attach_expense_receipt_to_invoice(self, attach_receipt_to_invoice):
        """Set whether to attach receipt to invoice.

        Args:
            attach_receipt_to_invoice(bool): True to attach receipt to invoice.

        """
        self.attach_expense_receipt_to_invoice = attach_receipt_to_invoice

    def get_attach_expense_receipt_to_invoice(self):
        """Get whether to attach receipt to invoice.

        Returns:
            bool: True to attach receipt to invoice.

        """
        return self.attach_expense_receipt_to_invoice

    def set_is_estimate_enabled(self, is_estimate_enabled):
        """Set whether to enable estimate or not.

        Args:
            is_estimate_enabled(bool): True to enable estimate else False.

        """ 
        self.is_estimate_enabled = is_estimate_enabled

    def get_is_estimate_enabled(self): 
        """Get whether to enable estimate or not.

        Returns:
            bool: True to enable estimate else false.

        """
        return self.is_estimate_enabled

    def set_is_project_enabled(self, is_project_enabled):
        """Set whether to enable project or not.

        Args:
            is_project_enabled(bool): True to enable project else False.

        """
        self.is_project_enabled = is_project_enabled

    def get_is_project_enabled(self):
        """Get whether to enable project or not.

        Returns:
            bool: True to enable project else False.

        """
        return self.is_project_enabled

    def set_is_purchaseorder_enabled(self, is_purchaseorder_enabled):
        """Set whether is purchaseorder enabled.

        Args:
            is_purchaseorder_enabled(bool):True if purchase order is enabled 
                 else false.

        """
        self.is_purchaseorder_enabled = is_purchaseorder_enabled

    def get_is_purchaseorder_enabled(self):
        """Get whether is purchase order enabled.

        Returns:
            bool: True if purchase order is enabled else false.

        """
        return self.is_purchaseorder_enabled

    def set_is_salesorder_enabled(self, is_salesorder_enabled):
        """Set whether salesorder is enabled.

        Args:
            is_salesorder_enabled(bool): True if salesorder is enabled else 
                false.

        """
        self.is_salesorder_enabled = is_salesorder_enabled

    def get_is_salesorder_enabled(self):
        """Get whether salesorder is enabled.

        Returns:
            bool: True if sales order is enabled else false.

        """
        return self.is_salesorder_enabled

    def set_is_pricebooks_enabled(self, is_pricebooks_enabled):
        """Set is pricebooks enabled.

        Args:
            is_pricebooks_enabled(bool): True if pricebooks is enabled else 
                false.

        """
        self.is_pricebooks_enabled = is_pricebooks_enabled

    def get_is_pricebooks_enabled(self):
        """Get is pricebooks enabled.

        Returns:
            bool: True if price books is enabled else false.

        """
        return self.is_pricebooks_enabled

    def set_attach_payment_receipt_with_acknowledgement(self, \
        attach_payment_receipt_with_acknowledgement):
        """Set attachpayment receipt with acknowledgemnt.

        Args:
            attach_payment_receipt_with_acknowledgement(bool): True to attach 
                payment receipt with acknowledgemnt.

        """
        self.attach_payment_receipt_with_acknowledgement = \
            attach_payment_receipt_with_acknowledgement

    def get_attach_payment_receipt_with_acknowledgemnt(self):
        """Get attach payment receipt with acknowledgement.

        Returns:
            bool: True to attach payment receipt with acknowledgment.

        """
        return self.attach_payment_receipt_with_acknowledgement

    def set_auto_reminders(self, auto_reminder):
        """Set auto reminders.

        Args:
            auto_reminder(instance): Auto reminders.

        """
        self.auto_reminders.append(auto_reminder)

    def get_auto_reminders(self): 
        """Get auto reminders.

        Returns:
            list of instance: List of auto reminder object.

        """
        return self.auto_reminders

    def set_terms(self, term):
        """Set terms.

        Args:
            term(instance): Terms object.

        """
        self.terms = term

    def get_terms(self):
        """Get terms.

        Returns:
            instance: Term object.

        """
        return self.terms

    def set_address_formats(self, address_formats):
        """Set address formats.

        Args:
            address_formats(instance): Address Formats.

        """
        self.address_formats = address_formats

    def get_address_formats(self):
        """Get address formats.

        Returns:
            instance: Address formats.

        """
        return self.address_formats

    def to_json(self):
        """This method is used to convert preference object to json format.

        Returns:
            dict: Dictionary containing json object for preferences.

        """
        data = {}
        if self.convert_to_invoice is not None:
            data['convert_to_invoice'] = self.convert_to_invoice
        if self.notify_me_on_online_payment is not None:
            data['notify_me_on_online_payment'] = \
                self.notify_me_on_online_payment
        if self.send_payment_receipt_acknowledgement is not None:
            data['send_payment_receipt_acknowledgement'] = \
                self.send_payment_receipt_acknowledgement
        if self.auto_notify_recurring_invoice is not None:
            data['auto_notify_recurring_invoice'] = \
                self.auto_notify_recurring_invoice
        if self.snail_mail_include_payment_stub != None:
            data['snail_mail_include_payment_stub'] = \
                self.snail_mail_include_payment_stub
        if self.is_show_powered_by != None: 
            data['is_show_powered_by'] = self.is_show_powered_by
        if self.attach_expense_receipt_to_invoice != None:
            data['attach_expense_receipt_to_invoice'] = \
                self.attach_expense_receipt_to_invoice
        if self.is_estimate_enabled != None:
            data['is_estimate_enabled'] = self.is_estimate_enabled
        if self.is_project_enabled != None:
            data['is_project_enabled'] = self.is_project_enabled
        return data
