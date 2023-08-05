#$Id$#

from books.model.PreferenceList import PreferenceList
from books.model.Preference import Preference
from books.model.CustomField import CustomField
from books.model.PlaceholderAddressFormat import PlaceholderAddressFormat
from books.model.Autoreminder import Autoreminder
from books.model.AutoReminderList import AutoReminderList
from books.model.Term import Term
from books.model.AddressFormat import AddressFormat
from books.model.Invoice import Invoice
from books.model.Estimate import Estimate
from books.model.Contact import Contact
from books.model.Organization import Organization
from books.model.Customer import Customer
from books.model.Organization import Organization
from books.model.Address import Address
from books.model.UserList import UserList
from books.model.User import User
from books.model.EmailId import EmailId
from books.model.PageContext import PageContext
from books.model.Item import Item
from books.model.ItemList import ItemList
from books.model.InvoiceSetting import InvoiceSetting
from books.model.NotesAndTerms import NotesAndTerms
from books.model.EstimateSetting import EstimateSetting
from books.model.CreditnoteSetting import CreditnoteSetting
from books.model.CurrencyList import CurrencyList
from books.model.Currency import Currency
from books.model.ExchangeRate import ExchangeRate
from books.model.ExchangeRateList import ExchangeRateList
from books.model.TaxList import TaxList
from books.model.Tax import Tax
from books.model.TaxGroup import TaxGroup
from books.model.OpeningBalance import OpeningBalance
from books.model.Account import Account
from books.model.PlaceHolder import PlaceHolder
from books.model.ManualReminder import ManualReminder
from books.model.ManualReminderList import ManualReminderList

class SettingsParser:
    """This class is used to parse the json for Settings."""

    def preference_list(self, resp):
        """This method parses the given response and returns preferneces 
            object.

        Args:
            resp(dict): Response containing json obejct for preferences.

        Returns:
            instance: Prefenreces object.

        Raises:
            Books Exception: If status is not '200' or '201'.

        """
        preferences = resp['preferences']
        preferences_list = PreferenceList()
        preference_obj = Preference()
        preference_obj.set_convert_to_invoice(preferences[\
        'convert_to_invoice'])
        preference_obj.set_attach_pdf_for_email(preferences[\
        'attach_pdf_for_email'])
        preference_obj.set_estimate_approval_status(preferences[\
        'estimate_approval_status'])
        preference_obj.set_notify_me_on_online_payment(preferences[\
        'notify_me_on_online_payment'])
        preference_obj.set_send_payment_receipt_acknowledgement(preferences[\
        'send_payment_receipt_acknowledgement'])
        preference_obj.set_auto_notify_recurring_invoice(preferences[\
        'auto_notify_recurring_invoice'])
        preference_obj.set_snail_mail_include_payment_stub(preferences[\
        'snail_mail_include_payment_stub'])
        preference_obj.set_is_show_powered_by(preferences['is_show_powered_by'])
        preference_obj.set_attach_expense_receipt_to_invoice(preferences[\
        'attach_expense_receipt_to_invoice'])
        preference_obj.set_is_estimate_enabled(preferences[\
        'is_estimate_enabled'])
        preference_obj.set_is_project_enabled(preferences['is_project_enabled'])
        preference_obj.set_is_purchaseorder_enabled(preferences[\
        'is_purchaseorder_enabled'])
        preference_obj.set_is_salesorder_enabled(preferences[\
        'is_salesorder_enabled'])
        preference_obj.set_is_pricebooks_enabled(preferences[\
        'is_pricebooks_enabled'])
        preference_obj.set_attach_payment_receipt_with_acknowledgement(\
        preferences['attach_payment_receipt_with_acknowledgement'])
        for value in preferences['auto_reminders']:
            auto_reminder = Autoreminder()
            auto_reminder.set_payment_reminder_id(value['payment_reminder_id'])
            auto_reminder.set_is_enabled(value['is_enabled'])
            auto_reminder.set_notification_type(value['notification_type'])
            auto_reminder.set_address_type(value['address_type'])
            auto_reminder.set_number_of_days(value['number_of_days'])
            auto_reminder.set_subject(value['subject'])
            auto_reminder.set_body(value['body'])
            preference_obj.set_auto_reminders(auto_reminder)
        terms = preferences['terms']
        terms_obj = Term()
        terms_obj.set_invoice_terms(terms['invoice_terms'])
        terms_obj.set_estimate_terms(terms['estimate_terms'])
        terms_obj.set_creditnote_terms(terms['creditnote_terms'])
        preference_obj.set_terms(terms_obj)
        address_formats_obj = AddressFormat()
        address_formats = preferences['address_formats']
        address_formats_obj.set_organization_address_format(address_formats[\
        'organization_address_format'])
        address_formats_obj.set_customer_address_format(address_formats[\
        'customer_address_format'])
        preference_obj.set_address_formats(address_formats_obj)
        preferences_list.set_preferences(preference_obj)
        custom_fields = resp['customfields']
        custom_fields_obj = CustomField()
        for value in custom_fields['invoice']:
            invoice = Invoice()
            invoice.set_index(value['index'])
            invoice.set_show_in_all_pdf(value['show_in_all_pdf'])
            invoice.set_label(value['label'])
            custom_fields_obj.set_invoice(invoice)
        for value in custom_fields['contact']:
            contact = Contact()
            contact.set_index(value['index'])
            contact.set_show_in_all_pdf(vlaue['show_in_all_pdf'])
            contact.set_label(value['label'])
            custom_fields_obj.set_contact(contact)
        for value in custom_fields['estimate']:
            estimate = Estimate()
            estimate.set_index(value['index'])
            estimate.set_show_in_all_pdf(value['show_in_all_pdf'])
            estimate.set_label(value['label'])
            custom_fields_obj.set_estimate(estimate)
        preferences_list.set_custom_fields(custom_fields_obj)
        placeholders_address_format = resp['placeholders_address_format']
        placeholders_address_format_obj = PlaceholderAddressFormat()
        for value in placeholders_address_format['organization']:
            organization = Organization()
            organization.set_value(value['value'])
            organization.set_name(value['name'])
            placeholders_address_format_obj.set_organization(organization)
        for value in placeholders_address_format['customer']:
            customer = Customer()
            customer.set_name(value['name'])
            customer.set_value(value['value'])
            placeholders_address_format_obj.set_customer(customer)
        preferences_list.set_placeholders_address_format(\
        placeholders_address_format_obj)
        return preferences_list

    def get_message(self, resp):
        """This message parses the given response and returns message string.
    
        Args:
            resp(dict): Response containing json object for message.

        Returns:
            str: Success message.

        """
        return resp['message']

    def get_organizations(self, resp):
        """This message parses the given response and returns organizations 
            list.

        Args:
            resp(dict): Response containing json object for organizations list.
 
        Returns:
            instance: Organizations list object.

        """
        organizations_list = []
        for value in resp['organizations']:
            organization = Organization()
            organization.set_organization_id(value['organization_id'])
            organization.set_name(value['name'])
            organization.set_contact_name(value['contact_name'])
            organization.set_email(value['email'])
            organization.set_is_default_org(value['is_default_org'])
            organization.set_version(value['version'])
            organization.set_plan_type(value['plan_type'])
            organization.set_tax_group_enabled(value['tax_group_enabled'])
            organization.set_plan_name(value['plan_name'])
            organization.set_plan_period(value['plan_period'])
            organization.set_language_code(value['language_code'])
            organization.set_fiscal_year_start_month(value[\
            'fiscal_year_start_month'])
            organization.set_account_created_date(value[\
            'account_created_date'])
            organization.set_account_created_date_formatted(value[\
            'account_created_date_formatted'])
            organization.set_time_zone(value['time_zone'])
            organization.set_is_org_active(value['is_org_active'])
            organization.set_currency_id(value['currency_id'])
            organization.set_currency_code(value['currency_code'])
            organization.set_currency_symbol(value['currency_symbol'])
            organization.set_currency_format(value['currency_format'])
            organization.set_price_precision(value['price_precision'])
            organizations_list.append(organization)
        return organizations_list

    def get_organization(self, resp):
        """This method parses the given response and returns organization 
            object.

        Args:
            resp(dict): Response containing json object for organization.

        """
        organization = resp['organization']
        organization_obj = Organization()
        organization_obj.set_organization_id(organization['organization_id'])
        organization_obj.set_name(organization['name'])
        organization_obj.set_is_default_org(organization['is_default_org'])
        organization_obj.set_user_role(organization['user_role'])
        organization_obj.set_account_created_date(organization[\
        'account_created_date'])
        organization_obj.set_time_zone(organization['time_zone'])
        organization_obj.set_language_code(organization['language_code'])
        organization_obj.set_date_format(organization['date_format'])
        organization_obj.set_field_separator(organization['field_separator'])
        organization_obj.set_fiscal_year_start_month(organization[\
        'fiscal_year_start_month'])
        organization_obj.set_contact_name(organization['contact_name'])
        organization_obj.set_industry_type(organization['industry_type'])
        organization_obj.set_industry_size(organization['industry_size'])
        organization_obj.set_company_id_label(organization['company_id_label'])
        organization_obj.set_company_id_value(organization['company_id_value'])
        organization_obj.set_tax_id_label(organization['tax_id_label'])
        organization_obj.set_tax_id_value(organization['tax_id_value'])
        organization_obj.set_currency_id(organization['currency_id'])
        organization_obj.set_currency_code(organization['currency_code'])
        organization_obj.set_currency_symbol(organization['currency_symbol'])
        organization_obj.set_currency_format(organization['currency_format'])
        organization_obj.set_price_precision(organization['price_precision'])
        address = organization['address']
        address_obj = Address()
        address_obj.set_street_address1(address['street_address1'])
        address_obj.set_street_address2(address['street_address2'])
        address_obj.set_city(address['city'])
        address_obj.set_state(address['state'])
        address_obj.set_country(address['country'])
        address_obj.set_zip(address['zip'])
        organization_obj.set_address(address_obj)
        organization_obj.set_org_address(organization['org_address'])
        organization_obj.set_remit_to_address(organization['remit_to_address'])
        organization_obj.set_phone(organization['phone'])
        organization_obj.set_fax(organization['fax'])
        organization_obj.set_website(organization['website'])
        organization_obj.set_email(organization['email'])
        organization_obj.set_tax_basis(organization['tax_basis'])
        for value in organization['custom_fields']:
            custom_field = CustomField()
            custom_field.set_value(value['value'])
            custom_field.set_index(value['index'])
            custom_field.set_label(value['label'])
            organization_obj.set_custom_fields(custom_field)
        organization_obj.set_is_org_active(organization['is_org_active'])
        organization_obj.set_is_new_customer_custom_fields(organization[\
        'is_new_customer_custom_fields'])
        organization_obj.set_is_portal_enabled(organization['is_portal_enabled'])
        organization_obj.set_portal_name(organization['portal_name'])
        return organization_obj

    def get_users(self, resp):
        """This method parses the given response and returns USers list object.

        Args:
            resp(dict): Response containing json object for users list.

        Returns:
            instance: Users list object.

        """
        users_list = UserList()
        for value in resp['users']:
            user = User()
            user.set_user_id(value['user_id'])
            user.set_role_id(value['role_id'])
            user.set_name(value['name'])
            user.set_email(value['email'])
            user.set_user_role(value['user_role'])
            user.set_status(value['status'])
            user.set_is_current_user(value['is_current_user'])
            user.set_photo_url(value['photo_url'])
            users_list.set_users(user)
        page_context_obj = PageContext()
        page_context = resp['page_context']
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_applied_filter(page_context['applied_filter'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        users_list.set_page_context(page_context_obj)
        return users_list

    def get_user(self, resp):
        """This method parses the given response and returns user object.

        Args:
            resp(dict): Response containing json object for user.

        Returns:
            instance: User object.

        Raises: 
            Books Exception: If status is not '200' or '201'.

        """
        user = resp['user'] 
        user_obj = User()
        user_obj.set_user_id(user['user_id'])
        user_obj.set_name(user['name'])
        for value in user['email_ids']:
            email_id = EmailId()
            email_id.set_is_selected(value['is_selected'])
            email_id.set_email(value['email'])
            user_obj.set_email_ids(email_id)
        user_obj.set_status(user['status'])
        user_obj.set_user_role(user['user_role'])
        user_obj.set_created_time(user['created_time'])
        user_obj.set_photo_url(user['photo_url'])
        return user_obj

    def get_items(self, resp):
        """This method parses the given response and returns items list object.

        Args:
            resp(dict): Response containing json object for items list.

        Returns:
            instance: Items list object.

        """
        items_list = ItemList()
        for value in resp['items']:
            item = Item()
            item.set_item_id(value['item_id'])
            item.set_name(value['name'])
            item.set_status(value['status'])
            item.set_description(value['description'])
            item.set_rate(value['rate'])
            item.set_tax_id(value['tax_id'])
            item.set_tax_name(value['tax_name'])
            item.set_tax_percentage(value['tax_percentage'])
            for tp in value['item_tax_preferences']:
                item.set_item_tax_preferences(tp)
            items_list.set_items(item)
        page_context_obj = PageContext()
        page_context = resp['page_context']
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_applied_filter(page_context['applied_filter'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        items_list.set_page_context(page_context_obj)
        return items_list

    def get_item(self, resp):
        """This method parses the given response and returns item object.

        Args:
            resp(dict): Response containing json object for item.

        Returns:
            instance: Item object.

        """
        item = resp['item']
        item_obj = Item()
        item_obj.set_item_id(item['item_id'])
        item_obj.set_name(item['name'])
        item_obj.set_status(item['status'])
        item_obj.set_description(item['description'])
        item_obj.set_rate(item['rate'])
        item_obj.set_unit(item['unit'])
        item_obj.set_account_id(item['account_id'])
        item_obj.set_account_name(item['account_name'])
        item_obj.set_tax_id(item['tax_id'])
        item_obj.set_tax_name(item['tax_name'])
        item_obj.set_tax_percentage(item['tax_percentage'])
        item_obj.set_tax_type(item['tax_type'])
        return item_obj
        
    def get_invoice_settings(self, resp):
        """This method parses the given response and returns invoice settings 
            object.

        Args:
            resp(dict): Response containing json object for invoice settings.

        Returns:
            instance: Invoice settings object.

        """
        invoice_settings = resp['invoice_settings']
        invoice_settings_obj = InvoiceSetting()
        invoice_settings_obj.set_auto_generate(invoice_settings[\
        'auto_generate'])
        invoice_settings_obj.set_prefix_string(invoice_settings[\
        'prefix_string'])
        invoice_settings_obj.set_start_at(invoice_settings['start_at'])
        invoice_settings_obj.set_next_number(invoice_settings['next_number'])
        invoice_settings_obj.set_quantity_precision(invoice_settings[\
        'quantity_precision'])
        invoice_settings_obj.set_discount_type(invoice_settings[\
        'discount_type'])
        invoice_settings_obj.set_is_discount_before_tax(invoice_settings[\
        'is_discount_before_tax'])
        invoice_settings_obj.set_reference_text(invoice_settings[\
        'reference_text'])
        invoice_settings_obj.set_notes(invoice_settings['notes'])
        invoice_settings_obj.set_terms(invoice_settings['terms'])
        invoice_settings_obj.set_is_shipping_charge_required(invoice_settings[\
        'is_shipping_charge_required'])
        invoice_settings_obj.set_is_adjustment_required(invoice_settings[\
        'is_adjustment_required'])
        invoice_settings_obj.set_is_open_invoice_editable(invoice_settings[\
        'is_open_invoice_editable'])
        invoice_settings_obj.set_warn_convert_to_open(invoice_settings[\
        'warn_convert_to_open']) 
        invoice_settings_obj.set_warn_create_creditnotes(invoice_settings[\
        'warn_create_creditnotes'])
        invoice_settings_obj.set_attach_expense_receipt_to_invoice(\
        invoice_settings['attach_expense_receipt_to_invoice'])
        invoice_settings_obj.set_invoice_item_type(invoice_settings[\
        'invoice_item_type'])
        invoice_settings_obj.set_is_sales_person_required(invoice_settings[\
        'is_sales_person_required'])
        return invoice_settings_obj

    def get_notes_and_terms(self, resp):
        """This method parses the given response and returns notes and terms 
            object.
    
        Args:
            resp(dict): Dictionary containing json object for estimate 
                settings.

        Returns:
            instance: Notes and terms object.

        """
        notes_and_terms = resp['notes_and_terms']
        notes_and_terms_obj = NotesAndTerms()
        notes_and_terms_obj.set_notes(notes_and_terms['notes'])
        notes_and_terms_obj.set_terms(notes_and_terms['terms'])
        return notes_and_terms_obj

    def get_estimate_settings(self, resp):
        """This method parses the given response and returns estimate settings 
            object.

        Args:
            resp: Dictionary containing json object for estimate settings.

        Returns:
            instance: Estimate settings object.

        """
        estimate_settings = resp['estimate_settings']
        estimate_settings_obj = EstimateSetting()
        estimate_settings_obj.set_auto_generate(estimate_settings[\
        'auto_generate'])
        estimate_settings_obj.set_prefix_string(estimate_settings[\
        'prefix_string'])
        estimate_settings_obj.set_start_at(estimate_settings['start_at']) 
        estimate_settings_obj.set_next_number(estimate_settings['next_number'])
        estimate_settings_obj.set_quantity_precision(estimate_settings[\
        'quantity_precision'])
        estimate_settings_obj.set_discount_type(estimate_settings[\
        'discount_type'])
        estimate_settings_obj.set_is_discount_before_tax(estimate_settings[\
        'is_discount_before_tax']) 
        estimate_settings_obj.set_reference_text(estimate_settings[\
        'reference_text'])
        estimate_settings_obj.set_notes(estimate_settings['notes'])
        estimate_settings_obj.set_terms(estimate_settings['terms'])
        estimate_settings_obj.set_terms_to_invoice(estimate_settings[\
        'terms_to_invoice'])
        estimate_settings_obj.set_notes_to_invoice(estimate_settings[\
        'notes_to_invoice'])
        estimate_settings_obj.set_warn_estimate_to_invoice(estimate_settings[\
        'warn_estimate_to_invoice'])
        estimate_settings_obj.set_is_sales_person_required(estimate_settings[\
        'is_sales_person_required'])
        return estimate_settings_obj

    def get_creditnote_settings(self, resp):
        """This method parses the given response and returns creditnote 
            settings.

        Args:
            resp(dict): Dictionary containing json object for creditnote 
                settings.

        Returns:
            instance: Creditnotes settings object.

        """
        creditnote_settings_obj = CreditnoteSetting()
        creditnote_settings = resp['creditnote_settings'] 
        creditnote_settings_obj.set_auto_generate(creditnote_settings[\
        'auto_generate'])
        creditnote_settings_obj.set_prefix_string(creditnote_settings[\
        'prefix_string'])
        creditnote_settings_obj.set_reference_text(creditnote_settings[\
        'reference_text'])
        creditnote_settings_obj.set_next_number(creditnote_settings[\
        'next_number'])
        creditnote_settings_obj.set_notes(creditnote_settings['notes'])
        creditnote_settings_obj.set_terms(creditnote_settings['terms'])
        return creditnote_settings_obj

    def get_currencies(self, resp):
        """This method parses the given response and returns currency list 
            object.

        Args:
            resp(dict): Response containing json object for list of currencies.

        Returns:
            instance: Currency list object.

        """
        currency_list = CurrencyList()
        for value in resp['currencies']:
            currency = Currency()
            currency.set_currency_id(value['currency_id'])
            currency.set_currency_code(value['currency_code'])
            currency.set_currency_name(value['currency_name'])
            currency.set_currency_symbol(value['currency_symbol'])
            currency.set_price_precision(value['price_precision'])
            currency.set_currency_format(value['currency_format'])
            currency.set_is_base_currency(value['is_base_currency'])
            currency.set_exchange_rate(value['exchange_rate'])
            currency.set_effective_date(value['effective_date'])
            currency_list.set_currencies(currency)
        page_context_obj = PageContext()
        page_context = resp['page_context'] 
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        currency_list.set_page_context(page_context_obj)
        return currency_list

    def get_currency(self, resp):
        """This method parses the given response and returns currency object.

        Args:
            resp(dict): Response containing json object for currency.

        Returns:
            instance: Currency object.

        """
        currency_obj = Currency()
        currency = resp['currency'] 
        currency_obj.set_currency_id(currency['currency_id'])
        currency_obj.set_currency_code(currency['currency_code'])
        currency_obj.set_currency_name(currency['currency_name'])
        currency_obj.set_currency_symbol(currency['currency_symbol'])
        currency_obj.set_price_precision(currency['price_precision'])
        currency_obj.set_currency_format(currency['currency_format'])
        currency_obj.set_is_base_currency(currency['is_base_currency'])
        return currency_obj

    def get_exchange_rates(self, resp):
        """This method parses the given response and returns exchange rates 
            list.

        Args:
            resp(dict): Response containing json object for exchange rate.
 
        Returns:
            list of instance: List of exchange rates object.

        """
        exchange_rates = ExchangeRateList()
        for value in resp['exchange_rates']:
            exchange_rate = ExchangeRate()
            exchange_rate.set_exchange_rate_id(value['exchange_rate_id'])
            exchange_rate.set_currency_id(value['currency_id'])
            exchange_rate.set_currency_code(value['currency_code'])
            exchange_rate.set_effective_date(value['effective_date']) 
            exchange_rate.set_rate(value['rate'])
            exchange_rates.set_exchange_rates(exchange_rate)
        return exchange_rates

    def get_exchange_rate(self, resp):
        """This method parses the given response and returns exchange rate 
            object.

        Args:
            resp(dict): Response containing json object for exchange rate 
                object.

        Returns: 
            instance: Exchange rate object.

        """
        exchange_rate = resp['exchange_rate']
        exchange_rate_obj = ExchangeRate()
        exchange_rate_obj.set_exchange_rate_id(exchange_rate[\
        'exchange_rate_id'])
        exchange_rate_obj.set_currency_id(exchange_rate['currency_id'])
        exchange_rate_obj.set_currency_code(exchange_rate['currency_code'])
        exchange_rate_obj.set_effective_date(exchange_rate['effective_date'])
        exchange_rate_obj.set_rate(exchange_rate['rate'])
        return exchange_rate_obj   

    def get_taxes(self, resp):
        """This method parses the given response and returns tax list object.

        Args:
            resp(dict): Response containing json object for taxes.

        Returns:
            instance: Tax list object.

        """
        tax_list = TaxList()
        for value in resp['taxes']:
            tax = Tax()
            tax.set_tax_id(value['tax_id'])
            tax.set_tax_name(value['tax_name'])
            tax.set_tax_percentage(value['tax_percentage'])
            tax.set_tax_type(value['tax_type'])
            tax_list.set_taxes(tax)
        page_context = resp['page_context']
        page_context_obj = PageContext()
        page_context_obj.set_page(page_context['page'])
        page_context_obj.set_per_page(page_context['per_page'])
        page_context_obj.set_has_more_page(page_context['has_more_page'])
        page_context_obj.set_report_name(page_context['report_name'])
        page_context_obj.set_sort_column(page_context['sort_column'])
        page_context_obj.set_sort_order(page_context['sort_order'])
        tax_list.set_page_context(page_context_obj)
        return tax_list

    def get_tax(self, resp):
        """This method parses the given response and returns tax object.

        Args:
            resp(dict): Response containing json object for tax.

        Returns:
            instance: Tax object.

        """
        tax_obj = Tax()
        tax = resp['tax']
        tax_obj.set_tax_id(tax['tax_id'])
        tax_obj.set_tax_name(tax['tax_name'])
        tax_obj.set_tax_percentage(tax['tax_percentage'])
        tax_obj.set_tax_type(tax['tax_type'])
        return tax_obj

    def get_tax_group(self, resp):
        """This method parses the given response and returns Tax group object.

        Args:
            resp(dict): Response containing json object for tax group.

        Returns:
            instance: Tax group object.

        Raises:
            Books Exception: If status is not '200' or '201'.

        """
        tax_group_obj = TaxGroup()
        tax_group = resp['tax_group']
        tax_group_obj.set_tax_group_id(tax_group['tax_group_id'])
        tax_group_obj.set_tax_group_name(tax_group['tax_group_name'])
        tax_group_obj.set_tax_group_percentage(tax_group[\
        'tax_group_percentage'])
        for value in tax_group['taxes']:
            tax = Tax()
            tax.set_tax_id(value['tax_id'])
            tax.set_tax_name(value['tax_name'])
            tax.set_tax_percentage(value['tax_percentage'])
            tax.set_tax_type(value['tax_type'])
            tax_group_obj.set_taxes(tax)
        return tax_group_obj

    def get_opening_balance(self, resp):
        """This method parses the given response and returns opening balance 
            object.

        Args:
            resp(dict): Response containing json object for opening balance.

        Returns:
            instance: Opening balance object.

        """
        opening_balance_obj = OpeningBalance()
        opening_balance = resp['opening_balance'] 
        opening_balance_obj.set_opening_balance_id(opening_balance[\
        'opening_balance_id'])
        opening_balance_obj.set_date(opening_balance['date'])
        for value in opening_balance['accounts']:
            accounts = Account()
            accounts.set_account_split_id(value['account_split_id'])
            accounts.set_account_id(value['account_id'])
            accounts.set_account_name(value['account_name'])
            accounts.set_debit_or_credit(value['debit_or_credit'])
            accounts.set_exchange_rate(value['exchange_rate'])
            accounts.set_currency_id(value['currency_id'])
            accounts.set_currency_code(value['currency_code'])
            accounts.set_bcy_amount(value['bcy_amount'])
            accounts.set_amount(value['amount'])
            opening_balance_obj.set_accounts(accounts)
        return opening_balance_obj

    def get_autoreminders(self, resp):
        """This method parses the given response and returns autoreminders list.
        
        Args:
            resp(dict): Response containing json object for autoreminders.

        Returns:
            instance: Reminder list object.

        """
        autoreminders = AutoReminderList()
        for value in resp['autoreminders']:
            autoreminders_obj = Autoreminder()
            autoreminders_obj.set_autoreminder_id(value['autoreminder_id'])
            autoreminders_obj.set_is_enabled(value['is_enabled'])
            autoreminders_obj.set_notification_type(value['type'])
            autoreminders_obj.set_address_type(value['address_type'])
            autoreminders_obj.set_number_of_days(value['number_of_days'])
            autoreminders_obj.set_subject(value['subject'])
            autoreminders_obj.set_body(value['body'])
            autoreminders_obj.set_order(value['order'])
            autoreminders.set_auto_reminders(autoreminders_obj)
        return autoreminders

    def get_autoreminder(self, resp):
        """Get auto reminder.

        Args:
            resp(dict): Response containing json object for auto reminders 
                object.

        Returns:
            instance: Auto reminders object.

        """
        autoreminder = resp['autoreminder']
        autoreminder_obj = Autoreminder()
        autoreminder_obj.set_autoreminder_id(autoreminder['autoreminder_id'])
        autoreminder_obj.set_is_enabled(autoreminder['is_enabled'])
        autoreminder_obj.set_notification_type(autoreminder['type'])
        autoreminder_obj.set_address_type(autoreminder['address_type'])
        autoreminder_obj.set_number_of_days(autoreminder['number_of_days'])
        autoreminder_obj.set_subject(autoreminder['subject'])
        autoreminder_obj.set_body(autoreminder['body'])
        placeholders_obj = PlaceHolder()
        placeholders = resp['placeholders'] 
        for value in placeholders['Invoice']: 
            invoice = Invoice()
            invoice.set_name(value['name'])
            invoice.set_value(value['value'])
            placeholders_obj.set_invoice(invoice)
        for value in placeholders['Customer']:
            customer = Customer()
            customer.set_name(value['name'])
            customer.set_value(value['value'])
            placeholders_obj.set_customer(customer)
        for value in placeholders['Organization']:
            organization = Organization()
            organization.set_value(value['value'])
            organization.set_name(value['name'])
            placeholders_obj.set_organization(organization)
        autoreminder_obj.set_placeholders(placeholders)
        return autoreminder_obj

    def get_manual_reminders(self, resp):
        """This method parses the given response and returns manual reminders 
            list.

        Args:
            resp(dict): Response containing json object for manual reminders 
                list.

        Returns:
            list of instance: List of manual reminders object.

        """
        manual_reminders = ManualReminderList()
        for value in resp['manualreminders']:
            manual_reminder = ManualReminder()       
            manual_reminder.set_manualreminder_id(value['manualreminder_id'])
            manual_reminder.set_type(value['type'])
            manual_reminder.set_subject(value['subject'])
            manual_reminder.set_body(value['body'])
            manual_reminder.set_cc_me(value['cc_me'])
            manual_reminders.set_manual_reminders(manual_reminder)
        return manual_reminders

    def get_manual_reminder(self, resp):
        """Get manual reminder.

        Args:
            resp(dict): Response containing json object for manual reminder.

        Returns:
            instance: Manual reminders object.

        """
        manualreminder = resp['manualreminder']
        manualreminder_obj = ManualReminder()
        manualreminder_obj.set_manualreminder_id(manualreminder[\
        'manualreminder_id'])
        manualreminder_obj.set_type(manualreminder['type'])
        manualreminder_obj.set_subject(manualreminder['subject'])
        manualreminder_obj.set_body(manualreminder['body'])
        manualreminder_obj.set_cc_me(manualreminder['cc_me'])
        placeholders = resp['placeholders']
        placeholders_obj = PlaceHolder()
        for value in placeholders['Invoice']:
            invoice = Invoice()
            invoice.set_name(value['name'])
            invoice.set_value(value['value'])
            placeholders_obj.set_invoice(invoice)
        for value in placeholders['Customer']:
            customer = Customer()
            customer.set_name(value['name'])
            customer.set_value(value['value'])
            placeholders_obj.set_customer(customer)
        for value in placeholders['Organization']:
            organization = Organization()
            organization.set_name(value['name'])
            organization.set_value(value['value'])
            placeholders_obj.set_organization(organization)
        manualreminder_obj.set_placeholders(placeholders_obj)
        return manualreminder_obj
            

        

        

        
 
