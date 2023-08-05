#$Id$#

from books.model.Transaction import Transaction
from books.model.TransactionList import TransactionList
from books.model.PageContext import PageContext
from books.model.Instrumentation import Instrumentation
from books.model.SearchCriteria import SearchCriteria

class BankTransactionsParser:
    """This class is used to parse the json response for Bank transactions."""
   
    def get_list(self, resp):
        """This method parses the given response and returns bank transaction 
            list.

        Args: 
            resp(dict): Response containing json object for Bank transaction 
                list.

        Returns:
            instance: Bank transaction list object.

        """
        bank_transaction_list = TransactionList()
        for value in resp['banktransactions']:
            bank_transaction = Transaction()
            bank_transaction.set_transaction_id(value['transaction_id'])
            bank_transaction.set_date(value['date'])
            bank_transaction.set_amount(value['amount']) 
            bank_transaction.set_transaction_type(value['transaction_type'])
            bank_transaction.set_status(value['status'])
            bank_transaction.set_source(value['source'])
            bank_transaction.set_account_id(value['account_id'])
            bank_transaction.set_customer_id(value['customer_id'])
            bank_transaction.set_payee(value['payee'])
            bank_transaction.set_currency_id(value['currency_id'])
            bank_transaction.set_currency_code(value['currency_code'])
            bank_transaction.set_debit_or_credit(value['debit_or_credit'])
            bank_transaction.set_offset_account_name(value['offset_account_name'])
            bank_transaction.set_reference_number(value['reference_number'])
            bank_transaction.set_imported_transaction_id(value[\
            'imported_transaction_id'])
            bank_transaction_list.set_transactions(bank_transaction)
        page_context_obj = PageContext()
        page_context = resp['page_context']
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_applied_filter(page_context['applied_filter'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        bank_transaction_list.set_page_context(page_context_obj)
        return bank_transaction_list

    def get_transaction(self, resp):
        """This method parses the given response and returns Bank Transaction 
            object.
      
        Args: 
            resp(dict): Response containing json object for Bank transaction.

        Returns:
            instance: Bank transaction object.

        """
        transactions = Transaction()
        bank_transaction = resp['banktransaction']
        transactions.set_transaction_id(bank_transaction['transaction_id'])
        transactions.set_from_account_id(bank_transaction['from_account_id'])
        transactions.set_from_account_name(bank_transaction[\
        'from_account_name'])
        transactions.set_to_account_id(bank_transaction['to_account_id'])
        transactions.set_to_account_name(bank_transaction['to_account_name'])
        transactions.set_transaction_type(bank_transaction['transaction_type'])
        transactions.set_currency_id(bank_transaction['transaction_type'])
        transactions.set_currency_code(bank_transaction['currency_code'])
        transactions.set_amount(bank_transaction['amount'])
        transactions.set_exchange_rate(bank_transaction['exchange_rate'])
        transactions.set_date(bank_transaction['date'])
        transactions.set_reference_number(bank_transaction['reference_number'])
        transactions.set_description(bank_transaction['description'])
        transactions.set_imported_transaction(bank_transaction[\
        'imported_transactions'])
        return transactions

    def get_message(self, resp):
        """This method parses the given response and returns message.

        Args:
            resp(dict): Response containing json object for message.

        Returns:
            str: Success message('The transaction hasbeen deleted.').

        """
        return resp['message']

    def get_matching_transaction(self, resp): 
        """This method parses the given response and returns matching 
            transactions list.
  
        Args: 
            resp(dict): Response containing json object for matching 
                transactions.

        Returns:
            instance: Transaction list object.

        """
        transaction_list = TransactionList()
        for value in resp['matching_transactions']:
            transaction = Transaction()
            transaction.set_transaction_id(value['transaction_id'])
            transaction.set_date(value['date'])
            transaction.set_date_formatted(value['date_formatted'] if 'date_formatted' in value else None)
            transaction.set_transaction_type(value['transaction_type'])
            transaction.set_transaction_type_formatted(value[\
            'transaction_type_formatted'] if 'transaction_type_formatted' in value else None)
            transaction.set_reference_number(value['reference_number'])
            transaction.set_amount(value['amount'])
            transaction.set_amount_formatted(value['amount_formatted'] if 'amount_formatted' in value else None)
            transaction.set_debit_or_credit(value['debit_or_credit'])
            transaction.is_best_match = value['is_best_match'] if 'is_best_match' in value else None
            transaction.offset_account_name = value['offset_account_name'] if 'offset_account_name' in value else None
            transaction_list.set_transactions(transaction)
        page_context_obj = PageContext()
        page_context = resp['page_context']
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        for value in page_context['search_criteria']:
            criteria = SearchCriteria()
            criteria.set_column_name(value['column_name'])
            if value['comparator'] != 'range':
                criteria.set_search_text(value['search_text'])
            else:
                criteria.set_search_text('{} -- {}'.format(value['search_text_0'], value['search_text_0']))
            criteria.set_comparator(value['comparator'])
            page_context_obj.set_search_criteria(criteria)
        transaction_list.set_page_context(page_context_obj)
        '''instrumentation_obj = Instrumentation()
        instrumentation = resp['instrumentation']
        instrumentation_obj.set_query_execution_time(instrumentation[\
        'query_execution_time'])
        instrumentation_obj.set_request_handling_time(instrumentation[\
        'request_handling_time'])
        instrumentation_obj.set_response_write_time(instrumentation[\
        'response_write_time'])
        instrumentation_obj.set_page_context_write_time(instrumentation[\
        'page_context_write_time'])
        transaction_list.set_instrumentation(instrumentation_obj)'''
        return transaction_list

    def get_associated_transaction(self, resp):
        """This method parses the given response and returns associated 
            transactions list.

        Args:
            resp(dict): Response containing json object for associated 
                transactions.

        Returns:
            instance: Transaction object.

        """
        transaction = resp['transaction']
        transaction_obj = Transaction()
        transaction_obj.set_imported_transaction_id(transaction[\
        'imported_transaction_id'])
        transaction_obj.set_date(transaction['date'])
        transaction_obj.set_amount(transaction['amount'])
        transaction_obj.set_payee(transaction['payee'])
        transaction_obj.set_reference_number(transaction['reference_number'])
        transaction_obj.set_description(transaction['description'])
        transaction_obj.set_status(transaction['status'])
        transaction_obj.set_status_formatted(transaction['status_formatted'])
        for value in transaction['associated_transactions']:
            transaction = Transaction() 
            transaction.set_transaction_id(value['transaction_id'])
            transaction.set_date(value['date'])
            transaction.set_debit_or_credit(value['debit_or_credit'])
            transaction.set_transaction_type(value['transaction_type'])
            transaction.set_amount(value['amount'])
            transaction.set_customer_id(value['customer_id'])
            transaction.set_customer_name(value['customer_name'])
            transaction_obj.set_associated_transaction(transaction)
        page_context_obj = PageContext()
        page_context = resp['page_context']
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        '''instrumentation_obj = Instrumentation()
        instrumentation = resp['instrumentation']
        instrumentation_obj.set_query_execution_time(instrumentation[\
        'query_execution_time'])
        instrumentation_obj.set_request_handling_time(instrumentation[\
        'request_handling_time'])
        instrumentation_obj.set_response_write_time(instrumentation[\
        'response_write_time'])
        instrumentation_obj.set_page_context_write_time(instrumentation[\
        'page_context_write_time'])
        transaction_obj.set_instrumentation(instrumentation_obj)'''
        return transaction_obj

    
            


