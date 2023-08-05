#$Id$#

from books.model.Journal import Journal
from books.model.JournalList import JournalList
from books.model.PageContext import PageContext
from books.model.LineItem import LineItem

class JournalsParser: 
    """This class is used to parse the given json for Jornals."""
   
    def get_list(self, resp): 
        """This method parses the given response for journals list.

        Args:
            journals(dict): Response containing json object for journals list.

        Returns:
            instance: Journals list object.

        """
        journals_list = JournalList()
        for value in resp['journals']:
            journal = Journal()
            journal.set_journal_id(value['journal_id'])
            journal.set_journal_date(value['journal_date'])
            journal.set_entry_number(value['entry_number'])
            journal.set_reference_number(value['reference_number'])
            journal.set_notes(value['notes'])
            journal.set_total(value['total'])
            journals_list.set_journals(journal)
        page_context = resp['page_context']
        page_context_obj = PageContext()
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_applied_filter(page_context['applied_filter'])
        if 'from_date' in page_context:
            page_context_obj.set_from_date(page_context['from_date'])
        if 'to_date' in page_context:
            page_context_obj.set_to_date(page_context['to_date'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        journals_list.set_page_context(page_context_obj)
        return journals_list

    def get_journal(self, resp):
        """This method parses the given response and returns journals object.

        Args:
            resp(dict): Response containing json object for journal.

        Returns:
            instance: Journal object.

        """
        journal = resp['journal']
        journal_obj = Journal()
        journal_obj.set_journal_id(journal['journal_id'])
        journal_obj.set_entry_number(journal['entry_number'])
        journal_obj.set_reference_number(journal['reference_number'])
        journal_obj.set_notes(journal['notes'])
        journal_obj.set_currency_id(journal['currency_id'])
        journal_obj.set_currency_symbol(journal['currency_symbol'])
        journal_obj.set_journal_date(journal['journal_date'])
        for value in journal['line_items']:
            line_item = LineItem()
            line_item.set_line_id(value['line_id'])
            line_item.set_account_id(value['account_id'])
            line_item.set_account_name(value['account_name'])
            line_item.set_description(value['description'])
            line_item.set_debit_or_credit(value['debit_or_credit'])
            line_item.set_tax_id(value['tax_id'])
            line_item.set_tax_name(value['tax_name'])
            line_item.set_tax_type(value['tax_type'])
            line_item.set_tax_percentage(value['tax_percentage'])
            line_item.set_amount(value['amount'])
            journal_obj.set_line_items(line_item)
        journal_obj.set_line_item_total(journal['line_item_total'])
        journal_obj.set_total(journal['total'])
        journal_obj.set_price_precision(journal['price_precision'])
        journal_obj.set_created_time(journal['created_time'])
        journal_obj.set_last_modified_time(journal['last_modified_time'])
        for value in journal['taxes']:
            tax = Tax()
            tax.set_tax_name(value['tax_name'])
            tax.set_tax_amount(value['tax_amount'])
            journal_obj.set_taxes(tax)
        return journal_obj

    def get_message(self, resp):
        """This method parses the given response and returns string message.

        Args:
            resp(dict): Response containing json object for message.

        Returns: 
            str: Success message.

        """
        return resp['message']

             
