#$Id$

class Account:
    """This class is used to create object for accounts object."""
    def __init__(self):
        """Initialize parameters for Accounts."""
        self.account_id = ''
        self.account_name = ''
        self.bcy_balance = 0.0
        self.bcy_balance_formatted = ''
        self.fcy_balance = 0.0
        self.fcy_balance_formatted = ''
        self.adjusted_balance = 0.0
        self.adjusted_balance_formatted = ''
        self.gain_or_loss = 0.0
        self.gain_or_loss_formatted = ''
        self.gl_specific_type = 0

        self.account_split_id = ''
        self.debit_or_credit = ''
        self.exchange_rate = 0.0
        self.currency_id = ''
        self.currency_code = ''
        self.bcy_amount = 0.0
        self.amount = 0.0

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

    def set_bcy_balance(self, bcy_balance):
        """Set bcy balance.

        Args:
            bcy_balance(float): Bcy balance.

        """
        self.bcy_balance = bcy_balance

    def get_bcy_balance(self):
        """Get bcy balance.

        Returns:
            float: Bcy balance.

        """
        return self.bcy_balance

    def set_bcy_balance_formatted(self, bcy_balance_formatted): 
        """Set bcy balance formatted.

        Args:
            bcy_balance_formatted(str): Bcy balance formatted.

        """
        self.bcy_balance_formatted = bcy_balance_formatted

    def get_bcy_balance_formatted(self):
        """Get bcy balance formatted.

        Returns:
            str: Bcy balance formatted.

        """
        return self.bcy_balance_formatted

    def set_fcy_balance(self, fcy_balance):
        """Set fcy balance.

        Args:
            fcy_balance(float): Fcy balance.

        """
        self.fcy_balance = fcy_balance

    def get_fcy_balance(self):
        """Get fcy balance.

        Returns:
            float: Fcy balance.

        """
        return self.fcy_balance

    def set_fcy_balance_formatted(self, fcy_balance_formatted):
        """Set fcy balance formatted.

        Args:
            fcy_balance_formatted(str): Fcy balance formatted.

        """
        self.fcy_balance_formatted = fcy_balance_formatted

    def get_fcy_balance_formatted(self): 
        """Get fcy balance formatted.

        Returns:
            str: Fcy balance formatted.

        """
        return self.fcy_balance_formatted

    def set_adjsuted_balance(self, adjusted_balance):
        """Set adjusted balance.

        Args:
            adjusted_balance(float): Adjusted balance.

        """
        self.adjusted_balance = adjusted_balance

    def get_adjusted_balance(self): 
        """Get adjusted balance.

        Returns: 
            float: Adjusted balance.

        """
        return self.adjusted_balance

    def set_adjusted_balance(self, adjusted_balance):
        """Set adjusted balance.

        Args:
            adjusted_balance(float): Adjusted balance.

        """
        self.adjusted_balance = adjusted_balance

    def get_adjusted_balance(self):
        """Get adjusted balance.

        Returns:
            float: Adjusted balance.

        """
        return self.adjusted_balance

    def set_adjusted_balance_formatted(self, adjusted_balance_formatted):
        """Set adjusted balance formatted.

        Args:
            adjusted_balance_formatted(str): Adjusted balance formatted.

        """
        self.adjusted_balance_formatted = adjusted_balance_formatted

    def get_adjusted_balance_formatted(self): 
        """Get adjusted balance formatted.

        Returns: 
            str: Adjusted balance formatted.

        """
        return self.adjusted_balance_formatted

    def set_gain_or_loss(self, gain_or_loss): 
        """Set gain or loss.

        Args:
            gain_or_loss(float): Gain or loss.

        """
        self.gain_or_loss = gain_or_loss

    def get_gain_or_loss(self):
        """Get gain or loss.
 
        Returns:
            float: Gain or loss.

        """
        return self.gain_or_loss

    def set_gain_or_loss_formatted(self, gain_or_loss_formatted):
        """Set gain or loss formatted.

        Args:
            gain_or_loss_formatted(str): Gain or loss formatted.

        """
        self.gain_or_loss_formatted = gain_or_loss_formatted

    def get_gain_or_loss_formatted(self):
        """Get gain or loss formatted.

        Returns: 
            str: Gain or loss formatted.

        """
        return self.gain_or_loss_formatted

    def set_gl_specific_type(self, gl_specific_type):
        """Set gl specific type.

        Args:
            gl_specific_type(int): Gl specific type.

        """
        self.gl_specific_type = gl_specific_type

    def get_gl_specific_type(self):
        """Get gl specific type.

        Returns:
            int: Gl specific type.

        """
        return self.gl_specific_type

    def set_account_split_id(self, account_split_id):
        """Set account split id.
 
        Args: 
            account_split_id(str): Account split id.
 
        """
        self.account_split_id = account_split_id

    def get_account_split_id(self):
        """Get account split id.

        Returns:
            str: Account split id.
 
        """
        return self.account_split_id

    def set_debit_or_credit(self, debit_or_credit):
        """Set debit or credit.

        Args:
            debit_or_credit(str): Debit or credit.
 
        """
        self.debit_or_credit = debit_or_credit

    def get_debit_or_credit(self):
        """Get debit or credit.

        Returns:
            str: Debit or credit.

        """  
        return self.debit_or_credit

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

    def set_currency_id(self, currency_id): 
        """Set currency id.
 
        Args:
            str: Currecny id.
  
        """
        self.currency_id = currency_id

    def get_currency_id(self): 
        """Get currency id.

        Returns:
            str: Currency id.

        """
        return self.currency_id

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

    def set_bcy_amount(self, bcy_amount):
        """Set bcy amount.

        Args:
            bcy_amount(float): Bcy amount.

        """
        self.bcy_amount = bcy_amount

    def get_bcy_amount(self):
        """Get bcy amount.

        Returns:
            float: Bcy amount.

        """
        return self.bcy_amount

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

    def to_json(self):
        """This method is used to create json object for accounts.

        Returns:
            dict: Dictionary containing json object for accounts.

        """
        data = {}
        if self.account_id != '':
            data['account_id'] = self.account_id
        if self.debit_or_credit != '':
            data['debit_or_credit'] = self.debit_or_credit
        if self.exchange_rate > 0:
            data['exchange_rate'] = self.exchange_rate
        if self.currency_id != '':
            data['currency_id'] = self.currency_id
        if self.amount > 0: 
            data['amount'] = self.amount
        return data

