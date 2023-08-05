#$Id$

class Task: 
    """This class is used to create object for tasks."""
    def __init__(self): 
        """Initialize parameters for tasks object."""
        self.task_id = ''
        self.task_name = ''
        self.description = ''
        self.rate = 0.0
        self.budget_hours = 0
        self.total_hours = ''
        self.billed_hours= ''
        self.unbilled_hours = ''
        self.project_id = ''
        self.project_name = ''
        self.currency_id = ''
        self.customer_id = ''
        self.customer_name = ''
        self.log_time = ''

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

    def set_description(self, description):
        """Set description.

        Args:
            description(str): Description.

        """
        self.description = description

    def get_description(self):
        """Get description

        Returns:
            str: Description.

        """
        return self.description
    
    def set_rate(self, rate):
        """Set rate.
 
        Args:
            rate(float): Rate.

        """
        self.rate = rate

    def get_rate(self):
        """Get rate.

        Returns:
            float: Rate.

        """
        return self.rate

    def set_budget_hours(self, budget_hours):
        """Set budget hours.

        Args:
            budget_hours(int): Budget hours.

        """
        self.budget_hours = budget_hours

    def get_budget_hours(self):
        """Get budget_hours.

        Returns:
            int: Budget hours.

        """
        return self.budget_hours

    def set_total_hours(self, total_hours):
        """Set total hours.

        Args:
            total_hours(str): Total hours.

        """
        self.total_hours = total_hours
 
    def get_total_hours(self):
        """Get total hours.

        Returns:
            str: Total hours.

        """
        return self.total_hours

    def set_billed_hours(self, billed_hours):
        """Set billed hours.
 
        Args:
            billed_hours(str): Billed hours.

        """
        self.billed_hours = billed_hours

    def get_billed_hours(self):
        """Get billed hours.

        Args:
            str: billed hours.

        """
        return self.billed_hours

    def set_un_billed_hours(self, un_billed_hours):
        """Set unbilled hours.
       
        Args:
            un_billed_hours(str): Unbilled hours.

        """
        self.un_billed_hours = un_billed_hours

    def get_un_billed_hours(self):
        """Get unbilled hours.

        Returns: 
            str: Unbilled hours.

        """
        return self.un_billed_hours
 
    def set_project_id(self, project_id):
        """Set project_id.

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
            project_name(str): Project name.

        """
        self.project_name = project_name

    def get_project_name(self):
        """Get project name.

        Returns:
            str: Project name.

        """
        return self.project_name

    def set_currency_id(self, currency_id):
        """Set currency id.

        Args:
            currency_id(str): Currency id.

        """
        self.currency_id = currency_id

    def get_currency_id(self):
        """Get currency id.

        Returns:
            str: Currency id.

        """
        return self.currency_id

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

    def to_json(self):
        """This method is used to convert task object to jsno format.

        Returns:
            dict: Dictionary containing json object for task.

        """
        data = {}
        if self.task_name != '':
            data['task_name'] = self.task_name
        if self.description != '':
            data['description'] = self.description
        if self.rate > 0:
            data['rate'] = self.rate
        if self.budget_hours > 0:
            data['budget_hours'] = self.budget_hours
        return data
