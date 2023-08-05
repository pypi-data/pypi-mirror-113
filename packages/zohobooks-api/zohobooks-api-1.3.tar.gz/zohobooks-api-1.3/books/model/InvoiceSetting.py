#$Id$

class InvoiceSetting:
    """This class is used to create object for invoice settings."""
    def __init__(self):
        """Initialize parameters for Invoice settings."""
        self.auto_generate = None
        self.prefix_string = ''
        self.start_at = 0
        self.next_number = ''
        self.quantity_precision = 0 
        self.discount_type = ''
        self.is_discount_before_tax = None
        self.reference_text = ''
        self.default_template_id = ''
        self.notes = ''
        self.terms = ''
        self.is_shipping_charge_required = None
        self.is_adjustment_required = None
        self.is_open_invoice_editable = None
        self.warn_convert_to_open = None
        self.warn_create_creditnotes = None
        self.attach_expense_receipt_to_invoice = ''
        self.invoice_item_type = ''
        self.is_sales_person_required = None
        self.is_show_invoice_setup = None
        self.discount_enabled = None

    def set_discount_enabled(self, discount_enabled):
        """Set discount enabled.

        Args:
            discount_enabled(str): Discount enabled.

        """
        self.discount_enabled = discount_enabled

    def get_discount_enabled(self):
        """Get discount enabled.

        Returns:
            str: Discount enabled.

        """
        return self.discount_enabled

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
        """Set auto generate. 

        Args:
            auto_generate(bool): Auto generate.

        """
        self.auto_generate = auto_generate

    def get_auto_generate(self):
        """Get auto generate.

        Returns:
            bool: Auto generate.
       
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
            int: Start at.

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
        """Set whether it is discount before tax.

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

    def set_is_shipping_charge_required(self, is_shipping_charge_required):
        """Set whether shipping charge is required or not.

        Args:
            is_shipping_charge_required(bool): True if shipping charge is 
                required else false.

        """
        self.is_shipping_charge_required = is_shipping_charge_required

    def get_is_shipping_charge_required(self):
        """Get whether shipping charge is required or not.

        Returns:
            bool: True if shipping charge is required or not.

        """
        return self.is_shipping_charge_required

    def set_is_adjustment_required(self, is_adjustment_required):
        """Set whether adjustment is required.
 
        Args:
            is_adjustment_required(bool): True if adjustment is required else 
                false.
         
        """
        self.is_adjustment_required = is_adjustment_required

    def get_is_adjustment_required(self):
        """Get whether adjustment is required.

        Returns:
            bool: True if adjustment is required.

        """ 
        return self.is_adjustment_required

    def set_is_open_invoice_editable(self, is_open_invoice_editable):
        """Set whether open invoice editable.

        Args:
            is_open_invoice_editable(bool): True if open invoice editable else 
                false.

        """
        self.is_open_invoice_editable = is_open_invoice_editable

    def get_is_open_invoice_editable(self):
        """Get whether open invoice editable.
 
        Returns:
            bool: True if open invoice editable else false.

        """
        return self.is_open_invoice_editable

    def set_warn_convert_to_open(self, warn_convert_to_open):
        """Set whether to enable warning while converting to open.

        Args:
            warn_convert_to_open(bool): True to warn while converting to open 
                else false.

        """
        self.warn_convert_to_open = warn_convert_to_open

    def get_warn_convert_to_open(self):
        """Get whether to enable warning while converting to open.

        Returns:
            bool: True if warning while converting to open is enabled else 
                false.

        """
        return self.warn_convert_to_open

    def set_warn_create_creditnotes(self, warn_create_creditnotes):
        """Set whether to enable warning while creating creditnotes.

        Args: 
            warn_create_creditnotes(bool): True to warn while creating 
                creditnotes else false.

        """
        self.warn_create_creditnotes = warn_create_creditnotes

    def get_warn_create_creditnotes(self):
        """Get whether warning while creating creditnotes is enabled or not.

        Returns:
            bool: True to warn while creating creditnotes else false.

        """
        return self.warn_create_creditnotes

    def set_attach_expense_receipt_to_invoice(self, \
        attach_expense_receipt_to_invoice):
        """Set attach expense receipt to invoice.

        Args:
            attach_expense_receipt_to_invoice(str): Attach expense receipt to 
                invoice.

        """
        self.attach_expense_receipt_to_invoice = \
        attach_expense_receipt_to_invoice
   
    def get_attach_expense_receipt_to_invoice(self):
        """Get attach expense receipt to invoice.

        Returns:
            str: Attach expense receipt to invoice.

        """
        return self.attach_expense_receipt_to_invoice

    def set_is_open_invoice_editable(self, is_open_invoice_editable):
        """Set whether to open invoice editable.

        Args:
            is_open_invoice_editable(bool): True to open invoice editable else 
                false.

        """
        self.is_open_invoice_editable = is_open_invoice_editable

    def get_is_open_invoice_editable(self): 
        """Get whether to open invoice editable.

        Returns:
            bool: True to open invoice editable else false.

        """
        return self.is_open_invoice_editable

    def set_is_sales_person_required(self, is_sales_person_required):
        """Set whether sales person is required or not.

        Args:
            is_sales_person_required(bool): True if sales person is required 
                else false.

        """
        self.is_sales_person_required = is_sales_person_required

    def get_is_sales_person_required(self):
        """Get whether sales person is required or not.

        Returns:
            bool: True if sales person is required else false.

        """
        return self.is_sales_person_required

    def set_is_show_invoice_setup(self, is_show_invoice_setup):
        """Set whether to show invoice setup.

        Args:
            is_show_invoice_setup(bool): True to show invoice setup.

        """
        self.is_show_invoice_setup = is_show_invoice_setup

    def get_is_show_invoice_setup(self):
        """Get whether to show invoice setup.
 
        Returns: 
            bool: True to show invoice setup.
 
        """
        return self.is_show_invoice_setup

    def set_invoice_item_type(self, invoice_item_type):
        """Set invoice item type.

        Args:
            invoice_item_type(str): Invoice item type.

        """
        self.invoice_item_type = invoice_item_type

    def get_invoice_item_type(self):
        """Get invoice item type.

        Returns:
            str: Invoice item type.

        """
        return self.invoice_item_type

    def to_json(self): 
        """This method is used to convert invoice settings in json format.

        Returns:    
            dict: Dictionary containing json object for invoice settings.

        """
        data = {}
        if self.auto_generate is not None:
            data['auto_generate'] = self.auto_generate
        if self.prefix_string != None:
            data['prefix_string'] = self.prefix_string
        if self.start_at > 0:
            data['start_at'] = self.start_at
        if self.next_number != '':
            data['next_number'] = self.next_number
        if self.quantity_precision > 0:
            data['quantity_precision'] = self.quantity_precision
        if self.discount_enabled is not None:
            data['discount_enabled'] = self.discount_enabled
        if self.reference_text != '':
            data['reference_text'] = self.reference_text 
        if self.default_template_id != '':
            data['default_template_id'] = self.default_template_id
        if self.notes != '':
            data['notes'] = self.notes
        if self.terms != '':
            data['terms'] = self.terms
        if self.is_shipping_charge_required is not None:
            data['is_shipping_charge_required'] = \
                self.is_shipping_charge_required
        if self.is_adjustment_required is not None:
            data['is_adjustment_required'] = \
                self.is_adjustment_required
        if self.invoice_item_type != '':
            data['invoice_item_type'] = self.invoice_item_type
        if self.discount_type != '':
            data['discount_type'] = self.discount_type
        if self.warn_convert_to_open is not None: 
            data['warn_convert_to_open'] = self.warn_convert_to_open
        if self.warn_create_creditnotes is not None:
            data['warn_create_creditnotes'] = self.warn_create_creditnotes
        if self.is_open_invoice_editable is not None:
            data['is_open_invoice_editable'] = self.is_open_invoice_editable
        if self.is_sales_person_required is not None:
            data['is_sales_person_required'] = self.is_sales_person_required
        return data

         
