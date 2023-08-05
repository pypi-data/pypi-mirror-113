#$Id$#

from books.model.RecurringExpense import RecurringExpense
from books.model.RecurringExpenseList import RecurringExpenseList
from books.model.Expense import Expense
from books.model.ExpenseList import ExpenseList
from books.model.Comment import Comment
from books.model.PageContext import PageContext
from books.model.CommentList import CommentList

class RecurringExpensesParser:
    """This class is used to parse the json for recurring expenses. """
    
    def get_list(self, resp):
        """This method parses the given response and returns recurring 
            expenses list object.

        Args:
            resp(dict): Response containing json object for recurring expenses 
                list.

        Returns:
            instance: Recurring expenses list object.

        """
        recurring_expenses_list = RecurringExpenseList()
        for value in resp['recurring_expenses']:
            recurring_expenses = RecurringExpense()
            recurring_expenses.set_recurring_expense_id(\
            value['recurring_expense_id'])
            recurring_expenses.set_recurrence_name(value['recurrence_name'])
            recurring_expenses.set_recurrence_frequency(\
            value['recurrence_frequency'])
            recurring_expenses.set_repeat_every(value['repeat_every'])
            recurring_expenses.set_last_created_date(\
            value['last_created_date'])
            recurring_expenses.set_next_expense_date(\
            value['next_expense_date'])
            recurring_expenses.set_account_name(value['account_name'])
            recurring_expenses.set_paid_through_account_name(\
            value['paid_through_account_name'])
            recurring_expenses.set_description(value['description'])
            recurring_expenses.set_currency_id(value['currency_id'])
            recurring_expenses.set_currency_code(value['currency_code'])
            recurring_expenses.set_total(value['total'])
            recurring_expenses.set_is_billable(value['is_billable'])
            recurring_expenses.set_customer_name(value['customer_name'])
            recurring_expenses.set_vendor_name(value['vendor_name'])
            recurring_expenses.set_status(value['status'])
            recurring_expenses.set_created_time(value['created_time'])
            recurring_expenses_list.set_recurring_expenses(recurring_expenses)
        page_context = resp['page_context']
        page_context_obj = PageContext()
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_applied_filter(page_context['applied_filter'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        recurring_expenses_list.set_page_context(page_context_obj)
        return recurring_expenses_list

    def get_recurring_expense(self, resp):
        """This method parses the given response and returns recurring 
            expenses object.

        Args:
            resp(dict): Response containing json object for recurring expenses.

        Returns:
            instance: Recurring expenses object.

        """
        recurring_expense = resp['recurring_expense']
        recurring_expense_obj = RecurringExpense()
        recurring_expense_obj.set_recurring_expense_id(\
        recurring_expense['recurring_expense_id'])
        recurring_expense_obj.set_recurrence_name(\
        recurring_expense['recurrence_name'])
        recurring_expense_obj.set_start_date(recurring_expense['start_date'])
        recurring_expense_obj.set_end_date(recurring_expense['end_date'])
        recurring_expense_obj.set_recurrence_frequency(\
        recurring_expense['recurrence_frequency'])
        recurring_expense_obj.set_repeat_every(\
        recurring_expense['repeat_every'])
        recurring_expense_obj.set_last_created_date(\
        recurring_expense['last_created_date'])
        recurring_expense_obj.set_next_expense_date(\
        recurring_expense['next_expense_date'])
        recurring_expense_obj.set_account_id(recurring_expense['account_id'])
        recurring_expense_obj.set_account_name(\
        recurring_expense['account_name'])
        recurring_expense_obj.set_paid_through_account_id(\
        recurring_expense['paid_through_account_id'])
        recurring_expense_obj.set_paid_through_account_name(\
        recurring_expense['paid_through_account_name'])
        recurring_expense_obj.set_vendor_id(recurring_expense['vendor_id'])
        recurring_expense_obj.set_vendor_name(recurring_expense['vendor_name'])
        recurring_expense_obj.set_currency_id(recurring_expense['currency_id'])
        recurring_expense_obj.set_currency_code(\
        recurring_expense['currency_code'])
        recurring_expense_obj.set_exchange_rate(\
        recurring_expense['exchange_rate'])
        recurring_expense_obj.set_tax_id(recurring_expense['tax_id'])
        recurring_expense_obj.set_tax_name(recurring_expense['tax_name'])
        recurring_expense_obj.set_tax_percentage(\
        recurring_expense['tax_percentage'])
        recurring_expense_obj.set_tax_amount(recurring_expense['tax_amount'])
        recurring_expense_obj.set_sub_total(recurring_expense['sub_total'])
        recurring_expense_obj.set_total(recurring_expense['total'])
        recurring_expense_obj.set_bcy_total(recurring_expense['bcy_total'])
        recurring_expense_obj.set_amount(recurring_expense['amount'])
        recurring_expense_obj.set_description(recurring_expense['description'])
        recurring_expense_obj.set_is_inclusive_tax(\
        recurring_expense['is_inclusive_tax'])
        recurring_expense_obj.set_is_billable(recurring_expense['is_billable'])
        recurring_expense_obj.set_customer_id(recurring_expense['customer_id'])
        recurring_expense_obj.set_customer_name(\
        recurring_expense['customer_name'])
        recurring_expense_obj.set_status(recurring_expense['status'])
        recurring_expense_obj.set_created_time(\
        recurring_expense['created_time'])      
        recurring_expense_obj.set_last_modified_time(\
        recurring_expense['last_modified_time'])
        recurring_expense_obj.set_project_id(recurring_expense['project_id'])
        recurring_expense_obj.set_project_name(\
        recurring_expense['project_name'])
        return recurring_expense_obj

    def get_message(self, response):
        """This method parses the json object and returns the message string.

        Args:
            response(dict): Response containing json object for message.
 
        Returns:
            str: Success message.

        """
        return response['message']

    def get_expense_history(self, resp):
        """This method parses the json object and returns expense history list.

        Args:
            resp(dict): Response containing json object for expense history.

        Returns:
            instance: Expenses list object.

        """
        expenses_list = ExpenseList()
        for value in resp['expensehistory']:
            expense = Expense()
            expense.set_expense_id(value['expense_id'])
            expense.set_date(value['date'])
            expense.set_account_name(value['account_name'])
            expense.set_vendor_name(value['vendor_name'])
            expense.set_paid_through_account_name(\
            value['paid_through_account_name'])
            expense.set_customer_name(value['customer_name'])
            expense.set_total(value['total'])
            expense.set_status(value['status'])
            expenses_list.set_expenses(expense)
        page_context_obj = PageContext()
        page_context = resp['page_context']
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        expenses_list.set_page_context(page_context_obj)
        return expenses_list

    def get_comments(self, resp):
        """This method parses the given response and returns comments list.

        Args:
            resp(dict): Response containing comments list.

        Returns:
            instance: Comments List object.

        """
        comments_list = CommentList()
        for value in resp['comments']:
            comment = Comment()
            comment.set_comment_id(value['comment_id'])
            comment.set_recurring_expense_id(value['recurring_expense_id'])
            comment.set_description(value['description'])
            comment.set_commented_by_id(value['commented_by_id'])
            comment.set_commented_by(value['commented_by'])
            comment.set_date(value['date'])
            comment.set_date_description(value['date_description'])
            comment.set_time(value['time'])
            comment.set_operation_type(value['operation_type'])
            comment.set_transaction_id(value['transaction_id'])
            comment.set_transaction_type(value['transaction_type'])
            comments_list.set_comments(comment)
        return comments_list
