#$Id$

from books.model.Address import Address

class Organization: 
    """This class is used to create object for organization."""
    def __init__(self):
        """Initialize parameters for organization object. """
        self.organization_id = ''
        self.name = ''
        self.is_default_org = None
        self.account_created_date = ''
        self.time_zone = ''
        self.language_code = ''
        self.date_format = ''
        self.field_separator = ''
        self.fiscal_year_start_month = ''
        self.contact_name = ''
        self.industry_type = ''
        self.industry_size = ''
        self.company_id_label = ''
        self.company_id_value = ''
        self.tax_id_label = ''
        self.tax_id_value = ''
        self.currency_id = ''
        self.currency_code = ''
        self.currency_symbol = ''
        self.currency_format = ''
        self.price_precision = 0
        self.address = Address()
        self.org_address = ''
        self.remit_to_address = ''
        self.phone = ''
        self.fax = ''
        self.website = ''
        self.email = ''
        self.tax_basis = ''
        self.is_org_active = None
        self.name = ''
        self.value = ''
        self.version = ''
        self.plan_type = 0
        self.plane_name = ''
        self.plan_period = ''
        self.tax_group_enabled = None
        self.account_created_date_formatted = ""
        self.zi_migration_status = 0
        self.user_role = ''
        self.custom_fields = []
        self.is_new_customer_custom_fields = None
        self.is_portal_enabled = None
        self.portal_name = ''
        self.tax_type = ''

    def set_organization_id(self, organization_id):
        """Set organization id.

        Args: 
            organization_id(str): Organization id.

        """
        self.organization_id = organization_id

    def get_organization_id(self):
        """Get organization id.

        Returns:
            str: Organization id.

        """
        return self.organization_id

    def set_name(self, name):
        """Set name.

        Args:
            name(str): Name.

        """
        self.name = name

    def set_is_default_org(self, is_default_org):
        """Set whether it is default organization.

        Args:
            is_default_org(bool): True if it is default organization else false.

        """
        self.is_default_org = is_default_org

    def get_is_default_org(self): 
        """Get whether it is default organization.

        Returns:
            bool: True if it is default organization else false.

        """
        return self.is_default_org

    def set_account_created_date(self, account_created_date):
        """Set account created date.

        Args:
            account_created_date(str): Account created date.

        """
        self.account_created_date = account_created_date

    def get_account_created_date(self):
        """Get account created date.

        Returns:
            str: Account created date.

        """
        return self.account_created_date

    def set_time_zone(self, time_zone):
        """Set time zone.

        Args:
            time_zone(str): Time zone.

        """
        self.time_zone = time_zone

    def get_time_zone(self):
        """Get time zone.

        Returns:
            str: Time zone.

        """
        return self.time_zone

    def set_language_code(self, language_code):
        """Set language code.

        Args:
            language_code(str): Language code.

        """
        self.language_code = language_code

    def get_language_code(self):
        """Get language code.

        Returns:
            str: Language code.

        """
        return self.language_code

    def set_date_format(self, date_format):
        """Set date format.

        Args:
            date_format(str): Date format.

        """
        self.date_format = date_format

    def get_date_format(self):
        """Get date format.

        Returns:
            str: Date format.

        """
        return self.date_format

    def set_field_separator(self, field_separator):
        """Set field separator.

        Args:
            field_separator(str): Field separator.

        """
        self.field_separator = field_separator

    def get_field_separator(self):
        """Get field separator.

        Returns:
            str: Field separator.

        """
        return self.field_separator

    def set_fiscal_year_start_month(self, fiscal_year_start_month):
        """Set fiscal year field separator.

        Args:
            fiscal_year_start_month(str): Fiscal year start month.

        """
        self.fiscal_year_start_month = fiscal_year_start_month

    def get_fiscal_year_start_month(self):
        """Get fiscal year start month.

        Returns:
            str: Fiscal year start month.

        """
        return self.fiscal_year_start_month

    def set_contact_name(self, contact_name): 
        """Set contact name.

        Args: 
            contact_name(str): Contact name.

        """
        self.contact_name = contact_name

    def get_contact_name(self):
        """Get contact name.

        Returns:
            str: Contact name.

        """
        return self.contact_name

    def set_industry_type(self, industry_type):
        """Set industry type.

        Args:
            industry_type(str): Industry type.

        """
        self.industry_type = industry_type

    def get_industry_type(self):
        """Get industry type.

        Returns:
            str: Industry type.

        """ 
        return self.industry_type

    def set_industry_size(self, industry_size):
        """Set industry size.

        Args:
            industry_size(str): Industry size.

        """
        self.industry_size = industry_size

    def get_industry_size(self):
        """Get industry size.

        Returns:
            str: Industry size.

        """
        return self.industry_size

    def set_company_id_label(self, company_id_label):
        """Set company id label.

        Args:
            company_id_label(str): Company id label.

        """
        self.company_id_label = company_id_label

    def get_company_id_label(self):
        """Get company id label.

        Returns:
            str: Company id label.

        """
        return self.company_id_label

    def set_company_id_value(self, company_id_value):
        """Set company id value.

        Args:
            company_id_value(str): Company id value.

        """
        self.company_id_value = company_id_value

    def get_company_id_value(self):
        """Get company id value.

        Returns:
            str: Company id value.

        """
        return self.company_id_value

    def set_tax_id_label(self, tax_id_label):
        """Set tax id label.

        Args:
            tax_id_label(str): Tax id label.

        """
        self.tax_id_label = tax_id_label

    def get_tax_id_label(self):
        """Get tax id label.

        Retruns:
            str: Tax id label.

        """
        return self.tax_id_label

    def set_tax_id_value(self, tax_id_value):
        """Set tax id value.

        Args:
            tax_id_value(str): Tax id value.

        """
        self.tax_id_value = tax_id_value

    def get_tax_id_value(self):
        """Get atx id value.

        Returns:
            str: Tax id value.

        """
        return self.tax_id_value

    def set_currency_id(self, currency_id):
        """Set currency id.

        Args:
            currency_id(str): Currency id.

        """
        self.currency_id = currency_id

    def get_currency_id(self):
        """Get currency id.

        Returns:
            str: Currency id.

        """
        return self.currency_id

    def set_currency_code(self, currency_code):
        """Set currency code.

        Args:
            currency_code(str): Currency code.

        """
        self.currency_code = currency_code

    def get_currency_code(self):
        """Get currency code.

        Returns:
            str: Currency code.

        """
        return self.currency_code

    def set_currency_symbol(self, currency_symbol):
        """Set currency symbol.

        Args:
            currency_symbol(str): Currency symbol.

        """ 
        self.currency_symbol = currency_symbol

    def get_currency_symbol(self):
        """Get currency symbol.

        Returns:
            str: Currency symbol.

        """
        return self.currency_symbol

    def set_currency_format(self, currency_format):
        """Set currency format.

        Args:
            currency_format(str): Currency format.

        """
        self.currency_format = currency_format

    def get_currency_format(self):
        """Get currency format.

        Retruns:
            str: Currency format.

        """
        return self.currency_format

    def set_price_precision(self, price_precision):
        """Set price precision.

        Args:
            price_precision(int): Price precision.

        """
        self.price_precision = price_precision

    def set_address(self, address):
        """Set address.

        Args:
            address(instance): Address

        """
        self.address = address

    def get_address(self):
        """Get address.

        Returns:
            instance: Address.

        """
        return self.address

    def set_org_address(self, org_address):
        """Set organization address.

        Args:
            org_address(str): Organization address.

        """
        self.org_address = org_address

    def get_org_address(self):
        """Get organization address.

        Returns:
            str: Organization address.

        """
        return self.org_address

    def set_remit_to_address(self, remit_to_address):
        """Set remit to address.

        Args:
            remit_to_address(str): Remit to address.
 
        """
        self.remit_to_address = remit_to_address

    def get_remit_to_address(self):
        """Get remit to address.

        Returns:
            str: Remit to address.

        """ 
        return self.remit_to_address

    def set_phone(self, phone):
        """Set phone.

        Args:
            phone(str): Phone.

        """
        self.phone = phone

    def get_phone(self):
        """Get phone.

        Returns:
            str: Phone.

        """
        return self.phone

    def set_fax(self, fax):
        """Set fax.

        Args:
            fax(str): Fax.

        """
        self.fax = fax

    def get_fax(self):
        """Get fax.

        Returns:
            str: Fax.

        """
        return self.fax

    def set_website(self, website):
        """Set website.

        Args:
            website(str): Website.

        """
        self.website = website

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

    def set_tax_basis(self, tax_basis):
        """Set tax basis.

        Args:
            tax_basis(str): Tax basis.
      
        """
        self.tax_basis = tax_basis

    def get_tax_basis(self):
        """Get tax basis.

        Returns:
            str: Tax basis.

        """
        return self.tax_basis

    def set_is_org_active(self, is_org_active):
        """Set whether it the organization is active or not.

        Args:
            is_org_active(bool): True if organization is active else false.

        """
        self.is_org_active = is_org_active

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

    def set_value(self, value):
        """Set value.

        Args:
            value(str): Value.

        """
        self.value = value

    def get_value(self):
        """Get value.

        Returns:
            str: Value.

        """
        return self.value

    def set_version(self, version):
        """Set version.
 
        Args:
            version(str): Version

        """
        self.version = version

    def get_version(self):
        """Get version.

        Returns:
            str: Version.

        """
        return self.version

    def set_plan_type(self, plan_type):
        """Set plan type.

        Args:
            plan_type(int): Plan type.

        """
        self.plan_type = plan_type

    def get_plan_type(self):
        """Get plan type.

        Returns: 
            int: Plan type.

        """
        return self.plan_type

    def set_plan_name(self, plan_name):
        """Set plan name.

        Args:
            plan_name(str): Plan name.

        """
        self.plan_name = plan_name

    def get_plan_name(self):
        """Get plan name.

        Args:
            str: Plan name.

        """
        return self.plan_name

    def set_plan_period(self, plan_period):
        """Set plan period.

        Args:
            plan_period(str): Plan period.

        """
        self.plan_period = plan_period

    def get_plan_period(self):
        """Get plan period.

        Returns:
            str: Plan period.

        """
        return self.plan_period

    def set_tax_group_enabled(self, tax_group_enabled):
        """Set tax group enabled.

        Args:
            tax_group_enabled(bool): Tax group enabled.

        """
        self.tax_group_enabled = tax_group_enabled

    def get_tax_group_enabled(self):
        """Get tax group enabled.

        Returns:
            bool: Tax group enabled.

        """
        return self.tax_group_enabled

    def set_account_created_date_formatted(self, account_created_date_formatted):
        """Set account created date formatted.

        Args:
            account_created_date_formatted(str): Account created date formatted.

        """
        self.account_created_date_formatted = account_created_date_formatted

    def get_account_created_date_formatted(self):
        """Get account created date formatted.

        Returns: 
            str: Account created date formatted.

        """
        return self.account_created_date_formatted

    def set_zi_migration_status(self, zi_migration_status):
        """Set zi migration status.

        Args:
            zi_migration_status(int): Zi migration status.

        """
        self.zi_migration_status = zi_migration_status

    def get_zi_migration_status(self):
        """Get zi migration status .

        Returns:
            int: Zi migration status.

        """
        return self.zi_migration_status

    def set_custom_fields(self, custom_field):
        """Set custom fields.

        Args:
            custom_field(instance): Custom field.

        """
        self.custom_fields.append(custom_field)

    def get_custom_fields(self):
        """Get custom fields.

        Returns:
            list of instance: List of custom fields object.

        """
        return self.custom_fields

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

    def set_is_new_customer_custom_fields(self, is_new_customer_custom_fields):
        """Set whether new customer custom fields or not.

        Args:
            is_new_customer_custom_fields(bool): True if new customer custom fields else False.

        """
        self.is_new_customer_custom_fields = is_new_customer_custom_fields

    def get_is_new_customer_custom_fields(self):
        """Get whether new customer custom fields or not.

        Returns:
            bool: True if new customer custom fields else false.

        """ 
        return self.is_new_customer_custom_fields

    def set_is_portal_enabled(self, is_portal_enabled):
        """Set whether portal is enabled or not.

        Args:
            is_portal_enabled(bool): True if portal enabled else false.

        """
        self.is_portal_enabled = is_portal_enabled

    def get_is_portal_enabled(self):
        """Get whether is portal enabled.

        Returns:
            bool: True if portal is enabled else false.

        """
        return self.is_portal_enabled

    def set_portal_name(self, portal_name):
        """Set portal name.

        Args:
            portal_name(str): Portal name.

        """
        self.portal_name = portal_name

    def get_portal_name(self):
        """Get portal name.

        Returns:
            str: Portal name.

        """
        return self.portal_name

    def set_tax_type(self, tax_type):
        """Set tax type.

        Args:
            tax_type(str): Tax type.

        """
        self.tax_type = tax_type

    def get_tax_type(self):
        """Get tax type.

        Returns:
            str: Tax type.

        """
        return self.tax_type

    def to_json(self):
        """This method is used to convert organizations object to json format.

        Returns:
            dict: Dictionary containing json object for organizations.

        """
        data = {}
        if self.name != '':
            data['name'] = self.name
        if self.address is not None:
            data['address'] = self.address.to_json()
        if self.industry_type != '':
            data['industry_type'] = self.industry_type
        if self.industry_size != '':
            data['industry_size'] = self.industry_size
        if self.fiscal_year_start_month != '':
            data['fiscal_year_start_month'] = self.fiscal_year_start_month
        if self.currency_code != '':
            data['currency_code'] = self.currency_code
        if self.time_zone != '':
            data['time_zone'] = self.time_zone
        if self.date_format != '':
            data['date_format'] = self.date_format
        if self.field_separator != '':
            data['field_separator'] = self.field_separator
        if self.language_code != '':
            data['language_code'] = self.language_code
        if self.tax_basis != '':
            data['tax_basis'] = self.tax_basis
        if self.org_address != '':
            data['org_address'] = self.org_address
        if self.remit_to_address != '':
            data['remit_to_address'] = self.remit_to_address
        if self.tax_type != '':
            data['tax_type'] = self.tax_type
        return data
