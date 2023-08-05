#$Id$

class TimeEntry: 
    """This class is used to create object for Time Entry."""
    def __init__(self):
        """Initialize parameters for Time entry object."""
        self.time_entry_id = ''
        self.project_id = ''
        self.project_name = ''
        self.task_id = ''
        self.task_name = '' 
        self.user_id = ''
        self.user_name = ''
        self.is_current_user = None
        self.log_date = ''
        self.begin_time = ''
        self.end_time = ''
        self.log_time = ''
        self.billed_status = ''
        self.notes = ''
        self.time_started_at = ''
        self.timer_duration_in_minutes = 0
        self.created_time = ''
        self.customer_id = ''
        self.customer_name = ''
        self.start_timer = None

    def set_start_timer(self, start_timer):
        """Set start timer.

        Args:
            start_timer(bool): Start timer.

        """
        self.start_timer = start_timer

    def get_start_timer(self):
        """Get start timer.

        Returns:
            bool: Start timer.

        """
        return self.start_timer
     
    def set_time_entry_id(self, time_entry_id):
        """Set time entry id.

        Args:
            time_entry_id(str): Time entry id.

        """
        self.time_entry_id = time_entry_id

    def get_time_entry_id(self):
        """Get time entry id.

        Returns:
            str: Time entry id.

        """
        return self.time_entry_id

    def set_project_id(self, project_id):
        """Set project id.

        Args:
            project_id(str): Project id.

        """
        self.project_id = project_id

    def get_project_id(self):
        """Get project id.

        Returns:
            str: Project id.

        """
        return self.project_id

    def set_project_name(self, project_name):
        """Set project name.

        Args:
            project_name(str):Project name.

        """
        self.project_name = project_name

    def get_project_name(self):
        """Get project name.

        Returns:  
            str: Project name.

        """
        return self.project_name

    def set_task_id(self, task_id):
        """Set task id.

        Args: 
            task_id(str): Task id.

        """
        self.task_id = task_id

    def get_task_id(self):
        """Get task id.

        Returns:
            str: Task id.

        """
        return self.task_id

    def set_task_name(self, task_name):
        """Set task name.

        Args:
            task_name(str): Task name.

        """
        self.task_name = task_name

    def get_task_name(self):
        """Get task name.

        Returns:
            str: Task name.

        """
        return self.task_name

    def set_user_id(self, user_id):
        """Set user id.

        Args:
            user_id(str): User id.
 
        """ 
        self.user_id = user_id

    def get_user_id(self):
        """Get user id.

        Returns:
            str: User id.

        """
        return self.user_id

    def set_user_name(self, user_name):
        """Set user name.

        Args:
            user_name(str): User name.

        """
        self.user_name = user_name

    def get_user_name(self):
        """Get user name.

        Returns:
            str: User name.
 
        """
        return self.user_name

    def set_is_current_user(self, is_current_user): 
        """Set whether it is current user or not.

        Args:
            is_current_user(bool): True if it is a current user else false.

        """
        self.is_current_user = is_current_user

    def get_is_current_user(self):
        """Get whether it is current user or not.

        Returns:
            bool: True if it is current user else False.

        """
        return self.is_current_user

    def set_log_date(self, log_date):
        """Set log date.

        Args:
            log_date(str): Log date.

        """
        self.log_date = log_date

    def get_log_date(self):
        """Get log date.

        Returns:
            str: Log date.

        """
        return self.log_date

    def set_begin_time(self, begin_time):
        """Set begin time.

        Args:
            begin_time(str): Begin time.

        """
        self.begin_time = begin_time

    def get_begin_time(self):
        """Get begin time.
 
        Returns:
            str: Begin time.

        """
        return self.begin_time

    def set_end_time(self, end_time):
        """Set end time.

        Args:
            end_time(str): End time.

        """
        self.end_time = end_time

    def get_end_time(self):
        """Get end time.

        Returns:
            str: End time

        """
        return self.end_time

    def set_log_time(self, log_time):
        """Set log time.

        Args:
            log_time(str): Log time.
 
        """
        self.log_time = log_time

    def get_log_time(self):
        """Get log time.

        Returns:
            str: Log time.

        """
        return self.log_time

    def set_billed_status(self, billed_status):
        """Set billed status.

        Args:
            billed_status(str): Billed status.

        """
        self.billed_status = billed_status

    def get_billed_status(self):
        """Get billed status.

        Returns:
            str: Billed status.

        """
        return self.billed_status

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

    def set_timer_started_at(self, timer_started_at):
        """Set timer started at.

        Args:
            timer_started_at(str): Timer started at.

        """
        self.timer_started_at = timer_started_at

    def get_timer_started_at(self):
        """Get timer started at.

        Returns:
            str: Timer started at.

        """
        return self.timer_started_at

    def set_timer_duration_in_minutes(self, timer_duration_in_minutes):
        """Set timer duration in minutes.

        Args:
            timer_duration_in_minutes(int): Timer duration in minutes.

        """
        self.timer_duration_in_minutes = timer_duration_in_minutes

    def get_timer_duration_in_minutes(self):
        """Get timer duration in minutes.

        Returns:
            str: Timer duration in minutes.

        """
        return self.timer_duration_in_minutes

    def set_created_time(self, created_time):
        """Set created time.

        Args:
            created_time(str): Created time.

        """
        self.created_time = created_time

    def get_created_time(self):
        """Get created time.

        Returns:
            str: Created time.

        """
        return self.created_time

    def set_customer_id(self, customer_id):
        """Set customer id.

        Args:
            customer_id(str): Customer id.
 
        """
        self.customer_id = customer_id

    def get_customer_id(self):
        """Get customer id.

        Returns:
            str: Customer id.
 
        """
        return self.customer_id

    def set_customer_name(self, customer_name):
        """Set customer name.
  
        Args:
            customer_name(str): Customer name.
 
        """ 
        self.customer_name = customer_name

    def get_customer_name(self):
        """Get customer name.

        Returns: 
            str: Customer name.
 
        """
        return self.customer_name

    def to_json(self):
         """This method is used to convert time entry object to json format.

         Returns:
             dict: Dictionary containing json object for time entry.

         """
         data = {}
         if self.project_id != '':
             data['project_id'] = self.project_id
         if self.task_id != '':
             data['task_id'] = self.task_id
         if self.user_id != '':
             data['user_id'] = self.user_id
         if self.log_date != '': 
             data['log_date'] = self.log_date
         if self.begin_time != '':
             data['begin_time'] = self.begin_time
         if self.end_time != '':
             data['end_time'] = self.end_time
         if self.log_time != '':
             data['log_time'] = self.log_time
         if self.notes != '':
             data['notes'] = self.notes
         if self.start_timer != '':
             data['start_timer'] = self.start_timer
         return data
