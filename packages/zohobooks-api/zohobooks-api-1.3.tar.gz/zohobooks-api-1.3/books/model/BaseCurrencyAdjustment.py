#$Id$

class BaseCurrencyAdjustment: 
    """This class is used to create object for Base Currency adjustment."""
    def __init__(self):
        """Initialize parameters for Base currency adjustment."""
        self.base_currency_adjustment_id = ''
        self.adjustment_date = ''
        self.exchange_rate = 0.0
        self.exchange_rate_formatted = ''
        self.currency_id = ''
        self.currency_code = ''
        self.notes = ''
        self.gain_or_loss = 0.0
        self.adjustment_date_formatted = ''
        self.accounts = []

    def set_base_currency_adjustment_id(self, base_currency_adjustment_id):
        """Set base currency adjustment id.

        Args:
            base_currency_adjustment_id(str): Base currency adjustment id.

        """
        self.base_currency_adjustment_id = base_currency_adjustment_id

    def get_base_currency_adjustment_id(self):
        """Get base currency adjustment id.

        Returns:
            str: Base currency adjustment id.

        """
        return self.base_currency_adjustment_id

    def set_adjustment_date(self, adjustment_date): 
        """Set adjustment date.

        Args:
            adjustment_date(str): Adjustment date.

        """ 
        self.adjustment_date = adjustment_date

    def get_adjustment_date(self): 
        """Get adjustment date.

        Returns:
            str: Adjustment date.

        """
        return self.adjustment_date

    def set_exchange_rate(self, exchange_rate):
        """Set exchaneg rate.

        Args:
            exchaneg_rate(float): Exchange rate.

        """
        self.exchange_rate = exchange_rate

    def get_exchange_rate(self):
        """Get exchange rate.

        Returns:
            float: Exchange rate.

        """
        return self.exchange_rate

    def set_exchange_rate_formatted(self, exchange_rate_formatted):
        """Set exchange rate formatted.

        Args: 
            exchange_rate_formatted(str): Exchange rate formatted.

        """
        self.exchange_rate_formatted = exchange_rate_formatted

    def get_exchange_rate_formatted(self):
        """Get exchange rate formatted.

        Returns:
            str: Exchange rate formatted.

        """
        return self.exchange_rate_formatted
    
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
        """Set currency code.

        Args:
            currency_code(str): Currency code.

        """
        self.currency_code = currency_code

    def get_currency_code(self): 
        """Get currecny code.

        Returns:  
            str: Currency code.

        """
        return self.currency_code

    def set_notes(self, notes):
        """Set notes.
 
        Args:
            notes(str): Notes.

        """
        self.notes = notes

    def get_notes(self):
        """Get notes.

        Returns: 
            str: Notes.

        """
        return self.notes
    
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

    def set_adjustment_date_formatted(self, adjustment_date_formatted):
        """Set adjustment date formatted.

        Args:
            adjustment_date_formatted(str): Adjustment date formatted.

        """
        self.adjustment_date_formatted = adjustment_date_formatted

    def get_adjustment_date_foramtted(self):
        """Get adjustment date formatted.

        Returns: 
            str: Adjustment date formatted.

        """
        return self.adjustment_date_formatted

    def set_accounts(self, accounts):
        """Set accounts.

        Args:
            accounts(instance): Accounts.

        """
        self.accounts.append(accounts)

    def get_accounts(self):
        """Get accounts.

        Returns:
            instance: Accounts.

        """
        return self.accounts

    def to_json(self):
        """This method is used to convert base currency adjusment object in json format.

        Returns:
            dict: Dictionary containing json object for base currency adjustment.

        """
        data = {}
        if self.currency_id != '':
            data['currency_id'] = self.currency_id
        if self.adjustment_date != '':
            data['adjustment_date'] = self.adjustment_date
        if self.exchange_rate > 0:
            data['exchange_rate'] = self.exchange_rate
        if self.notes != '':
            data['notes'] = self.notes
        return data
