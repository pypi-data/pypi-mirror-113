#$Id$

class AutoReminderList:
    """This class is used to create object for Reminder list."""
    def __init__(self):
        """Initialize parameters for Reminder list."""
        self.auto_reminders = []

    def set_auto_reminders(self, reminder):
        """Set reminder.

        Args:
            reminder(instance): Reminder object.

        """
        self.auto_reminders.append(reminder)

    def get_auto_reminders(self):
        """Get reminders.

        Returns:
            list of instance: List of manual reminders object.

        """
        return self.auto_reminders
