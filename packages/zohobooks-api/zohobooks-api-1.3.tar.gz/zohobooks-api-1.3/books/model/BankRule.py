#$Id$

class BankRule:
    """This class is used to create object for bank rules."""
    def __init__(self):
        """Initialize parameters for Bank rules."""
        self.rule_id = ''
        self.rule_name = ''
        self.rule_order = 0
        self.apply_to = ''
        self.target_account_id = ''
        self.apply_to = ''
        self.criteria_type = ''
        self.criterion = []
        self.record_as = ''
        self.account_id = ''
        self.account_name = ''
        self.tax_id = ''
        self.reference_number = ''
        self.customer_id = ''
        self.customer_name = ''

    def set_rule_id(self, rule_id): 
        """Set rule id.

        Args:
            rule_id(str): Rule id.

        """
        self.rule_id = rule_id

    def get_rule_id(self): 
        """Get rule id.
           
        Returns:
            str: Rule id.

        """
        return self.rule_id

    def set_rule_name(self, rule_name):
        """Set rule name.

        Args:
            rule_name(str): Rule name.

        """
        self.rule_name = rule_name

    def get_rule_name(self):
        """Get rule name.

        Returns:
            str:Rule name.

        """
        return self.rule_name

    def set_rule_order(self, rule_order):
        """Set rule order.

        Args:
            rule_order(int): Rule order.

        """
        self.rule_order = rule_order

    def get_rule_order(self):
        """Get rule order.

        Returns:
            int: Rule order.

        """
        return self.rule_order

    def set_apply_to(self, apply_to):
        """Set apply to.

        Args:
            apply_to(str): Apply to.

        """
        self.apply_to = apply_to

    def get_apply_to(self):
        """Get apply to.

        Returns:
            str: Apply to.

        """
        return self.apply_to

    def set_criteria_type(self, criteria_type):
        """Set criteria type.

        Args:
            criteria_type(str): Criteria type.

        """
        self.criteria_type = criteria_type

    def get_criteria_type(self):
        """Get criteria type.

        Returns: 
            str: Criteria type.

        """
        return self.criteria_type

    def set_target_account_id(self, target_account_id):
        """Set target account id.

        Args:
            target_account_id(str): Target account id.

        """
        self.target_account_id = target_account_id

    def get_target_account_id(self):
        """Get target account id.

        Returns:
            str: Target account id.

        """
        return self.target_account_id
  
    def set_criterion(self, criteria):
        """Set criterion.

        Args:
            criteria(instance): Criteria object.

        """
        self.criterion.append(criteria)

    def get_criterion(self): 
        """Get criterion.

        Returns: 
            list of instance: List of criteria object.

        """
        return self.criterion

    def set_record_as(self, record_as):  
        """Set record as.

        Args:
            record_as(str): Record as.

        """
        self.record_as = record_as

    def get_record_as(self):
        """Get record as.

        Returns:
            str: Record as.

        """
        return self.record_as

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

    def set_tax_id(self, tax_id):
        """Set tax id.
  
        Args:
            tax_id(str): Tax id.

        """	
        self.tax_id = tax_id

    def get_tax_id(self):
        """Get tax id.

        Returns:
            str:Tax id.

        """
        return self.tax_id

    def set_reference_number(self, reference_number): 
        """Set reference number.

        Args: 
            reference_number(str): Reference number.

        """
        self.reference_number = reference_number

    def get_reference_number(self):
        """Get reference number.

        Returns:
            str: Reference number.

        """
        return self.reference_number

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

    def set_customer_name(self, customer_name):
        """Set customer name.

        Args:
            customer_name(str): Customer name.

        """
        self.customer_name = ''
 
    def get_customer_name(self):
        """Get customer name.

        Returns:
            str: Customer name.
 
        """
        return self.customer_name

    def to_json(self):
        """This method is used to convert bills object to json object.

        Returns:
            dict: Dictionary containing json object for bank rules.

        """
        data = {}
        if self.rule_name != '':
            data['rule_name'] = self.rule_name
        if self.target_account_id != '':
            data['target_account_id'] = self.target_account_id
        if self.apply_to != '':
            data['apply_to'] = self.apply_to
        if self.criteria_type != '':
            data['criteria_type'] = self.criteria_type
        if self.criterion:
            data['criterion'] = []
            for value in self.criterion:
               criteria = value.to_json()
               data['criterion'].append(criteria)
        if self.record_as != '':
            data['record_as'] = self.record_as
        if self.account_id != '':
            data['account_id'] = self.account_id
        if self.tax_id != '':
            data['tax_id'] = self.tax_id
        if self.reference_number != '':
            data['reference_number'] = self.reference_number
        if self.customer_id != '':
            data['customer_id'] = self.customer_id
        return data
