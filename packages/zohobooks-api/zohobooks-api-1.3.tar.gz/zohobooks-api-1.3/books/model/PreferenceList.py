#$Id$

from books.model.Preference import Preference
from books.model.CustomField import CustomField
from books.model.PlaceholderAddressFormat import PlaceholderAddressFormat

class PreferenceList:
    """This class is used to create object for Preferences list."""
    def __init__(self): 
        """Initialize parameters for preferences list."""
        self.preferences = Preference()
        self.custom_fields = CustomField()
        self.placeholders_address_format = PlaceholderAddressFormat()

    def set_preferences(self, preference):
        """Set preferences.

        Args:
            preference(instance): Preference object.

        """
        self.preferences = preference

    def get_preferences(self):
        """Get preferneces.

        Retruns:
            instance: Preferences object.

        """
        return self.preferences

    def set_custom_fields(self, custom_fields):
        """Set custom fields.

        Args:
            custom_fields(instance): Custom fields.

        """
        self.custom_fields = custom_fields

    def set_placeholders_address_format(self, placeholders_address_format):
        """Set placeholders address format.

        Args:
            placeholders_address_format(instance): Place holders address format.

        """
        self.placeholdedrs_address_format = placeholders_address_format

    def get_placeholders_address_format(self):
        """Get placeholders address format.

        Returns:
            instance: Placeholders address format.

        """
        return self.placeholders_address_format

