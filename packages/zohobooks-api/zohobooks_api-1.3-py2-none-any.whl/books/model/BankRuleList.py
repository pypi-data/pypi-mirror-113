#$Id$#

class BankRuleList:
    """This class is used to create object for Bank rules list."""
    def __init__(self):
        """Initialize parameters for bank rules list."""
 
        self.bank_rules = []

    def set_bank_rules(self, bank_rules):
        """Set bank rules.
 
        Args: 
            bank_rules(instance): Bank rules object.

        """
        self.bank_rules.append(bank_rules)

    def get_bank_rules(self):
        """Get bank rules.

        Returns: 
            list of instance: List of bank rules object.

        """
        return self.bank_rules 
