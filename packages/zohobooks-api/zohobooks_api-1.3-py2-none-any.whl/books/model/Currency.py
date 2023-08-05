#$Id$

class Currency:
    """This class is used to create object for currency. """
    def __init__(self):
        """Initialize parameters for currency object."""
        self.currency_id = ''
        self.currency_code = ''
        self.currency_name = ''
        self.currency_symbol = ''
        self.price_precision = 0
        self.currency_format = ''
        self.is_base_currency = None
        self.exchange_rate = 0.0
        self.effective_date = ''

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

    def set_currency_name(self, currency_name):
        """Set currency name.

        Args:
            currency_name(str): Currency name.

        """
        self.currency_name = currency_name

    def get_currency_name(self): 
        """Get currency name.

        Returns:
            str: Currency name.

        """
        return self.currency_name

    def set_currency_symbol(self, currency_symbol):
        """Set currency symbol.

        Args:
            currency_symbol(str): Currency symbol.

        """
        self.currency_symbol = currency_symbol

    def get_currency_symbol(self):
        """Get currency symbol.

        Returns:
            str: Currency symbol.

        """
        return self.currency_symbol

    def set_price_precision(self, price_precision):
        """Set price precision.

        Args:
            price_precision(int): Price precision.

        """
        self.price_precision = price_precision

    def get_price_precision(self):
        """Get price precision.

        Returns:
            int: Price precision.
 
        """
        return self.price_precision

    def set_currency_format(self, currency_format):
        """Set currency format.

        Args:
            currency_format(str): Currency format.

        """
        self.currency_format = currency_format

    def get_currency_format(self):
        """Get currency format.

        Returns:
            str: Currency fromat.

        """
        return self.currency_format

    def set_is_base_currency(self, is_base_currency):
        """Set whether the currency is base currency.

        Args:
            is_base_currency(bool): True if it is base currency else False.
      
        """
        self.is_base_currency = is_base_currency

    def get_is_base_currency(self):
        """Get whether the currency is base currency.

        Returns:
            bool: True if it is base currency else false.

        """
        return self.is_base_currency

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

    def to_json(self):
        """This method is used to create json object for currency.

        Returns:
            dict: Dictionary containing json object for currency.

        """
        data = {}
        if self.currency_code != '':
            data['currency_code'] = self.currency_code
        if self.currency_symbol != '':
            data['currency_symbol'] = self.currency_symbol
        if self.price_precision > 0:
            data['price_precision'] = self.price_precision
        if self.currency_format != '':
            data['currency_format'] = self.currency_format
        return data
