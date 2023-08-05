#$Id$#

from books.model.ChartOfAccount import ChartOfAccount
from books.model.ChartOfAccountList import ChartOfAccountList
from books.model.TransactionList import TransactionList
from books.model.Transaction import Transaction
from books.model.PageContext import PageContext

class ChartOfAccountsParser:
    """This class parses the json response for chart of accounts."""

    def get_list(self, resp):
        """This method parses the given response and returns chart of accounts 
            list.

        Args:
            resp(dict): Dictionary containing json object for chart of accounts 
                list.

        Returns: 
            instance: Chart of accounts list object.

        """
        chart_of_accounts_list = ChartOfAccountList()
        for value in resp['chartofaccounts']:
            chart_of_accounts = ChartOfAccount()
            chart_of_accounts.set_account_id(value['account_id'])
            chart_of_accounts.set_account_name(value['account_name'])
            chart_of_accounts.set_account_type(value['account_type'])
            chart_of_accounts.set_is_active(value['is_active'])
            chart_of_accounts.set_is_user_created(value['is_user_created'])
            chart_of_accounts.set_is_involved_in_transaction(value[\
            'is_involved_in_transaction'])
            chart_of_accounts.set_is_system_account(value['is_system_account'])
            chart_of_accounts_list.set_chartofaccounts(chart_of_accounts)
        page_context = resp['page_context']
        page_context_obj = PageContext()
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_applied_filter(page_context['applied_filter'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        chart_of_accounts_list.set_page_context(page_context_obj)
        return chart_of_accounts_list

    def get_account(self, resp):
        """This method parses the given response and returns chart of 
            accounts object.

        Args:
            resp(dict): Dictionary containing json object for chart of accounts.

        Returns:
            instance: Chart of accounts object.

        """
        chart_of_account = resp['chart_of_account']
        chart_of_account_obj = ChartOfAccount()
        chart_of_account_obj.set_account_id(chart_of_account['account_id'])
        chart_of_account_obj.set_account_name(chart_of_account['account_name']) 
        chart_of_account_obj.set_is_active(chart_of_account['is_active'])
        chart_of_account_obj.set_account_type(chart_of_account['account_type'])
        chart_of_account_obj.set_account_type_formatted(chart_of_account[\
        'account_type_formatted'])
        chart_of_account_obj.set_description(chart_of_account['description'])
        return chart_of_account_obj

    def get_message(self, resp):
        """This method parses the given response and returns string message.

        Args:
            reps(dict): Dictionary containing json object for message.

        Returns:
            str: Success message.

        """ 
        return resp['message']    

    def get_transactions_list(self, resp):
        """This method parses the given response and returns transactions list.

        Args:
            resp(dict): Dictionary containing json object for transactions list.

        Returns:
            instance: Transaction list object.

        """
        transactions_list = TransactionList()
        for value in resp['transactions']:
            transactions = Transaction()
            transactions.set_categorized_transaction_id(value[\
            'categorized_transaction_id'])
            transactions.set_transaction_type(value['transaction_type'])
            transactions.set_transaction_id(value['transaction_id'])
            transactions.set_transaction_date(value['transaction_date'])
            transactions.set_transaction_type_formatted(value[\
            'transaction_type_formatted'])
            transactions.set_account_id(value['account_id']) 
            transactions.set_customer_id(value['customer_id'])
            transactions.set_payee(value['payee'])
            transactions.set_description(value['description'])
            transactions.set_entry_number(value['entry_number'])
            transactions.set_currency_id(value['currency_id'])
            transactions.set_currency_code(value['currency_code'])
            transactions.set_debit_or_credit(value['debit_or_credit'])
            transactions.set_offset_account_name(value['offset_account_name'])
            transactions.set_reference_number(value['reference_number'])
            transactions.set_reconcile_status(value['reconcile_status'])
            transactions.set_debit_amount(value['debit_amount'])
            transactions.set_credit_amount(value['credit_amount'])
            transactions_list.set_transactions(transactions)
        page_context = resp['page_context']
        page_context_obj = PageContext()
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        transactions_list.set_page_context(page_context_obj)
        return transactions_list

       
