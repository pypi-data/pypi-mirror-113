#$Id$

class Expense():
    """This class is used to create objecct for expenses."""
    def __init__(self):
        """Initialize parameters for Expenses object.""" 
        self.account_id = ''
        self.paid_through_account_id = ''
        self.date = ''
        self.amount = 0.0
        self.tax_id = ''
        self.is_inclusive_tax = None
        self.is_billable = None
        self.customer_id = ''
        self.vendor_id = ''
        self.currency_id = ''
        self.exchange_rate = 0.0
        self.project_id = ''
        self.expense_id = ''
        self.expense_item_id = ''
        self.account_name = ''
        self.paid_through_account_name = ''
        self.vendor_name = ''
        self.tax_name = ''
        self.tax_percentage = 0.0
        self.currency_code = ''
        self.tax_amount = 0.0
        self.sub_total = 0.0
        self.total = 0.0
        self.bcy_total = 0.0
        self.reference_number = ''
        self.description = ''
        self.customer_name = ''
        self.expense_receipt_name = ''
        self.created_time = ''
        self.last_modified_time = '' 
        self.status = ''
        self.invoice_id = ''
        self.invoice_number = ''
        self.project_name = ''
        self.recurring_expense_id = ''
        self.product_type = ''
        self.hsn_or_sac = 0
        self.gst_no = ''
        self.gst_treatment = ''
        self.destination_of_supply = ''

    def set_account_id(self, account_id):
        """Set account id.

        Args:
            account_id(str): Account id.

        """
        self.account_id = account_id

    def get_account_id(self): 
        """Get account id.

        Returns:
            str: Account id.

        """
        return self.account_id
  
    def set_paid_through_account_id(self, paid_through_account_id):
        """Set paid through account id.

        Args:
            paid_through_account_id(str): Paid through account id.

        """
        self.paid_through_account_id = paid_through_account_id

    def get_paid_through_account_id(self):
        """Get paid through account id.
 
        Returns:
            str: Paid through account id.

        """
        return self.paid_through_account_id
   
    def set_date(self, date):
        """Set date.

        Args:
            date(str): Date.

        """
        self.date = date

    def get_date(self):
        """Get date.

        Returns:
            str: Date.

        """
        return self.date
  
    def set_amount(self, amount):
        """Set amount.

        Args: 
            amount(float): Amount.

        """
        self.amount = amount

    def get_amount(self):
        """Get amount.

        Returns:
            float: Amount.

        """
        return self.amount
  
    def set_tax_id(self, tax_id):
        """Set tax id.

        Args:
            tax_id(str): Tax id.

        """
        self.tax_id = tax_id

    def get_tax_id(self):
        """Get tax id.

        Returns:
            str: Tax id.

        """
        return self.tax_id
   
    def set_is_inclusive_tax(self, is_inclusive_tax):
        """Set whether tax is inclusive.
 
        Args:
            is_inclusive_tax(bool): True if tax is inclusive else False.

        """
        self.is_inclusive_tax = is_inclusive_tax

    def get_is_inclusive_tax(self):
        """Get whether tax is inclusive.

        Returns:
            bool: True if tax is inclusive else False.

        """
        return self.is_inclusive_tax
 
    def set_is_billable(self, is_billable):
        """Set whether expenses are billable.

        Args:
            is_billable(bool): True if billable else False.

        """
        self.is_billable = is_billable

    def get_is_billable(self):
        """Get whether expenses are billable.

        Returns:
            bool: True if billable else False.

        """
        return self.is_billable

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

    def set_vendor_id(self, vendor_id):
        """Set vendor id.
 
        Args:
            vendor_id(str): Vendor id.

        """
        self.vendor_id = vendor_id
 
    def get_vendor_id(self):
        """Get vendor id.

        Returns:
            str: Vendor id.

        """
        return self.vendor_id
    
    def set_currency_id(self, currency_id):
        """Set currency id.

        Args:
            currency_id(str): Currency id.

        """
        self.currency_id = currency_id

    def get_currency_id(self):
        """Get currency idd.

        Returns:
            str: Currency id.

        """
        return self.currency_id

    def set_exchange_rate(self, exchange_rate):
        """Set exchange rate.

        Args:
            exchange_rate(float): Exchange rate.

        """
        self.exchange_rate = exchange_rate

    def get_exchange_rate(self):
        """Get exchange rate.

        Returns:
            float: Exchangge rate.

        """
        return self.exchange_rate
    
    def set_project_id(self, project_id):
        """Set project id.

        Args:
            project_id(str): Project id.

        """
        self.project_id = project_id
 
    def get_project_id(self):
        """Get project id.

        Returns:
            str: Project id.
 
        """
        return self.project_id

    def set_expense_id(self, expense_id): 
        """Set expense id.

        Args:
            expense_id(str): Expense id.

        """
        self.expense_id = expense_id

    def get_expense_id(self):
        """Get expense id.

        Returns:
            str: Expense id.

        """
        return self.expense_id
 
    def set_expense_item_id(self, expense_item_id):
        """Set expense item id.

        Args:
            expense_item_id(str): Expense item id.

        """
        self.expense_item_id = expense_item_id

    def get_expense_item_id(self):
        """Get expense item id.

        Returns:
            str: Expense item id.

        """
        return self.expense_item_id

    def set_account_name(self, account_name):
        """Set account name.

        Args:
            account_name(str): Account name.

        """
        self.account_name = account_name

    def get_account_name(self):
        """Get account name.

        Returns:
            str: Account name.

        """
        return self.account_name

    def set_paid_through_account_name(self, paid_through_account_name):
        """Set paid through account name.

        Args:
            paid_through_account_name(str): Paid through account name.

        """
        self.paid_through_account_name = paid_through_account_name

    def get_paid_through_account_name(self):
        """Get paid through account name.

        Returns:
            str: Paid through account name.

        """
        return self.paidf_through_account_name

    def set_vendor_name(self, vendor_name): 
        """Set vendor name.

        Args:
            vendor_name(str): Vendor name.

        """
        self.vendor_name = vendor_name

    def get_vendor_name(self):
        """Get vendor name.

        Returns:
            str: Vendor name.
  
        """
        return self.vendor_name

    def set_tax_name(self, tax_name):
        """Set tax name.

        Args:
            tax_name(str): Tax name.

        """
        self.tax_name = tax_name

    def get_tax_name(self):
        """Get tax name.
 
        Returns:
            str: Tax name.

        """
        return self.tax_name

    def set_tax_percentage(self, tax_percentage):
        """Set tax percentage.

        Args:
            tax_percentage(float): Tax percentage.

        """
        self.tax_percentage = tax_percentage

    def get_tax_percentage(self): 
        """Get tax percentage.

        Returns:
            float: Tax percentage.

        """
        return self.tax_percentage

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

    def set_tax_amount(self, tax_amount):
        """Set tax amount.

        Args:
            tax_amount(float): Tax amount.

        """
        self.tax_amount = tax_amount

    def get_tax_amount(self):
        """Get tax amount.

        Returns:
            float: Tax amount.

        """
        return self.tax_amount

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

    def set_total(self, total):
        """Set total.

        Args:
            total(float): Total.

        """
        self.total = total
  
    def get_total(self):
        """Get total.

        Returns:
            float: Total.

        """
        return self.total

    def set_bcy_total(self, bcy_total):
        """Set bcy total.

        Args:
            bcy_total(float): Bcy total.

        """
        self.bcy_total = bcy_total

    def get_bcy_total(self):
        """Get bcy total.

        Returns:
            float: Bcy total.

        """
        return self.bcy_total

    def set_reference_number(self, reference_number):
        """Set reference number.

        Args:
            reference_number(str): Reference number.

        """
        self.reference_number = reference_number

    def get_reference_number(self):
        """Get reference_number.

        Returns:
            str: Reference number.

        """
        return self.reference_number

    def set_description(self, description):
        """Set description.

        Args:
            description(str): Description

        """
        self.description = description

    def get_description(self): 
        """Get description.

        Returns:
            str: Description.

        """
        return self.description

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

    def set_expense_receipt_name(self, expense_receipt_name):
        """Set expense receipt name.

        Args:
            expense_receipt_name(str): Expense receipt name.

        """
        self.expense_receipt_name = expense_receipt_name

    def get_expense_receipt_name(self):
        """Get expense receipt name.

        Returns:
            str: Expense receipt name.

        """
        return self.expense_receipt_name

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
        return status

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

    def set_invoice_number(self, invoice_number): 
        """Set invoice number.

        Args:
            invoice_number(str): Invoice number.

        """
        self.invoice_number = invoice_number

    def get_invoice_number(self): 
        """Get invoice number.

        Returns:
            str: Invoice number.

        """
        return self.invoice_number

    def set_project_name(self, project_name): 
        """Set project name.

        Args:
            project_name(str): Project name.

        """
        self.project_name = project_name

    def get_project_name(self):
        """Get project name.

        Returns:
            str: Project name.

        """
        return self.project_name

    def set_recurring_expense_id(self, recurring_expense_id):
        """Set recurring expense id.

        Args:
            recurring_expense_id(str): Recurring expense id.

        """
        self.recurring_expense_id = recurring_expense_id

    def get_recurring_expense_id(self):
        """Get recurring expense id.

        Returns:
            str: Recurring expense id.

        """
        return self.recurring_expense_id

    def to_json(self):
        """This method is used to convert expense object to json object.

        Returns:
            dict: Dictionary containing json object for expenses.

        """
        data = {}
        if self.account_id != '':
            data['account_id'] = self.account_id
        if self.paid_through_account_id != '':
            data['paid_through_account_id'] = self.paid_through_account_id
        if self.date != '':
            data['date'] = self.date
        if self.amount > 0:
            data['amount'] = self.amount
        if self.tax_id != '':
            data['tax_id'] = self.tax_id
        if self.is_inclusive_tax is not None:
            data['is_inclusive_tax'] = self.is_inclusive_tax
        if self.reference_number != '':
            data['reference_number'] = self.reference_number
        if self.description != '':
            data['description'] = self.description
        if self.is_billable is not None:
            data['is_billable'] = self.is_billable
        if self.customer_id != '':
            data['customer_id'] = self.customer_id
        if self.vendor_id != '':
            data['vendor_id'] = self.vendor_id
        if self.currency_id != '':
            data['currency_id'] = self.currency_id
        if self.exchange_rate > 0:
            data['exchange_rate'] = self.exchange_rate
        if self.recurring_expense_id != '':
            data['recurring_expense_id'] = self.recurring_expense_id
        if self.project_id != '':
            data['project_id'] = self.project_id
        if self.product_type != '':
            data['product_type'] = self.product_type
        if self.hsn_or_sac != '':
            data['hsn_or_sac'] = self.hsn_or_sac
        if self.gst_no != '':
            data['gst_no'] = self.gst_no
        if self.gst_treatment != '':
            data['gst_treatment'] = self.gst_treatment
        if self.destination_of_supply != '':
            data['destination_of_supply'] = self.destination_of_supply
        return data




