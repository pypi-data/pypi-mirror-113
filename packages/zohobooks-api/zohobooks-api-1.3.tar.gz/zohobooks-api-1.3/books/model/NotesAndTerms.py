#$Id$

class NotesAndTerms:
    """This class is used to create object for notes and terms."""
    def __init__(self):
        """Initialize parameters for notes and terms."""
        self.notes = ''
        self.terms = ''
 
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
        """This method is used to convert notes and terms object to json form.
 
        Returns:
            dict: Dictionary containing json object for notes and terms.

        """
        data = {} 
        if self.notes != '':
            data['notes'] = self.notes
        if self.terms != '':
            data['terms'] = self.terms
        return data
