#$Id$

class Item:
    """This class is used to create object for item."""
    def __init__(self):
        """Initialize parameters for Item object."""
        self.item_id = ''
        self.name = ''
        self.status = ''
        self.description = ''
        self.rate = 0.0
        self.unit = ''
        self.account_id = ''
        self.account_name = ''
        self.tax_id = ''
        self.tax_name = ''
        self.tax_percentage = 0.0
        self.tax_type = ''
        self.item_tax_preferences = []

    def set_item_tax_preferences(self, item_tax_preference):
        """Set item_tax_preferences.

        Args:
            item_tax_preference(instance): item_tax_preference object.

        """
        self.item_tax_preferences.append(item_tax_preference)

    def get_item_tax_preferences(self):
        """Get item_tax_preference.

        Returns: 
            instance: item_tax_preference object.

        """
        return self.item_tax_preferences

    def set_item_id(self, item_id):
        """Set item id.

        Args:
            item_id(str): Item id.

        """
        self.item_id = item_id

    def get_item_id(self):
        """Get item id.

        Returns:
            str: Item id.

        """
        return self.item_id

    def set_name(self, name):
        """Set name.

        Args:
            name(str): Name.

        """
        self.name = name

    def get_name(self):
        """Get name.

        Returns:
            str: Name.

        """
        return self.name

    def set_status(self, status):
        """Set status.

        Args:
            status(str): Status.

        """
        self.status = status

    def get_status(self):
        """Get status.
  
        Returns:
            str: Status.

        """
        return self.status

    def set_description(self,description):
        """Set description.
 
        Args:
            descritpion(str): Description.

        """
        self.description = description

    def get_description(self):
        """Get description.

        Returns:
            str: Descritpion.

        """
        return self.description

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

    def set_unit(self, unit):
        """Set unit.

        Args:
            unit(float): Unit.
    
        """
        self.unit = unit

    def get_unit(self):
        """Get unit.

        Returns:
            float: Unit.

        """
        return self.unit

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
            str: Account name.

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
            str: Tax id.

        """
        return self.tax_id

    def set_tax_name(self, tax_name):
        """Set tax name.

        Args:
            tax_name(str): Tax name.

        """
        self.tax_name = tax_name

    def get_tax_name(self):
        """Get tax name.

        Returns:
            str: Tax name.

        """
        return self.tax_name

    def set_tax_percentage(self, tax_percentage):
        """Set tax percentage.

        Args:
            tax_percentage(float): Tax percentage.

        """
        self.tax_percentage = tax_percentage

    def get_tax_percentage(self):
        """Get tax percentage.

        Returns: 
            float: Tax percentage.

        """
        return self.tax_percentage

    def set_tax_type(self, tax_type):
        """Set tax type.

        Args:
            tax_type(str): Tax type.

        """
        self.tax_type = tax_type

    def get_tax_type(self):
        """Get tax type.

        Returns:
            str: Tax type.

        """
        return self.tax_type

    def to_json(self):
        """This method is used to create json object for items.

        Returns: 
            dict: Dictionary containing json object for items.

        """
        data = {}
        if self.name != '':
            data['name'] = self.name
        if self.description != '':
            data['description'] = self.description
        if self.rate > 0:
            data['rate'] = self.rate
        if self.account_id != '':
            data['account_id'] = self.account_id 
        if self.tax_id != '':
            data['tax_id'] = self.tax_id
        if self.item_tax_preferences:
            data['item_tax_preferences'] = self.item_tax_preferences
        return data

