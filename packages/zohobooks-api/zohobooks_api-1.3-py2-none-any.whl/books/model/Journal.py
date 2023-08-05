#$Id$

class Journal:   
    """This class is used to create object for Journals."""
    def __init__(self): 
        """Initilaize parameters for journals object."""
        self.journal_date = ''
        self.reference_number = ''
        self.notes = ''
        self.line_items = []
        self.journal_id = ''
        self.entry_number = ''
        self.currency_id = ''
        self.currency_symbol = ''
        self.journal_date = ''
        self.line_item_total = 0.0
        self.total = 0.0
        self.price_precision = 0
        self.taxes = []
        self.created_time = ''
        self.last_modified_time = ''

    def set_journal_date(self, journal_date):
        """Set journal date.
 
        Args:
            journal_date(str): Journal date.
 
        """
        self.journal_date = journal_date

    def get_journal_date(self):
        """Get journal date.

        Returns:
            str: Journal date.

        """
        return self.journal_date

    def set_reference_number(self, reference_number):
        """Set reference date.

        Args:
            reference_number(str): Reference number.

        """
        self.reference_number = reference_number

    def get_reference_number(self):
        """Get reference number.

        Returns:
            str: Reference number.

        """
        return self.reference_number

    def set_notes(self, notes):
        """Set notes.

        Args:
            notes(str): Notes.

        """
        self.note = notes

    def get_notes(self):
        """Get notes.

        Returns:
            str: Notes.

        """
        return self.notes

    def set_line_items(self, line_item):
        """Set line items.

        Args:
            line_items(instance): Line items.

        """
        self.line_items.append(line_item)

    def get_line_items(self):
        """Get line items.

        Returns:
            list of instance: List of instance object.

        """
        return self.line_items

    def set_journal_id(self, journal_id): 
        """Set journal id.

        Args:
            journal_id(str): Journal id.

        """
        self.journal_id = journal_id

    def get_journal_id(self):
        """Get journal id.
 
        Returns:
            str: Journal id.

        """
        return self.journal_id

    def set_entry_number(self, entry_number): 
        """Set entry number.

        Args:
            entry_number(str): Entry number.

        """
        self.entry_number = entry_number

    def get_entry_number(self):
        """Get entry number.

        Returns:
            str: Entry number.

        """
        return self.entry_number

    def set_currency_id(self, currency_id): 
        """Set currecny id.

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

    def set_journal_date(self, journal_date):
        """Set journal date.

        Args: 
            journal_date(str): Journal date.

        """ 
        self.journal_date = journal_date

    def get_journal_date(self):
        """Get journal date.

        Returns:
            str: Journal date.

        """
        return self.journal_date

    def set_line_item_total(self, line_item_total):
        """Set line item total.

        Args:
            lin_item_total(float): Line item total.

        """
        self.line_item_total = line_item_total

    def get_line_item_total(self):
        """Get line item total.

        Returns:
            float: Line item total.

        """
        return self.line_item_total

    def set_total(self, total): 
        """Set total.

        Args:
            total(float): Total.

        """
        self.total = total

    def get_total(self):
        """Get total.

        Returns: 
            float: Total.

        """
        return self.total

    def set_price_precision(self, price_precision):
        """Set price precision.

        Args:
            price_precision(int): Price precision.

        """
        self.price_precision = price_precision

    def get_price_precision(self):
        """Get price precision.

        Returns:
            int: Price precision.

        """
        return self.price_precision

    def set_taxes(self, tax):
        """Set taxes.

        Args:
            tax(instance): Tax.

        """
        self.taxes.append(tax)
  
    def get_taxes(self):
        """Get taxes.

        Returns:
            list of instance: List of tax object.

        """
        return self.taxes

    def set_created_time(self, created_time):
        """Set created time.

        Args:
            created_time(str): Created time.

        """
        self.created_time = created_time

    def get_created_time(self):
        """Get created time.

        Returns: 
            str: Created time.

        """
        return self.created_time

    def set_last_modified_time(self, last_modified_time):
        """Set last modified time.

        Args:
            last_modified_time(str): Last modified time.

        """
        self.last_modified_time = last_modified_time

    def get_last_modified_time(self): 
        """Get last modified time.

        Returns:
            str: Last modified time.

        """
        return self.last_modified_time

    def to_json(self): 
        """This method is used to create json object for journals.

        Returns:
            dict: Response containing json object for journals.

        """
        data = {} 
        if self.journal_date != '':       
            data['journal_date'] = self.journal_date
        if self.reference_number != '':
            data['reference_number'] = self.reference_number
        if self.notes != '':
            data['notes'] = self.notes
        if self.line_items:
            data['line_items'] = []
            for value in self.line_items:
                line_item = value.to_json()
                data['line_items'].append(line_item)
        return data 

