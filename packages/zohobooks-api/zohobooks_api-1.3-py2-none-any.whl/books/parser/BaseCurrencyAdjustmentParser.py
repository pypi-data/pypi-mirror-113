#$Id$#

from books.model.BaseCurrencyAdjustment import BaseCurrencyAdjustment
from books.model.BaseCurrencyAdjustmentList import BaseCurrencyAdjustmentList
from books.model.PageContext import PageContext
from books.model.Account import Account

class BaseCurrencyAdjustmentParser: 
    """This class is used to parse the json object for Base Currency 
        adjustment Api."""

    def get_list(self, resp):
        """This method parses the given response and returns base currency 
            adjustment list object.

        Args:
            resp(dict): Response containing json for base currency adjustments 
                list.

        Returns:
            instance: Base currency list object.

        """
        base_currency_adjustment_list = BaseCurrencyAdjustmentList()
        for value in resp['base_currency_adjustments']:
            base_currency_adjustment = BaseCurrencyAdjustment()
            base_currency_adjustment.set_base_currency_adjustment_id(\
            value['base_currency_adjustment_id'])
            base_currency_adjustment.set_adjustment_date(value[\
            'adjustment_date'])
            base_currency_adjustment.set_exchange_rate(value['exchange_rate'])
            base_currency_adjustment.set_currency_id(value['currency_id'])
            base_currency_adjustment.set_currency_code(value['currency_code'])
            base_currency_adjustment.set_notes(value['notes'])
            base_currency_adjustment.set_gain_or_loss(value['gain_or_loss'])
            base_currency_adjustment_list.set_base_currency_adjustments(\
            base_currency_adjustment)
        page_context = resp['page_context']
        page_context_obj = PageContext()
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_applied_filter(page_context['applied_filter'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        base_currency_adjustment_list.set_page_context(page_context_obj)
        return base_currency_adjustment_list

    def get_base_currency_adjustment(self, resp):
        """This method parses the given response and returns the base currency 
            adjustment details object.

        Args:
            resp(dict): Response containing json object for base currency 
                adjustment.

        Returns:
            instance: Base currency adjustment object.

        """
        data = resp['data']
        base_currency_adjustment = BaseCurrencyAdjustment()
        base_currency_adjustment.set_base_currency_adjustment_id(data[\
        'base_currency_adjustment_id']) 
        base_currency_adjustment.set_currency_id(data['currency_id'])
        base_currency_adjustment.set_currency_code(data['currency_code'])
        base_currency_adjustment.set_adjustment_date(data['adjustment_date'])
        base_currency_adjustment.set_exchange_rate(data['exchange_rate'])
        base_currency_adjustment.set_notes(data['notes'])
        for value in data['accounts']:
            account = Account()
            account.set_account_id(value['account_id'])
            account.set_account_name(value['account_name'])
            account.set_bcy_balance(value['bcy_balance'])
            account.set_fcy_balance(value['fcy_balance'])
            account.set_adjusted_balance(value['adjusted_balance'])
            account.set_gain_or_loss(value['gain_or_loss'])
            account.set_gl_specific_type(value['gl_specific_type'])
            base_currency_adjustment.set_accounts(account)
        return base_currency_adjustment

    def list_account_details(self, resp):
        """This method parses the given response and returns list of account 
            details for base currency adjustment.

        Args:
            resp(dict): Response containing json object for account details list.

        Returns:
            instance: Base currency adjustment object.

        """
        data = resp['data']
        base_currency_adjustment = BaseCurrencyAdjustment()
        base_currency_adjustment.set_adjustment_date(data['adjustment_date'])
        base_currency_adjustment.set_adjustment_date_formatted(data[\
        'adjustment_date_formatted'])
        base_currency_adjustment.set_exchange_rate(data['exchange_rate'])
        base_currency_adjustment.set_exchange_rate_formatted(data[\
        'exchange_rate_formatted'])
        base_currency_adjustment.set_currency_id(data['currency_id'])
        for value in data['accounts']:
            accounts = Account()
            accounts.set_account_id(value['account_id'])
            accounts.set_account_name(value['account_name'])
            accounts.set_gl_specific_type(value['gl_specific_type'])
            accounts.set_fcy_balance(value['fcy_balance'])
            accounts.set_fcy_balance_formatted(value['fcy_balance_formatted'])
            accounts.set_bcy_balance(value['bcy_balance'])
            accounts.set_bcy_balance_formatted(value['bcy_balance_formatted'])
            accounts.set_adjusted_balance(value['adjusted_balance'])
            accounts.set_adjusted_balance_formatted(value[\
            'adjusted_balance_formatted'])
            accounts.set_gain_or_loss(value['gain_or_loss'])
            accounts.set_gain_or_loss_formatted(value['gain_or_loss_formatted'])
            base_currency_adjustment.set_accounts(accounts)
        base_currency_adjustment.set_notes(data['notes'])
        base_currency_adjustment.set_currency_code(data['currency_code'])
        return base_currency_adjustment

    def get_message(self, resp): 
        """This method parses the given response and returns message.

        Args:
            resp(dict): Response containing json object for message.

        Returns:
            str: Success message.

        """
        return resp['message']
