#$Id$

from books.model.PlaceHolder import PlaceHolder

class Autoreminder: 
    """This class is used to create object for auto reminders."""
    def __init__(self):
        """Initialize parameters for auto reminders object."""
        self.payment_reminder_id = ''
        self.is_enabled = None
        self.notification_type = ''
        self.address_type = ''
        self.number_of_days = 0
        self.subject = ''
        self.body = ''
        self.autoreminder_id = ''
        self.order = 0
        self.name = ''
        self.cc_addresses = ''
        self.placeholder = PlaceHolder()
    
    def set_cc_addresses(self, cc_addresses):
        """Set cc addresses.

        Args:
            cc_addresses(str): Cc addresses.

        """
        self.cc_addresses = cc_addresses

    def get_cc_addresses(self):
        """Get cc addresses.

        Returns:
            str: Cc addresses.

        """
        return self.cc_addresses

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

    def set_payment_reminder_id(self, payment_reminder_id):
        """Set payment reminder id.

        Args:
            payment_reminder_id(str): Payment reminder id.

        """ 
        self.payment_reminder_id = payment_reminder_id

    def get_payment_reminder_id(self):
        """Get payment reminder id.

        Returns:
            str: Payment reminder id.

        """
        return self.payment_reminder_id

    def set_is_enabled(self, is_enabled):
        """Set whether it is enabled or not.

        Args:
            is_enabled(bool): True to enable else False.

        """
        self.is_enabled = is_enabled

    def get_is_enabled(self):
        """Get is enabled.

        Returns:
            bool: True if enabled else false.

        """
        return self.is_enabled

    def set_notification_type(self, notification_type):
        """Set notification type.

        Args:
            notification_type(str): Notification type.

        """
        self.notification_type = notification_type

    def get_notification_type(self):
        """Get notification type.
 
        Returns: 
            str: Notification type.

        """
        return self.notification_type

    def set_address_type(self, address_type):
        """Set address type.

        Args:
            address_type(str): Address type.

        """
        self.address_type = address_type

    def get_address_type(self):
        """Get address type.

        Returns:
            str: Address type.

        """
        return self.address_type

    def set_number_of_days(self, number_of_days):
        """Set number of days.

        Args:
            number_of_days(int): Number of days.

        """
        self.number_of_days = number_of_days

    def get_number_of_days(self):
        """Get number of days.

        Returns:
            int: Number of days.

        """
        return self.number_of_days

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

    def set_autoreminder_id(self, autoreminder_id):
        """Set autoreminder id.

        Args:
            autoreminder_id(str): Auto reminder id.

        """
        self.autoreminder_id = autoreminder_id

    def get_autoreminder_id(self):
        """Get autoreminder id.

        Returns:
            str: Auto reminder id.

        """ 
        return self.autoreminder_id

    def set_order(self, order):
        """Set order.

        Args:
            order(int): Order.

        """
        self.order = order

    def get_order(self):
        """Get order.

        Returns:
            int: Order.

        """
        return self.order

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
        """This method is used to convert auto reminder object to json object.

        Returns:
            dict: Dictionary cocntaining json object for autoreminder.

        """
        data = {}
        if self.is_enabled != '':
            data['is_enabled'] = self.is_enabled
        if self.notification_type != '':
            data['type'] = self.notification_type
        if self.address_type != '':
            data['address_type'] = self.address_type
        if self.subject != '':
            data['subject'] = self.subject
        if self.body != '':
            data['body'] = self.body
        return data
