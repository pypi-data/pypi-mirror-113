#$Id$

class OpeningBalance:
    """This class is used to create object for opening balance."""
    def __init__(self):
        """Initialize parameters for opening balance."""
        self.opening_balance_id = ''
        self.date = ''
        self.accounts = []
        
    def set_opening_balance_id(self, opening_balance_id):
        """Set opening balance id.

        Args:
            opening_balance_id(str): Opening balance id.
 
        """
        self.opening_balance_id = opening_balance_id

    def get_opening_balance_id(self):
        """Get opening balance id.

        Returns:
            str: Opening balancce id.

        """
        return self.opening_balance_id

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

    def set_accounts(self, account):
        """Set accounts.

        Args:
            account(instance): Account object.

        """
        self.accounts.append(account)

    def get_accounts(self):
        """Get accounts.

        Returns:
            list of instance: List of accounts object.

        """
        return self.accounts
        
    def to_json(self):
        """This method is used to convert opening balance object to json object.

        Returns:
            dict: Dictionary containing json object for opening balance.
         
        """
        data = {}
        if self.date != '':
            data['date'] = self.date
        if self.accounts:
            data['accounts'] = []
            for value in self.accounts:
                account = value.to_json()
                data['accounts'].append(account)
        return data
