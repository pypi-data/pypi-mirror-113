#$Id$

class RecurringExpense:
    """This class is used to create object for Recurring Expenses."""
    def __init__(self):
        """Initialize parameters for Recurring expenses."""
        self.account_id = ''
        self.paid_through_account_id = ''
        self.recurrence_name = ''
        self.start_date = ''
        self.end_date = ''
        self.recurrence_frequency = ''
        self.repeat_every = 0
        self.repeat_frequency = ''
        self.amount = 0.0
        self.tax_id = ''
        self.is_inclusive_tax = None
        self.is_billable = None
        self.customer_id = ''
        self.vendor_id = ''
        self.project_id = ''
        self.currency_id = ''
        self.exchange_rate = 0.0
        self.recurring_expense_id = ''
        self.last_created_date = ''
        self.next_expense_date = ''
        self.account_name = ''
        self.paid_through_account_name = ''
        self.vendor_name = ''
        self.currency_code = ''
        self.tax_name = ''
        self.tax_percentage = 0
        self.tax_amount = 0.0
        self.sub_total = 0.0
        self.total = 0.0
        self.bcy_total = 0.0
        self.description = ''
        self.customer_name = ''
        self.status = ''
        self.created_time = ''
        self.last_modified_time = ''
        self.project_name = ''
  
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

    def set_recurrence_name(self, recurrence_name):
        """Set recurrence name.

        Args:
            recurrence_name(str): Recurrence name.

        """
        self.recurrence_name = recurrence_name

    def get_recurrence_name(self):
        """Get recurrence name.

        Returns: 
            str: Recurrence name.

        """
        return self.recurrence_name

    def set_start_date(self, start_date):
        """Set start date.

        Args:
            start_date(str): Start date.

        """
        self.start_date = start_date

    def get_start_date(self):
        """Get start date.

        Returns:
            str: Start date.

        """
        return self.start_date
  
    def set_end_date(self, end_date):
        """Set end date.

        Args:
            end_date(str): End date.

        """
        self.end_date = end_date

    def get_end_date(self):
        """Get end date.

        Returns:
            str: End date.

        """
        return self.end_date
  
    def set_recurrence_frequency(self, recurrence_frequency):
        """Set recurrence frequency.

        Args:
            recurrence_frequency(str): Recurrence frequency.

        """
        self.recurrence_frequency = recurrence_frequency

    def get_recurrence_frequency(self):
        """Get recurrence frequency.

        Returns:
            str: Recurrence frequency.

        """
        return self.recurrence_frequency
  
    def set_repeat_every(self, repeat_every):
        """Set repeat every.
    
        Args:
            repeat_every(int): Repeat every.

        """
        self.repeat_every = repeat_every

    def get_repeat_every(self):
        """Get repeat every.

        Returns:
            int: Repeat every.
 
        """
        return self.repeat_every
 
    def set_repeat_frequency(self, repeat_frequency):
        """Set repeat frequency.
 
        Args:
            repeat_frequency(str): Repeat frequency.

        """
        self.repeat_frequency = repeat_frequency

    def get_repeat_frequency(self):
        """Get repeat frequency.

        Returns:
            str: Repeat frequency.

        """
        return self.repeat_frequency
 
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
        """Set whether Recurring Expense is billable.

        Args:
            is_billable(bool): True if billable else False.

        """ 
        self.is_billable = is_billable
    
    def get_is_billable(self):
        """Get whether Recurring Expense is billable.

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
            str: Get vendor id.

        """
        return self.vendor_id

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
  
    def set_currency_id(self, currency_id):
        """Set currency id.

        Args:
            currency_id(str): Currency id.

        """
        self.currency_id = currency_id
 
    def get_currency_id(self):
        """Get currency id.

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
            float: Exchange rate.

        """
        return self.exchange_rate
  
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

    def set_last_created_date(self, last_created_date):
        """Set last created date.

        Args:
            last_created_date(str): Last created date.

        """
        self.last_created_date = last_created_date

    def get_last_created_date(self): 
        """Get last created date.

        Returns:
            str: Last created date.

        """
        return self.last_created_date

    def set_next_expense_date(self, next_expense_date): 
        """Set next expense date.

        Args:
            next_expense_date(str): Next expense date.

        """
        self.next_expense_date = next_expense_date

    def get_next_expense_date(self): 
        """Get next expense date.

        Returns:
            str: Next expense date.

        """
        return self.next_expense_date

    def set_account_name(self, account_name):
        """Set account name.

        Args:
            account_name(str): Account name.

        """
        self.account_name = account_name

    def get_account_name(self): 
        """Get account name.

        Return:
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
        return self.paid_through_account_name

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
            tax_percentage(int): Tax percentage.

        """
        self.tax_percentage = tax_percentage

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

    def set_description(self, description):
        """Set description.

        Args:
            description(str): Description.

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

    def set_status(self, status): 
        """Set status.
 
        Args:
            status(str): Status.

        """
        self.status = ''
 
    def get_status(self):
        """Get status.

        Returns:
            str: Status.

        """
        return self.status

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

    def to_json(self):
        """This method is used to convert recurring expenses object to json object.

        Returns:
            dict: Dictionary coontaining json object for recurring expenses.

        """
        data = {}
        if self.account_id != '':
            data['account_id'] = self.account_id
        if self.paid_through_account_id != '':
            data['paid_through_account_id'] = self.paid_through_account_id
        if self.recurrence_name != '':
            data['recurrence_name'] = self.recurrence_name
        if self.start_date != '':
            data['start_date'] = self.start_date
        if self.end_date != '':
            data['end_date'] = self.end_date
        if self.recurrence_frequency != '':  
            data['recurrence_frequency'] = self.recurrence_frequency
        if self.repeat_every > 0:
            data['repeat_every'] = self.repeat_every
        if self.amount > 0:
            data['amount'] = self.amount
        if self.tax_id != '':
            data['tax_id'] = self.tax_id
        if self.is_inclusive_tax is not None:
            data['is_inclusive_tax'] = self.is_inclusive_tax
        if self.is_billable is not None:
            data['is_billable'] = self.is_billable
        if self.customer_id != '':
            data['customer_id'] = self.customer_id
        if self.vendor_id != '':
            data['vendor_id'] = self.vendor_id
        if self.project_id != '':
            data['project_id'] = self.project_id
        if self.currency_id != '':
            data['currency_id'] = self.currency_id
        if self.exchange_rate > 0:
            data['exchange_rate'] = self.exchange_rate
        return data


