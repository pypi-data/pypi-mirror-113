#$Id$

class Criteria: 
    """This class is used to create object for criteria."""
    def __init__(self):
        """Initialize parameters for criteria object."""
        self.criteria_id = ''
        self.field = ''
        self.comparator = ''
        self.value = 0.0

    def set_criteria_id(self, criteria_id):
        """Set criteria id.

        Args:
            criteria_id(str): Criteria id.

        """
        self.criteria_id = criteria_id

    def get_criteria_id(self):
        """Get criteria id.

        Returns:
            str: Criteria id.

        """
        return self.criteria_id

    def set_field(self, field):
        """Set field.

        Args:
            field(str): Field.
 
        """
        self.field = field

    def get_field(self): 
        """Get field.

        Returns:
            str: Field.

        """
        return self.field

    def set_comparator(self, comparator):
        """Set comparator.

        Args:
            comparator(str): Comparator.

        """
        self.comparator = comparator

    def get_comparator(self):
        """Get comparator.
 
        Returns:
            str: Comparator.

        """
        return self.comparator

    def set_value(self, value):
        """Set value.

        Args:
            value(float): Value.

        """
        self.value = value

    def get_value(self):
        """Get value.

        Returns:
            float: Value.

        """
        return self.value

    def to_json(self):
        """This method is used to convert criteria object to json object.

        Returns:
            dict: Dictionary containing json object for criteria.

        """
        data = {}
        if self.field != '':
            data['field'] = self.field
        if self.comparator != '':
            data['comparator'] = self.comparator
        if self.value > 0:
            data['value'] = self.value
        return data
          
       
