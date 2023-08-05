#$Id$

class User:
    """This class is used to create object for Users."""
    def __init__(self):
        """Initialize parameters for Users object."""
        self.user_id = ''
        self.is_current_user = None
        self.user_name = ''
        self.email = ''
        self.user_role = ''
        self.status = ''
        self.rate = 0.0
        self.budget_hours = 0
        self.total_hours = ''
        self.billed_hours = ''
        self.un_billed_hours = ''
        self.project_id = ''
        self.created_time = ''
        self.email_ids = []
        self.role_id = ''
        self.name = ''
        self.photo_url = ''
    
    def set_photo_url(self, photo_url):
        """Set photo url.

        Args:
            photo_url(str): Photo url.

        """
        self.photo_url = photo_url

    def get_photo_url(self):
        """Get photo url.

        Returns:
            str: Photo url.

        """
        return self.photo_url

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

    def set_is_current_user(self, is_current_user):
        """Set whether it is current user or not.

        Args:
            is_current_user(bool): True if it is current user else False.

        """
        self.is_current_user = is_current_user

    def get_is_current_user(self):
        """Get whether it is current user.

        Returns:
            bool: True if it is a current user else False.

        """
        return self.is_current_user

    def set_user_name(self, user_name): 
        """Set user name.

        Args:
            user_name(str): User name.

        """
        self.user_name = user_name

    def get_user_name(self):
        """Get user name.

        Returns:
            str: User name

        """
        return self.user_name

    def set_email(self, email):
        """Set email.

        Args:
            email(str): Email.

        """
        self.email = email

    def get_email(self):
        """Get email.

        Returns:
            str: Email.

        """
        return self.email

    def set_user_role(self, user_role):
        """Set user role.

        Args:
            user_role(str): User role.

        """
        self.user_role = user_role

    def get_user_role(self):
        """Get user role.

        Returns:
            str: User role.

        """
        return self.user_role

    def set_status(self, status):
        """Set status.

        Args:
            status(str): Status.

        """
        self.status = status

    def get_status(self):
        """Get status.

        Returns:
            str: Status.

        """ 
        return self.status

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
        """Get budget hours.

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

        Returns:
            str: Billed hours.

        """
        return self.billed_hours

    def set_status(self, status): 
        """Set status.

        Args: 
            status(str): Status.

        """
        self.status = status

    def get_status(self):
        """Get status.

        Returns:
            str: Status.

        """
        return self.status

    def set_rate(self, rate):
        """Set rate.
        
        Args:
            rate(float): Rate

        """
        self.rate = rate

    def get_rate(self):
        """Get rate.

        Returns:
            float: Rate.

        """
        return self.rate

    def budget_hours(self, budget_hours):
        """Set budget hours.

        Args:
            budget_hours(str): Budget hours.

        """
        self.budget_hours = budget_hours

    def get_budget_hours(self):
        """Get budget hours.

        Returns:
            str: Budget hours.

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

        Returns:
            str: Billed hours.

        """ 
        return self.billed_hours

    def set_un_billed_hours(self, un_billed_hours):
        """Set unbilled hours.

        Args:
            un_billed_hours(str): Un billed hours.

        """
        self.un_billed_hours = un_billed_hours

    def get_un_billed_hours(self):
        """Get unbilled hours.

        Returns:
            str: Unbilled hours.

        """ 
        return self.un_billed_hours

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

    def set_email_ids(self, email_ids):
        """Set email ids.

        Args:
            email_ids(instance): Email ids object.

        """
        self.email_ids = email_ids

    def get_email_ids(self):
        """Get email ids.
 
        Returns:
            list of instance: list of Email ids object.

        """ 
        return self.email_ids

    def set_role_id(self, role_id):
        """Set role id.

        Args:
            role_id(str): Role id.

        """
        self.role_id = role_id

    def get_role_id(self):
        """Get role id.

        Returns:
            str: Role id.

        """
        return self.role_id

    def to_json(self):
        """This method is used to convert user object to json format.

        Returns:
            dict: Dictionary containing json object for user.

        """
        data = {}
        if self.user_id != '':
            data['user_id'] = self.user_id
        if self.rate > 0:
            data['rate'] = self.rate
        if self.budget_hours > 0:
            data['budget_hours'] = self.budget_hours
        if self.user_name != '':
            data['user_name'] = self.user_name
        if self.email != '':
            data['email'] = self.email
        if self.user_role != '':
            data['user_role'] = self.user_role
        if self.name != '':
            data['name'] = self.name
        return data
        
