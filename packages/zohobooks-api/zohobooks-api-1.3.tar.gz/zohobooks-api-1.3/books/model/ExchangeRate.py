#$Id$

class ExchangeRate:
    """This class is used to create object for Exchange rate."""
    def __init__(self):
        """Initialize parameters for exchange rate."""
        self.exchange_rate_id = ''
        self.currency_id = ''
        self.currency_code = ''
        self.effective_date = ''
        self.rate = 0.0

    def set_exchange_rate_id(self, exchange_rate_id):
        """Set exchange rate id.

        Args:
            exchange_rate_id(str): Exchange rate id.

        """
        self.exchange_rate_id = exchange_rate_id

    def get_exchange_rate_id(self):
        """Get exchange rate id.
 
        Returns:
            str: Exchange rate id.

        """
        return self.exchange_rate_id

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
        """Get currency code.

        Returns:
            str: Currency code.

        """
        return self.currency_code

    def set_effective_date(self, effective_date):
        """Set effective date.
 
        Args:
            effective_date(str): Effective date.

        """
        self.effective_date = effective_date

    def get_effective_date(self):
        """Get effective date.

        Returns:
            str: Effective date.

        """
        return self.effective_date

    def set_rate(self, rate):
        """Set rate.

        Args:
            rate(float): Rate.

        """
        self.rate = rate

    def get_rate(self):
        """Get rate.

        Returns:
            float: Rate.

        """
        return self.rate

    def to_json(self):
        """This method is used to create json object for exchange rate.

        Returns:
            dict: Dictionary containing json object for exchange rate.

        """
        data = {}
        if self.currency_id != '':
            data['currency_id'] = self.currency_id
        if self.currency_code != '':
            data['currency_code'] = self.currency_code
        if self.effective_date != '':
            data['effective_date'] = self.effective_date
        if self.rate > 0:
            data['rate'] = self.rate
        if self.effective_date != '':
            data['effective_date'] = self.effective_date
        return data
