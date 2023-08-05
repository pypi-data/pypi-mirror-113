#$Id$

from books.model.PlaceHolder import PlaceHolder

class ManualReminder:
    """This class is used to create object for manual reminders."""
    def __init__(self):
        """Initilaize parameters for manual reminders."""
        self.manualreminder_id = ''
        self.type = ''
        self.subject = ''
        self.body = ''
        self.cc_me = None
        self.placeholder = PlaceHolder()

    def set_manualreminder_id(self, manualreminder_id):
        """Set manual reminder id.

        Args:
            manualreminder_id(str): Manual reminder id.

        """
        self.manualreminder_id = manualreminder_id

    def get_manualreminder_id(self):
        """Get manual reminder id.

        Returns:
            str: Manual reminder id.

        """
        return self.manualreminder_id

    def set_type(self, type):
        """Set type.

        Args:
            type(str): Type.

        """
        self.type = type

    def get_type(self):
        """Get type.

        Returns:
            str: Type.

        """
        return self.type

    def set_subject(self, subject):
        """Set subject.

        Args:
            subject(str): Subject.

        """
        self.subject = subject

    def get_subject(self):
        """Get subject.

        Returns:
            str: Subject.

        """
        return self.subject

    def set_body(self, body):
        """Set body.

        Args:
            body(str): Body.

        """
        self.body = body

    def get_body(self):
        """Get body.

        Returns:
            str: Body.

        """
        return self.body

    def set_cc_me(self, cc_me):
        """Set cc me.

        Args:
            cc_me(bool): True to cc me else false.

        """
        self.cc_me = cc_me

    def get_cc_me(self):
        """Get cc me.

        Returns: 
            bool: True to cc me else false.

        """
        return self.cc_me

    def set_placeholders(self, placeholders):
        """Set place holders.

        Args:
            place_holders: Palce holders object.

        """
        self.placeholders = placeholders

    def get_placeholders(self):
        """Get place holders.

        Returns:
            instance: Place holders.

        """
        return self.placeholders

    def to_json(self): 
        """"This method is used to convert manual reminder object to json format.

        Returns:
            dict: Dictionary containing json object for manual reminders.

        """
        data = {}
        if self.subject != '':
            data['subject'] = self.subject
        if self.body != '':
            data['body'] = self.body
        if self.cc_me is not None: 
            data['cc_me'] = self.cc_me
        return data
 
