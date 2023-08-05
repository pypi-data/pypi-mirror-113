#$Id$#

class ExchangeRateList:
    """This class is used to create object for Exchange Rate List."""
  
    def __init__(self):
        """Initialize parameters for exchange rate list."""
        self.exchange_rates = []

    def set_exchange_rates(self, exchange_rate):
        """Set exchange rate.

        Args:
            exchange_rate(instance): Exchange rate.

        """
        self.exchange_rates.append(exchange_rate)

    def get_exchange_rates(self):
        """Get exchange rate.

        Returns:
            list of instance: List of exchange rate object.
 
        """
        return self.exchange_rates
