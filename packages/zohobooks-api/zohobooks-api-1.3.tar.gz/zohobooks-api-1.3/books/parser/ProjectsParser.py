#$Id$#

from books.model.ProjectList import ProjectList
from books.model.Project import Project
from books.model.PageContext import PageContext
from books.model.TaskList import TaskList
from books.model.Task import Task
from books.model.User import User
from books.model.TimeEntryList import TimeEntryList
from books.model.TimeEntry import TimeEntry
from books.model.Comment import Comment
from books.model.InvoiceList import InvoiceList
from books.model.Invoice import Invoice
from books.model.UserList import UserList
from books.model.CommentList import CommentList

class ProjectsParser:
    """This class is used to parse the json object for Projects."""
  
    def get_projects_list(self, resp):
        """This method parses the given response and returns projects list 
            object.

        Args:
            resp(dict): Response containing json object for projects.

        Returns:
            instance: Projects list object.

        """
        projects_list = ProjectList()
        for value in resp['projects']:
            project = Project()
            project.set_project_id(value['project_id'])
            project.set_project_name(value['project_name'])
            project.set_customer_id(value['customer_id'])
            project.set_customer_name(value['customer_name'])
            project.set_description(value['description'])
            project.set_status(value['status'])
            project.set_billing_type(value['billing_type'])
            #project.set_rate(value['rate'])
            project.set_created_time(value['created_time'])
            projects_list.set_projects(project)
        page_context_obj = PageContext()
        page_context = resp['page_context']
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        projects_list.set_page_context(page_context_obj)
        return projects_list

    def get_project(self, resp):
        """This method parses the given response and returns projects object.

        Args:
            resp(dict): Dictionary containing json object for projects.

        Returns:
            instance: Projects object.

        """
        project_obj = Project()
        project = resp['project']
        project_obj.set_project_id(project['project_id'])
        project_obj.set_project_name(project['project_name'])
        project_obj.set_customer_id(project['customer_id'])
        project_obj.set_customer_name(project['customer_name'])
        project_obj.set_currency_code(project['currency_code'])
        project_obj.set_description(project['description'])
        project_obj.set_status(project['status'])
        project_obj.set_billing_type(project['billing_type'])
        project_obj.set_budget_type(project['budget_type'])
        project_obj.set_total_hours(project['total_hours'])
        project_obj.set_billed_hours(project['billed_hours'])
        project_obj.set_un_billed_hours(project['un_billed_hours'])
        project_obj.set_created_time(project['created_time'])
        for value in project['tasks']:
            task = Task()
            task.set_task_id(value['task_id'])
            task.set_task_name(value['task_name'])
            task.set_description(value['description'])
            task.set_rate(value['rate'])
            task.set_budget_hours(value['budget_hours'])
            task.set_total_hours(value['total_hours'])
            task.set_billed_hours(value['billed_hours'])
            task.set_un_billed_hours(value['un_billed_hours'])
            project_obj.set_tasks(task)
        for value in project['users']:
            user = User()
            user.set_user_id(value['user_id'])
            user.set_is_current_user(value['is_current_user'])
            user.set_user_name(value['user_name'])
            user.set_email(value['email'])
            user.set_user_role(value['user_role'])
            user.set_status(value['status'])
            user.set_rate(value['rate'])
            user.set_budget_hours(value['budget_hours'])
            user.set_total_hours(value['total_hours'])
            user.set_billed_hours(value['billed_hours'])
            user.set_un_billed_hours(value['un_billed_hours'])
            project_obj.set_users(user)
        return project_obj

    def get_message(self, resp):
        """This method parses the given response and returns string message.

        Args:
            resp(dict): Response containing json object for string message.

        Returns:
            str: Success message.

        """
        return resp['message']

    def get_tasks_list(self, resp):
        """This method parses the given response and returns tasks list object.

        Args:
            resp(dict): Response containing json object for tasks list.


        Returns:
            instance: Task list object.

        """
        task_list = TaskList()
        for value in resp['task']:
            task = Task()
            task.set_project_id(value['project_id'])
            task.set_task_id(value['task_id'])
            task.set_currency_id(value['currency_id'])  
            task.set_customer_id(value['customer_id'])
            task.set_task_name(value['task_name'])
            task.set_project_name(value['project_name'])
            task.set_customer_name(value['customer_name'])
            task.set_billed_hours(value['billed_hours'])
            task.set_log_time(value['log_time'])
            task.set_un_billed_hours(value['un_billed_hours'])
            task_list.set_tasks(task)     
        page_context_obj = PageContext()
        page_context = resp['page_context']
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        task_list.set_page_context(page_context_obj)
        return task_list

    def get_task(self, resp):
        """This method parses the given response and returns task object.

        Args:
            resp(dict): Response containing json object for task.

        Returns:
            instance: Task object.

        """
        task_obj = Task()
        task = resp['task']
        task_obj.set_project_id(task['project_id'])
        task_obj.set_project_name(task['project_name'])
        task_obj.set_task_id(task['task_id'])
        task_obj.set_task_name(task['task_name'])
        task_obj.set_description(task['description'])
        task_obj.set_rate(task['rate'])
        return task_obj

    def get_users(self, resp):
        """This method parses the given response and returns list of users 
            object.

        Args:
            resp(dict): Response containing json object for users list object.

        Returns: 
            instance: Users list object.

        """
        users = UserList()
        for value in resp['users']:
            user = User()
            user.set_user_id(value['user_id'])
            user.set_is_current_user(value['is_current_user'])
            user.set_user_name(value['user_name'])
            user.set_email(value['email'])
            user.set_user_role(value['user_role'])
            user.set_status(value['status'])
            user.set_rate(value['rate'])
            user.set_budget_hours(value['budget_hours'])
            users.set_users(user)
        return users

    def get_user(self, resp):
        """This method parses the given response and returns user object.

        Args:
            resp(dict): Response containing json object for user.

        Returns:
            instance: User object.

        """
        user_obj = User()
        user = resp['user']
        user_obj.set_project_id(user['project_id'])
        user_obj.set_user_id(user['user_id'])
        user_obj.set_is_current_user(user['is_current_user'])
        user_obj.set_user_name(user['user_name'])
        user_obj.set_email(user['email'])
        user_obj.set_user_role(user['user_role'])
        return user_obj

    def get_time_entries_list(self, resp):
        """This method parses the given response and returns time entries list 
            object.

        Args:
            resp(dict): Response containing json object for time entries.

        Returns:
            instance: Time entries list object.

        """
        time_entries_list = TimeEntryList()
        for value in resp['time_entries']:
            time_entry = TimeEntry()
            time_entry.set_time_entry_id(value['time_entry_id'])
            time_entry.set_project_id(value['project_id'])
            time_entry.set_project_name(value['project_name'])
            time_entry.set_customer_id(value['customer_id'])
            time_entry.set_customer_name(value['customer_name'])
            time_entry.set_task_id(value['task_id'])
            time_entry.set_task_name(value['task_name'])
            time_entry.set_user_id(value['user_id'])
            time_entry.set_is_current_user(value['is_current_user'])
            time_entry.set_user_name(value['user_name'])
            time_entry.set_log_date(value['log_date'])
            time_entry.set_begin_time(value['begin_time'])
            time_entry.set_end_time(value['end_time'])
            time_entry.set_log_time(value['log_time'])
            time_entry.set_billed_status(value['billed_status'])
            time_entry.set_notes(value['notes'])
            time_entry.set_timer_started_at(value['timer_started_at'])
            time_entry.set_timer_duration_in_minutes(value[\
            'timer_duration_in_minutes'])
            time_entry.set_created_time(value['created_time'])
            time_entries_list.set_time_entries(time_entry)
        page_context_obj = PageContext()
        page_context = resp['page_context']
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name']) 
        page_context_obj.set_applied_filter(page_context['applied_filter'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        time_entries_list.set_page_context(page_context_obj)
        return time_entries_list

    def get_time_entry(self, resp):
        """This method parses the given response and returns time entry object.

        Args:
            resp(dict):Response containing json object for time entry.

        Returns: 
            instance: Time entry object

        """
        time_entry = resp['time_entry']
        time_entry_obj = TimeEntry()
        time_entry_obj.set_time_entry_id(time_entry['time_entry_id'])
        time_entry_obj.set_project_id(time_entry['project_id'])
        time_entry_obj.set_project_name(time_entry['project_name'])
        time_entry_obj.set_task_id(time_entry['task_id'])
        time_entry_obj.set_task_name(time_entry['task_name'])
        time_entry_obj.set_user_id(time_entry['user_id'])
        time_entry_obj.set_user_name(time_entry['user_name'])
        time_entry_obj.set_is_current_user(time_entry['is_current_user'])
        time_entry_obj.set_log_date(time_entry['log_date'])
        time_entry_obj.set_begin_time(time_entry['begin_time'])
        time_entry_obj.set_end_time(time_entry['end_time'])
        time_entry_obj.set_log_time(time_entry['log_time'])
        time_entry_obj.set_billed_status(time_entry['billed_status'])
        time_entry_obj.set_notes(time_entry['notes'])
        time_entry_obj.set_timer_started_at(time_entry['timer_started_at'])
        time_entry_obj.set_timer_duration_in_minutes(time_entry[\
        'timer_duration_in_minutes'])
        time_entry_obj.set_created_time(time_entry['created_time'])
        return time_entry_obj

    def get_comments(self, resp):
        """This method parses the given response and returns comments list 
            object.

        Args: 
            resp(dict): Response containing json object for comments list.

        Returns:
            list of instance: Comments list object.

        """
        comments = CommentList()
        for value in resp['comments']:
            comment = Comment()
            comment.set_comment_id(value['comment_id'])
            comment.set_project_id(value['project_id'])
            comment.set_description(value['description'])
            comment.set_commented_by_id(value['commented_by_id'])
            comment.set_commented_by(value['commented_by'])
            comment.set_is_current_user(value['is_current_user'])
            comment.set_date(value['date'])
            comment.set_date_description(value['date_description'])
            comment.set_time(value['time'])
            comments.set_comments(comment)
        return comments

    def get_comment(self, resp):
        """This method parses the given response and returns comment object.

        Args:
            resp(dict): Response containing json object for comment object.

        Returns: 
            instance: Comment object.

        """
        comment = resp['comment'] 
        comment_obj = Comment()
        comment_obj.set_comment_id(comment['comment_id'])
        comment_obj.set_project_id(comment['project_id'])
        comment_obj.set_description(comment['description'])
        comment_obj.set_commented_by_id(comment['commented_by_id'])
        comment_obj.set_commented_by(comment['commented_by'])
        comment_obj.set_date(comment['date'])
        comment_obj.set_date_description(comment['date_description'])
        comment_obj.set_time(comment['time'])
        return comment_obj

    def get_invoice_list(self, resp):
        """This method parses the given response and returns invoice list 
            object.

        Args:
            resp(dict): Response containing json object for invoice list 
                object.

        Returns:
            instance: Invoice list object.

        """
        invoices = InvoiceList()
        for value in resp['invoices']:
            invoice = Invoice()
            invoice.set_invoice_id(value['invoice_id'])
            invoice.set_customer_name(value['customer_name'])
            invoice.set_customer_id(value['customer_id'])
            invoice.set_status(value['status'])
            invoice.set_invoice_number(value['invoice_number'])
            invoice.set_reference_number(value['reference_number'])
            invoice.set_date(value['date'])
            invoice.set_due_date(value['due_date'])
            invoice.set_total(value['total'])
            invoice.set_balance(value['balance'])
            invoice.set_created_time(value['created_time'])
            invoices.set_invoices(invoice)
        page_context = resp['page_context']
        page_context_obj = PageContext()
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        invoices.set_page_context(page_context)
        return invoices

       
    
