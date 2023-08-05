#$Id$

class ManualReminderList:
    """This class is used to create object for Reminder list."""
    def __init__(self):
        """Initialize parameters for Reminder list."""
        self.manual_reminders = []

    def set_manual_reminders(self, reminder):
        """Set reminder.

        Args:
            reminder(instance): Reminder object.

        """
        self.manual_reminders.append(reminder)

    def get_manual_reminders(self):
        """Get reminders.

        Returns:
            list of instance: List of manual reminders object.

        """
        return self.manual_reminders
