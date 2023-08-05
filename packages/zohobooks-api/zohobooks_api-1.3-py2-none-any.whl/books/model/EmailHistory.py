#$Id$

class EmailHistory:
    """This class is used to create an object for Email history."""
    def __init__(self):
        """Initialize the parameters for Email hstory object."""
        self.mailhistory_id = ''
        self.from_mail_id = ''
        self.to_mail_ids = ''
        self.subject = ''
        self.date = ''
        self.type = 0

    def set_mailhistory_id(self, mailhistory_id):
        """Set mail history id.

        Args:
            mailhistory_id(str): Mail history id.

        """
        self.mailhistory_id = mailhistory_id

    def get_mailhistory_id(self):
        """Get mail history id.

        Returns:
            str: Mail history id.

        """
        return self.mailhistory_id

    def set_from(self, from_mail_id):
        """Set from mail id.

        Args:
            from_mail_id(str): From mail id.

        """
        self.from_mail_id = from_mail_id

    def get_from(self):
        """Get from mail id.

        Returns:
            str: From mail id.

        """
        return self.from_mail_id

    def set_to_mail_ids(self, to_mail_ids):
        """Set to mail id.

        Args:
            to_mail_ids(str): To mail ids.

        """
        self.to_mail_ids = to_mail_ids

    def get_to_mail_ids(self):
        """Get to mail ids.

        Returns: 
            str: To mail ids.

        """
        return self.to_mail_ids

    def set_subject(self, subject):
        """Set subject.

        Args: 
            subjecct(str): Subject.

        """
        self.subject = subject

    def get_subject(self):
        """Get subject.

        Returns:
            str: Subject.

        """
        return self.subject

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

    def set_type(self, email_type):
        """Set type.

        Args:
            type(int): Type.

        """
        self.type = email_type

    def get_type(self):
        """Get type.
 
        Returns:
            int: Type.
 
        """
        return self.type


