#$Id$#

from books.model.Expense import Expense
from books.model.ExpenseList import ExpenseList
from books.model.Comment import Comment
from books.model.PageContext import PageContext
from books.model.CommentList import CommentList

class ExpensesParser:
    """This class is used to parse the json for Expenses."""
     
    def get_list(self, resp): 
        """This method parses the given response and returns Expense list 
            object.

        Args:
            resp(dict): Response containing json object for Expenses list.
        
        Returns:
            instance: Expenses list object.

        """
        expenses = resp['expenses']
        expense_list = ExpenseList()
        for value in expenses:
            expense = Expense()
            expense.set_expense_id(value['expense_id'])
            expense.set_date(value['date'])
            expense.set_account_name(value['account_name'])
            expense.set_paid_through_account_name(value[\
            'paid_through_account_name'])
            expense.set_description(value['description'])
            expense.set_currency_id(value['currency_id'])
            expense.set_currency_code(value['currency_code'])
            expense.set_bcy_total(value['bcy_total'])
            expense.set_total(value['total'])
            expense.set_is_billable(value['is_billable'])
            expense.set_reference_number(value['reference_number'])
            expense.set_customer_id(value['customer_id'])
            expense.set_customer_name(value['customer_name'])
            expense.set_vendor_id(value['vendor_id'])
            expense.set_vendor_name(value['vendor_name'])
            expense.set_status(value['status'])
            expense.set_created_time(value['created_time'])
            expense.set_expense_receipt_name(value['expense_receipt_name'])
            expense_list.set_expenses(expense)
        page_context_obj = PageContext()
        page_context = resp['page_context']
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_applied_filter(page_context['applied_filter'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        expense_list.set_page_context(page_context)

        return expense_list

    def get_expense(self, resp):  
        """This method parses the given response and returns expense object.

        Args:
            resp(dict): Response containing json object for expense.

        Returns:
            instance: Expense object.

        """
        expense = resp['expense']
        expense_obj = Expense()
        expense_obj.set_expense_id(expense['expense_id'])
        expense_obj.set_expense_item_id(expense['expense_item_id'])
        expense_obj.set_account_id(expense['account_id'])
        expense_obj.set_account_name(expense['account_name'])
        expense_obj.set_paid_through_account_id(expense[\
        'paid_through_account_id'])
        expense_obj.set_paid_through_account_name(expense[\
        'paid_through_account_name'])
        expense_obj.set_vendor_id(expense['vendor_id'])
        expense_obj.set_vendor_name(expense['vendor_name'])
        expense_obj.set_date(expense['date'])
        expense_obj.set_tax_id(expense['tax_id'])
        expense_obj.set_tax_name(expense['tax_name'])
        expense_obj.set_tax_percentage(expense['tax_percentage'])
        expense_obj.set_currency_id(expense['currency_id'])
        expense_obj.set_currency_code(expense['currency_code'])
        expense_obj.set_exchange_rate(expense['exchange_rate'])
        expense_obj.set_tax_amount(expense['tax_amount'])
        expense_obj.set_sub_total(expense['sub_total'])
        expense_obj.set_total(expense['total'])
        expense_obj.set_bcy_total(expense['bcy_total'])
        expense_obj.set_amount(expense['amount'])
        expense_obj.set_is_inclusive_tax(expense['is_inclusive_tax'])
        expense_obj.set_reference_number(expense['reference_number'])
        expense_obj.set_description(expense['description'])
        expense_obj.set_is_billable(expense['is_billable'])
        expense_obj.set_customer_id(expense['customer_id'])
        expense_obj.set_customer_name(expense['customer_name'])
        expense_obj.set_expense_receipt_name(expense['expense_receipt_name'])
        expense_obj.set_created_time(expense['created_time'])
        expense_obj.set_last_modified_time(expense['last_modified_time'])
        expense_obj.set_status(expense['status'])
        expense_obj.set_invoice_id(expense['invoice_id'])
        expense_obj.set_invoice_number(expense['invoice_number'])
        expense_obj.set_project_id(expense['project_id'])
        expense_obj.set_project_name(expense['project_name'])
        return expense_obj

    def get_message(self, resp):
        """This method parses the given json string and returns string message.

        Args:
            resp(dict): Response containing json object for success message.

        Returns:
            str: Success message.

        """
        return resp['message']

    def get_comments(self, resp):
        """This method parses the given json string and returns comments list.

        Args:
            resp(dict): Response containing json object for comments.

        Returns:
            instance: Comments list object.

        """
        comments = CommentList()
        for value in resp['comments']:
            comment = Comment()
            comment.set_comment_id(value['comment_id'])
            comment.set_expense_id(value['expense_id'])
            comment.set_description(value['description'])
            comment.set_commented_by_id(value['commented_by_id'])
            comment.set_commented_by(value['commented_by'])
            comment.set_date(value['date'])
            comment.set_date_description(value['date_description'])
            comment.set_time(value['time'])
            comment.set_operation_type(value['operation_type'])
            comment.set_transaction_id(value['transaction_id'])
            comment.set_transaction_type(value['transaction_type'])
            comments.set_comments(comment)
        return comments
