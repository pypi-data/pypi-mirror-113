#$Id$

class LineItem:
    """This class is used to create object for line items."""
    def __init__(self):
        """Initialize the parameters for line items."""
        self.item_id = ''
        self.line_item_id = ''
        self.name = ''
        self.description = ''
        self.item_order = 0
        self.bcy_rate = 0.0
        self.rate = 0.00
        self.quantity = 0
        self.unit = ''
        self.discount = 0.00
        self.tax_id = ''
        self.tax_name = ''
        self.tax_type = ''
        self.tax_percentage = 0.0
        self.item_total = 0.0
        self.expense_id = ''
        self.expense_item_id = ''
        self.expense_receipt_name = ''
        self.time_entry_ids = ''
        self.project_id = ''
        self.account_id = ''
        self.account_name = ''
        self.line_id = ''
        self.debit_or_credit = ''
        self.amount = 0.0
        self.discount_amount = 0.0
        self.hsn_or_sac = ''

    def set_hsn_or_sac(self,hsn_or_sac):
        """Set hsn_or_sac.

        Args:
            hsn_or_sac(str): hsn_or_sac.

        """
        self.hsn_or_sac = hsn_or_sac

    def get_hsn_or_sac(self):
        """Get hsn_or_sac.
 
        Returns:
            str: hsn_or_sac.

        """
        return self.hsn_or_sac
  
    def set_item_id(self,item_id):
        """Set item id.

        Args:
            item_id(str): Item id.

        """
        self.item_id = item_id

    def get_item_id(self):
        """Get item id.

        Returns:
            str: Item id.

        """
        return self.item_id

    def set_line_item_id(self,line_item_id):
        """Set line item id.

        Args:
            line_item_id(str): line_item_id

        """
        self.line_item_id = line_item_id
 
    def get_line_item_id(self):
        """Get line item id.

        Returns:
            str: line item id.

        """
        return self.line_item_id
  
    def set_name(self,name):
        """Set name of the line item.

        Args: 
            name(str): Name of the line item.

        """
        self.name = name

    def get_name(self):
        """Get name of the line item.

        Returns:
            str: Name of the line item.

        """
        return self.name
   
    def set_description(self,description):
        """Set description of the line item.

        Args:
            description(str): Description of the line item.

        """
        self.description = description
 
    def get_description(self):
        """Get description of the line item.

        Returns:
            str: Descritpion of the line item.

        """
        return self.description
  
    def set_item_order(self,item_order):
        """Set item order.

        Args:
            item_order(int): Item order.

        """
        self.item_order = item_order

    def get_item_order(self):
        """Get item order.

        Returns:
            int: Item order.

        """
        return self.item_order
  
    def set_bcy_rate(self,bcy_rate):
        """Set bcy rate.

        Args: 
            bcy_rate(float): Bcy rate.

        """
        self.bc_rate = bcy_rate

    def get_bcy_rate(self):
        """Get bcy rate.

        Returns:
            float: Bcy rate.

        """
        return self.bcy_rate
  
    def set_rate(self,rate):
        """Set rate.

        Args:
            rate(float): Rate.

        """
        self.rate = rate

    def get_rate(self):
        """Get rate.

        Returns:
            float: Rate.

        """
        return self.rate
 
    def set_quantity(self,quantity):
        """Set quantity.

        Args:
            quantity(float): Quantity.
     
        """ 
        self.quantity = quantity

    def get_quantity(self):
        """Get quantity.

        Returns:
            float: Quantity.

        """
        return self.quantity
  
    def set_unit(self,unit):
        """Set unit.

        Args: 
            unit(str): Unit.

        """
        self.unit = unit

    def get_unit(self):
        """Get unit.

        Returns:
            str: Unit.

        """
        return self.unit
  
    def set_discount(self,discount):
        """Set discount.

        Args: 
            discount(str): Discount.

        """
        self.discount = discount

    def get_discount(self):
        """Get discount.

        Returns:
            str:  Discount.

        """
        return self.discount
  
    def set_tax_id(self,tax_id):
        """Set tax id.
 
        Args:
            tax_id(str): Tax id.

        """
        self.tax_id = tax_id

    def get_tax_id(self):
        """Get tax id.

        Returns:
            str: Tax id.

        """
        return self.tax_id
  
    def set_tax_name(self,tax_name):
        """Set tax name.

        Args: 
            tax_name(str): Tax name.

        """
        self.tax_name = tax_name

    def get_tax_name(self):
        """Get tax name.

        Returns: 
            str: Tax name.

        """
        return self.tax_name
  
    def set_tax_type(self,tax_type):
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
  
    def set_tax_percentage(self,tax_percentage):
        """Set tax percentage.

        Args:
            tax_percentage(str): Tax percentage.

        """
        self.tax_percentage = tax_percentage

    def get_tax_percentage(self):
        """Get tax percentage.

        Returns:
            str: Tax percentage.

        """
        return self.tax_percentage

    def set_item_total(self,item_total):
        """Set item total.

        Args: 
            item_total(int): Item total.

        """
        self.item_total = item_total

    def get_item_total(self):
        """Get item total.

        Returns:
            int: Item total.

        """
        return self.item_total

    def set_expense_id(self,expense_id):
        """Set expense id.

        Args:
            expense_id(str): Expense id.

        """
        self.expense_id = expense_id

    def get_expense_id(self):
        """Get expense id.

        Args:
            expense_id(str): Expense id.

        """
        return self.expense_id
   
    def set_expense_item_id(self,expense_item_id):
        """Set expense item id.

        Args:
            expense_item_id(str): Expense item id.

        """
        self.expense_item_id = expense_item_id

    def get_expense_item_id(self):
        """Get expense item id.

        Returns:
            str: Expense item id.

        """
        return self.expense_item_id

    def set_expense_receipt_name(self,expense_receipt_name):
        """Set expense receipt name.

        Args:
            expense_receipt_name(str): Expense receipt name.

        """
        self.expense_receipt_name = expense_receipt_name

    def get_expense_receipt_name(self):
        """Get expense receipt name.

        Returns:
            str: Expense receipt name.

        """
        return self.expense_receipt_name
 
    def set_time_entry_ids(self,time_entry_ids):
        """Set time entry ids.

        Args: 
            time_entry_ids(str): Time entry ids.

        """
        self.time_entry_ids = time_entry_ids

    def get_time_entry_ids(self):
        """Get time entry ids.

        Returns:
            str: Time entry ids.

        """
        return self.time_entry_ids
  
    def set_project_id(self,project_id):
        """Set project id.
 
        Args:
            project_id(str): Project id.

        """
        self.project_id = project_id

    def get_project_id(self):
        """Get project id.
 
        Returns:
            str: Project id.

        """
        return self.project_id
  
    def set_account_id(self,account_id):
        """Set account id.
       
        Args:
            account_id(str): Account id.

        """
        self.account_id = account_id

    def get_account_id(self):
        """Get account id.

        Returns:
            str: Account id.

        """
        return self.account_id
   
    def set_account_name(self,account_name):
        """Set account name.

        Args:
            account_name(str): Account name.
 
        """
        self.account_name = account_name

    def get_account_name(self):
        """Get account name.
 
        Returns:
            str: Account name.

        """
        return self.account_name

    def set_line_id(self,line_id):
        """Set line id.

        Args:
            line_id(str): Line id.

        """
        self.line_id = line_id

    def get_line_id(self):
        """Get line id.

        Returns:
            str: Line id.

        """
        return self.line_id
  
    def set_debit_or_credit(self,debit_or_credit):
        """Set debit or credit.

        Args:
            debit_or_credit(str): Debit or credit.

        """
        self.debit_or_credit = debit_or_credit
 
    def get_debit_or_credit(self):
        """Get debit or credit.

        Returns:
            str: Debit or credit.

        """
        return self.debit_or_credit

    def set_amount(self, amount):
        """Set amount.

        Args: 
            amount(float): Amount.

        """
        self.amount = amount

    def get_amount(self): 
        """Get amount.

        Returns:
            float: Amount.

        """
        return self.amount

    def set_discount_amount(self,discount_amount):
        """Set discount amount.

        Args:
            discount_amount(float): Discount amount.

        """
        self.discount_amount = discount_amount

    def get_discount_amount(self):
        """Get discount amount.

        Returns:
            float: Discount amount.

        """
        return self.discount_amount

    def to_json(self):
        """This method is used to create json object for line items.

        Returns:
            dict: Dictionary containing json object for line items.

        """
        line_item = {}
        if self.item_id != '':
            line_item['item_id'] = self.item_id
        if self.account_id != '':
            line_item['account_id'] = self.account_id
        if self.name != '':
            line_item['name'] = self.name
        if self.description != '':
            line_item['description'] = self.description
        if self.unit != '':
            line_item['unit'] = self.unit
        if self.rate != None:
            line_item['rate'] = self.rate
        if self.item_order != None:
            line_item['item_order'] = self.item_order
        if self.quantity != None:
            line_item['quantity'] = self.quantity
        if self.discount is not None:
            line_item['discount'] = self.discount
        if self.tax_id != '':
            line_item['tax_id'] = self.tax_id
        if self.amount > 0:
            line_item['amount'] = self.amount
        if self.debit_or_credit != '':
            line_item['debit_or_credit'] = self.debit_or_credit
        if self.hsn_or_sac != '':
            line_item['hsn_or_sac'] = self.hsn_or_sac
        return line_item
