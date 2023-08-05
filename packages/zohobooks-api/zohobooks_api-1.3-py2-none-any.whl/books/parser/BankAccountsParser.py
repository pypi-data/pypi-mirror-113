#$Id$#

from books.model.BankAccount import BankAccount
from books.model.BankAccountList import BankAccountList
from books.model.Transaction import Transaction
from books.model.Statement import Statement
from books.model.PageContext import PageContext

class BankAccountsParser:
    """This class is used to parse the json response for Bank accounts."""
  
    def get_list(self, resp):
        """This method parses the given response and returns bank account list 
            object.

        Args:
            resp(dict): Response containing json object for Bank account list.

        Returns:
            instance: Bank account list object.

        """
        bank_account_list = BankAccountList()
        for value in resp['bankaccounts']:
            bank_accounts = BankAccount()
            bank_accounts.set_account_id(value['account_id'])
            bank_accounts.set_account_name(value['account_name'])
            bank_accounts.set_currency_id(value['currency_id'])
            bank_accounts.set_currency_code(value['currency_code'])
            bank_accounts.set_account_type(value['account_type'])
            bank_accounts.set_uncategorized_transactions(\
            value['uncategorized_transactions'])
            bank_accounts.set_is_active(value['is_active'])
            bank_accounts.set_balance(value['balance'])
            bank_accounts.set_bank_name(value['bank_name'])
            bank_accounts.set_routing_number(value['routing_number'])
            bank_accounts.set_is_primary_account(value['is_primary_account'])
            bank_accounts.set_is_paypal_account(value['is_paypal_account'])
            if value['is_paypal_account']:
                bank_accounts.set_paypal_email_address(\
                value['paypal_email_address'])
            bank_account_list.set_bank_accounts(bank_accounts)
        page_context_obj = PageContext()
        page_context = resp['page_context']
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_applied_filter(page_context['applied_filter'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        bank_account_list.set_page_context(page_context_obj)
        return bank_account_list

    def get_account_details(self, resp):
        """This method parses the given response and returns bank account 
            object. 

        Args:
            resp(dict): Response containing json object for bank accounts.

        Returns:
            instance: Bank accounts object.

        Raises: 
            Books Exception: If status is not '200' or '201'.

        """
        bank_account = resp['bankaccount']
        bank_account_obj = BankAccount()
        bank_account_obj.set_account_id(bank_account['account_id'])
        bank_account_obj.set_account_name(bank_account['account_name'])
        bank_account_obj.set_currency_id(bank_account['currency_id'])
        bank_account_obj.set_currency_code(bank_account['currency_code'])
        bank_account_obj.set_account_type(bank_account['account_type'])
        bank_account_obj.set_account_number(bank_account['account_number'])
        bank_account_obj.set_uncategorized_transactions(\
        bank_account['uncategorized_transactions'])
        bank_account_obj.set_is_active(bank_account['is_active'])
        bank_account_obj.set_balance(bank_account['balance'])
        bank_account_obj.set_bank_name(bank_account['bank_name'])
        bank_account_obj.set_routing_number(bank_account['routing_number'])
        bank_account_obj.set_is_primary_account(bank_account[\
        'is_primary_account'])
        bank_account_obj.set_is_paypal_account(bank_account[\
        'is_paypal_account'])
        if bank_account['is_paypal_account']:
            bank_account_obj.set_paypal_email_address(\
            bank_account['paypal_email_address'])
        bank_account_obj.set_description(bank_account['description'])
        return bank_account_obj

    def get_message(self, resp):
        """This message parses the given response and returns message string.
    
        Args:
            resp(dict): Response containing json object for message.

        Returns:
            str: Success message.

        """
        return resp['message']

    def get_statement(self, resp):
        """This method parses the given response and returns statement object.

        Args:
            resp(dict): Response containing json onbject for statement.

        Returns: 
            instance: Statement object.

        """
        statement = resp['statement']
        statement_obj = Statement()
        statement_obj.set_statement_id(statement['statement_id'])
        statement_obj.set_from_date(statement['from_date'])
        statement_obj.set_to_date(statement['to_date'])
        statement_obj.set_source(statement['source'])
        for value in statement['transactions']:
            transactions = Transaction()
            transactions.set_transaction_id(value['transaction_id'])
            transactions.set_debit_or_credit(value['debit_or_credit'])
            transactions.set_date(value['date'])
            transactions.set_customer_id(value['customer_id'])
            transactions.set_payee(value['payee'])
            transactions.set_reference_number(value['reference_number'])
            transactions.set_amount(value['amount'])
            transactions.set_status(value['status'])
            statement_obj.set_transactions(transactions)
        page_context = resp['page_context']
        page_context_obj = PageContext()
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        statement_obj.set_page_context(page_context_obj)
        return statement_obj
        
            
