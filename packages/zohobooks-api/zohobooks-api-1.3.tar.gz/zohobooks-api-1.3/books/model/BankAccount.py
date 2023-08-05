#$Id$

class BankAccount:
    """This class is used to create object for Bank accounts."""
    def __init__(self):
        """Initialize parameters for Bank accounts object."""
        self.account_id = ''
        self.account_name = ''
        self.currency_id = ''
        self.currency_code = ''
        self.account_type = ''
        self.account_number = ''
        self.uncategorized_transactions = ''
        self.is_active = None
        self.balance = 0.0
        self.bank_name = ''
        self.routing_number = ''
        self.is_primary_account = None
        self.is_paypal_account = None
        self.paypal_email_address = ''
        self.description = ''
        self.paypal_type = ''
 
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

    def set_currency_code(self, currency_code): 
        """Set currecny code.

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
 
    def set_account_type(self, account_type):
        """Set account type.

        Args:
            account_type(str): Account type.

        """
        self.account_type = account_type

    def get_account_type(self):
        """Get account type.

        Returns:
            str: Account type.

        """
        return self.account_type

    def set_account_number(self, account_number):
        """Set account number.

        Args:
            account_number(str): ACcount number.

        """
        self.acccount_number = account_number

    def get_account_number(self):
        """Get account number.

        Returns: 
            str: Account number.

        """
        return self.account_number

    def set_uncategorized_transactions(self, uncategorized_transactions):
        """Set uncategorized transactions.

        Args:
            uncategorized_transactions(str): Uncategorized transactions.

        """
        self.uncategorized_transactions = uncategorized_transactions

    def get_uncategorized_transactions(self):
        """Get uncategorized transactions.

        Returns:
            str: Uncategorized transactions.

        """
        return self.uncategorized_transactions

    def set_is_active(self, is_active): 
        """Set whether the account is active or not.
 
        Args:
            is_active(bool): True if it is active else False.

        """
        self.is_active = is_active

    def get_is_active(self):
        """Get whether the bank account is active or not.

        Returns:
            bool: True if active else False.

        """
        return self.is_active

    def set_balance(self, balance):
        """Set balance.

        Args:
            balance(float): Balance.

        """
        self.balance = balance

    def get_balance(self): 
        """Get balance.

        Returns:
            float: Balance.

        """
        return self.balance

    def set_bank_name(self, bank_name):
        """Set bank name.

        Args:
            bank_name(str): Bank name.

        """
        self.bank_name = bank_name

    def get_bank_name(self):
        """Get bank name.

        Returns:
            str: Bank name.

        """
        return self.bank_name 
 
    def set_routing_number(self, routing_number):
        """Set routing number.

        Args:
            routing_number(str): Routing number.

        """
        self.routing_number = routing_number

    def get_routing_number(self): 
        """Get routing number.

        Returns:
            str: Routing number.

        """
        return self.routing_number

    def set_is_primary_account(self, is_primary_account):
        """Set whether the bank account is primary account or not.
   
        Args:
            is_primary_account(bool): True if it is primary account else False.

        """
        self.is_primary_account = is_primary_account

    def get_is_primary_account(self):
        """Get whether the bank account is primary account or not.

        Returns:
            bool: True if it is primary account else False.

        """
        return self.is_primary_account

    def set_is_paypal_account(self, is_paypal_account): 
        """Set whether the account is paypal account.

        Args:
            is_paypal_account(bool): True if the account is paypal account.

        """
        self.is_paypal_account = is_paypal_account

    def get_is_paypal_account(self): 
        """Get whether the account is paypal account.

        Returns:
            bool: True if the account is paypal account else False.

        """
        return self.is_paypal_account
 
    def set_paypal_email_address(self, paypal_email_address):
        """Set paypal email address.

        Args:
            paypal_email_Address(str): Paypal email address.

        """
        self.paypal_email_address = paypal_email_address

    def get_paypal_email_address(self):
        """Get paypal email address.

        Returns:
            str: PAypal email address.
 
        """
        return self.paypal_email_address

   
 
    def set_description(self, description):
        """Set description.

        Args:
            description(str): Description.

        """
        self.descrition = description
 
    def get_description(self):
        """Get description.

        Returns:  
            str: Description.

        """
        return self.description

    def set_paypal_type(self, paypal_type):
        """Set paypal type.

        Args:
            paypal_type(str): Paypal type.

        """
        self.paypal_type = paypal_type

    def get_paypal_type(self):
        """Get paypal type.

        Returns:
            str: Paypal type.

        """
        return self.paypal_type

    def to_json(self):
        """This method is used to create json object for bank acoounts.
        
        Returns:
            dict: Dictionary containing json object for bank accounts.

        """
        data = {}
        if self.account_name != '':
            data['account_name'] = self.account_name
        if self.account_type != '':
            data['account_type'] = self.account_type
        if self.account_number != '':
            data['account_number'] = self.account_number
        if self.currency_id != '':
            data['currency_id'] = self.currency_id
        if self.description != '':
            data['description'] = self.description
        if self.bank_name != '':
            data['bank_name'] = self.bank_name
        if self.routing_number != '':
            data['routing_number'] = self.routing_number
        if self.is_primary_account is not None:
            data['is_primary_account'] = self.is_primary_account
        if self.is_paypal_account is not None:
            data['is_paypal_account'] = self.is_paypal_account
        if self.paypal_type != '':
            data['paypal_type'] = self.paypal_type
        if self.paypal_email_address != '':
            data['paypal_email_address'] = self.paypal_email_address
        return data
