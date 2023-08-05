#$Id$

class CreditnoteSetting:
    """This class is used to create object for creditnotes settings."""
    def __init__(self): 
        """Initialize parameters for creditnotes settings."""
        self.auto_generate = None
        self.prefix_string = ""
        self.reference_text = ""
        self.next_number = ""
        self.notes = ""
        self.terms = ""
 
    def set_auto_generate(self, auto_generate):
        """Set whether auto number generation is enabled.

        Args: 
            auto_generate(bool): True to enable auto number genration else false.

        """
        self.auto_generate = auto_generate

    def get_auto_generate(self):
        """Set whether auto number generation is enabled. 
    
        Returns:      
            bool: True to enable auto number genration else false.

        """
        return self.auto_generate

    def set_prefix_string(self, prefix_string):
        """Set prefix string.

        Args:
            prefix_string(str): Prefix string.
 
        """
        self.prefix_string = prefix_string

    def get_prefix_string(self):
        """Get prefix string.

        Returns:
            str: Prefix string.
 
        """
        return self.prefix_string

    def set_reference_text(self, reference_text):
        """Set reference text.
 
        Args:
            reference_text(str): Reference text.

        """
        self.reference_text = reference_text

    def get_reference_text(self):
        """Get reference text.

        Returns:
            str: Reference text.

        """
        return self.reference_text

    def set_next_number(self, next_number):
        """Set reference number.

        Args:
            reference_number(str): Reference number.

        """
        self.next_number = next_number

    def get_next_number(self):
        """Get next number.

        Returns:
            str: Next number.

        """
        return self.next_number

    def set_notes(self, notes):
        """Set notes.

        Args:
            notes(str): Notes.

        """
        self.notes = notes

    def get_notes(self):
        """Get notes.

        Returns:
            str: Notes.

        """
        return self.notes

    def set_terms(self, terms):
        """Set terms.

        Args:
            terms(str): Terms.

        """
        self.terms = terms

    def get_terms(self):
        """Get terms.

        Returns:
            str: Terms.

        """
        return self.terms

    def to_json(self):
        """This method is used to convert creditnote setting object to json objcet.
 
        Returns:
            dict: Dictionary containing json object for credit note setting.

        """
        data = {}
        if self.auto_generate is not None:
            data['auto_generate'] = self.auto_generate
        if self.prefix_string != '':
            data['prefix_string'] = self.prefix_string 
        if self.reference_text != '':
            data['reference_text'] = self.reference_text
        if self.next_number != '':
            data['next_number'] = self.next_number
        if self.notes != '':
            data['notes'] = self.notes
        if self.terms != '':
            data['terms'] = self.terms
        return data
