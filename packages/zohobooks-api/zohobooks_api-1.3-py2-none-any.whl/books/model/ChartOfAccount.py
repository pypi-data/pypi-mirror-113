#$Id$

class ChartOfAccount:
    """Create object for Chart of Accounts."""
    def __init__(self):
        """Initialize parameters for Chart of accounts."""
        self.account_id = ''
        self.account_name = ''
        self.is_active = None
        self.account_type = ''
        self.account_type_formatted = ''
        self.currency_id = ''
        self.description = ''
        self.is_user_created = None
        self.is_involved_in_transaction = None
        self.is_system_account = None
        #self.current_balance = 0.0 #Not mentioned 

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

    def set_is_active(self, is_active): 
        """Set whether the account is active or not.

        Args:
            is_active(bool): True if active else False.

        """
        self.is_active = is_active

    def get_is_active(self): 
        """Get whether is active.

        Returns:
            bool: True if active else false.

        """
        return self.is_active

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

    def set_account_type_formatted(self, account_type_formatted):
        """Set account type formatted.

        Args:
            account_type_formatted(str): Account type formatted.

        """
        self.account_type_formatted = account_type_formatted

    def get_account_type_formatted(self):
        """Get acccount type formatted.

        Returns:
            str: Account type formatted.

        """
        return self.account_type_formatted
  
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

    def set_description(self, description):
        """Set descripiton.

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

    def set_is_user_created(self, is_user_created):
        """Set whether the account is user created.

        Args:
            is_user_created(bool): True if user created else False.

        """
        self.is_user_created = is_user_created

    def get_is_user_created(self):
        """Get whether the account is user created.

        Returns:
            bool: True if user created else False.

        """
        return self.is_user_created

    def set_is_involved_in_transaction(self, is_involved_in_transaction):
        """Set Whether the account is involved in transactions.

        Args:
            is_involved_in_transaction(bool): True if the account is involved in transactions else False.

        """
        self.is_involved_in_transaction = is_involved_in_transaction

    def get_is_involved_in_transaction(self):
        """Get whether the account is involved in transactions.

        Returns:
            bool: True if the account is involved in transaction.

        """
        return self.is_involved_in_transaction

    def set_is_system_account(self, is_system_account): 
        """Set whether the account is system account.

        Args:
            is_system_account(bool): True if system account else False.

        """
        self.is_system_account = is_system_account

    def get_is_system_account(self):
        """Get whether the account is system account.

        Returns:
            bool: True if system account else False.

        """
        return self.is_system_account

    '''def set_current_balance(self, current_balance):
        """Set current balance.

        Args:
            current_balance(float): Current balance.

        """
        self.current_balance = current_balance

    def get_current_balance(self): 
        """Get current balance.

        Returns:
            float: Current balance.

        """
        return self.current_balance'''

    def to_json(self):
        """This method is used to convert chart of accounts object to json object.

        Returns:
            dict: Dictionary containing json object for chart of accounts.

        """
        data = {}
        if self.account_name != '':
            data['account_name'] = self.account_name
        if self.account_type != '':
            data['account_type'] = self.account_type
        if self.currency_id != '':
            data['currency_id'] = self.currency_id
        if self.description != '':
            data['description'] = self.description
        return data

 
