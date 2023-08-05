#$Id$

class Customer:
    """This class is used to create object for customer."""
    def __init__(self):
        """Initialize parameters for organization object. """
        self.name = ''
        self.value = ''

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

    def set_value(self, value):
        """Set value.

        Args:
            value(str): Value.

        """
        self.value = value

    def get_value(self):
        """Get value.

        Returns:
            str: Value.

        """
        return self.value
