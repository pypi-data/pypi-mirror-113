#$Id$

class EstimateSetting:
    """This class is used to create object for estimate settings."""
    def __init__(self):
        """Initialize parameters for estimate settings."""
        self.auto_generate = None
        self.prefix_string = ""
        self.start_at = 0
        self.next_number = ""
        self.quantity_precision = 0
        self.discount_type = ""
        self.is_discount_before_tax = None
        self.reference_text = ""
        self.notes = ""
        self.terms = ""
        self.terms_to_invoice = None
        self.notes_to_invoice = None
        self.warn_estimate_to_invoice = None
        self.is_sales_person_required = None
        self.default_template_id = ""
    
    def set_default_template_id(self, default_template_id): 
        """Set default template id.
       
        Args:
            default_template_id(str): Default template id.
 
        """
        self.default_template_id = default_template_id

    def get_default_template_id(self):
        """Get default template id.

        Returns: 
            str: Default template id.

        """ 
        return self.default_template_id       
 
    def set_auto_generate(self, auto_generate):
        """Set whether to enable or disable auto number generation.
 
        Args:
            auto_generate(bool): True to enable auto number generation.
  
        """
        self.auto_generate = auto_generate

    def get_auto_generate(self):
        """Get whether to enable or disable auto number generation.

        Returns:
            bool: True to enable auto number generation.

        """
        return self.auto_generate

    def set_prefix_string(self, prefix_string):
        """Set prefix string.

        Args:
            prefix_string(str): Prefix string.

        """
        self.prefix_string = prefix_string

    def get_prefix_string(self):
        """Get prefix string.
 
        Returns: 
            str: Prefix string.

        """
        return self.prefix_string

    def set_start_at(self, start_at):
        """Set start at.

        Args:
            start_at(int): Start at.

        """
        self.start_at = start_at

    def get_start_at(self):
        """Get start at.

        Returns:
            str: Get start at.

        """ 
        return self.start_at

    def set_next_number(self, next_number):
        """Set next number.

        Args:
            next_number(str): Next number.

        """
        self.next_number = next_number

    def get_next_number(self):
        """Get next number.

        Returns:
            str: Next number.

        """
        return self.next_number

    def set_quantity_precision(self, quantity_precision):
        """Set quantity precision.

        Args:
            quantity_precision(int): Quantity precision.

        """
        self.quantity_precision = quantity_precision

    def get_quantity_precision(self):
        """Get quantity precision.

        Returns:
            int: Quantity precision.

        """
        return self.quantity_precision

    def set_discount_type(self, discount_type):
        """Set discount type.

        Args:
            discount_type(str): Discount type.
 
        """
        self.discount_type = discount_type

    def get_discount_type(self):
        """Get discount type.

        Returns:
            str: Discount type.

        """
        return self.discount_type

    def set_is_discount_before_tax(self, is_discount_before_tax):
        """Set whether to discount before tax.

        Args:
            is_discount_before_tax(bool): True to discount before tax.

        """
        self.is_discount_before_tax = is_discount_before_tax

    def get_is_discount_before_tax(self):
        """Get whether to discount before tax.

        Returns:
            bool: True to discount before tax else false.

        """
        return self.is_discount_before_tax

    def set_reference_text(self, reference_text):
        """Set reference text.

        Args:
            reference_text(str): Reference text.

        """
        self.reference_text = reference_text

    def get_reference_text(self):
        """Get reference text.

        Returns:
            str: Reference text.

        """
        return self.reference_text

    def set_notes(self, notes):
        """Set notes.

        Args:
            notes(str): Notes.

        """
        self.notes = notes

    def get_notes(self):
        """Get notes.

        Returns:
            str: Notes.

        """
        return self.notes

    def set_terms(self, terms):
        """Set terms.

        Args:
            terms(str): Terms.

        """
        self.terms = terms

    def get_terms(self):
        """Get terms.

        Returns:
            str: Terms.

        """
        return self.terms

    def set_terms_to_invoice(self, terms_to_invoice):
        """Set terms to invoice.

        Args:
            terms_to_invoice(bool): True to determine whether terms and conditions field is to be copied from estimate to invoice else False.

        """
        self.terms_to_invoice = terms_to_invoice

    def get_terms_to_invoice(self):
        """Get terms to invoice.

        Returns: 
            bool: True to determine whether terms and conditions field is to be copied from estimate to invoice else False.

        """
        return self.terms_to_invoice

    def set_notes_to_invoice(self, notes_to_invoice):
        """Set notes to invoice.

        Args:
            notes_to_invoice(bool): True to determine whether customer notes field is to be copied from estimate to invoice.
 
        """
        self.notes_to_invoice = notes_to_invoice

    def get_notes_to_invoice(self):
        """Get notes to invoice.

        Returns:
            bool: True to determine whether customer notes field is to be copied from estimate to invoice.

        """
        return self.notes_to_invoice

    def set_warn_estimate_to_invoice(self, warn_estimate_to_invoice):
        """Set whether to warn while converting from estimate to invoice.

        Args:
            warn_estimate_to_invoice(bool): True to warn while converting from estiamte to invoice.

        """
        self.warn_estimate_to_invoice = warn_estimate_to_invoice

    def get_warn_estimate_to_invoice(self):
        """Get whether to warn while converting form estimate to invoice.

        Returns:
            bool: True to warn while converting from estimate to invoice.

        """
        return self.warn_estimate_to_invoice

    def set_is_sales_person_required(self, is_sales_person_required):
        """Set whether sales person is required.

        Args:
            is_sales_person_required(bool): True if sales person is required else false.

        """
        self.is_sales_person_required = is_sales_person_required

    def get_is_sales_person_required(self):
        """Get whether sales person is required.

        Returns:
            bool: True if sales person is required.

        """
        return self.is_sales_person_required

    def to_json(self):
        """This method is used to convert estimate setting object to json object.

        Returns:
            dict: Dictionary containing json object for estimate setting.

        """
        data = {}
        if self.auto_generate != None:
            data['auto_generate'] = self.auto_generate
        if self.prefix_string != "":
            data['prefix_string'] = self.prefix_string
        if self.start_at > 0:
            data['start_at'] = self.start_at
        if self.next_number != '':
            data['next_number'] = self.next_number
        if self.quantity_precision > 0:
            data['quantity_precision'] = self.quantity_precision
        if self.discount_type != '':
            data['discount_type'] = self.discount_type
        if self.reference_text != '':
            data['reference_text'] = self.reference_text
        if self.default_template_id != '':
            data['default_template_id'] = self.default_template_id
        if self.notes != '':
            data['notes'] = self.notes
        if self.terms != '':
            data['terms'] = self.terms
        if self.terms_to_invoice is not None:
            data['terms_to_invoice'] = self.terms_to_invoice
        if self.notes_to_invoice is not None:
            data['notes_to_invoice'] = self.notes_to_invoice
        if self.warn_estimate_to_invoice is not None: 
            data['warn_estimate_to_invoice'] = self.warn_estimate_to_invoice
        if self.is_sales_person_required is not None:
            data['is_sales_person_required'] = self.is_sales_person_required
        return data
