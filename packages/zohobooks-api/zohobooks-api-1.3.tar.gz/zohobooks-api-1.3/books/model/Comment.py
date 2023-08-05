#$Id$

class Comment:
    """This class is used to create object for comments."""
    def __init__(self):
        """Initialize parameters for comments."""
        self.comment_id = ''
        self.contact_id = ''
        self.contact_name = ''
        self.description = ''
        self.commented_by_id = ''
        self.commented_by = ''
        self.date = ''
        self.date_description = ''
        self.time = ''
        self.transaction_id = ''
        self.transaction_type = ''
        self.is_entity_deleted = None
        self.operation_type = ''
        self.estimate_id = ''
        self.comment_type = ''
        self.invoice_id = ''
        self.payment_expected_date = ''
        self.show_comment_to_clients = None
        self.recurring_invoice_id = ''
        self.creditnote_id = ''
        self.expense_id = ''
        self.recurring_expense_id = ''
        self.bill_id = ''
        self.project_id = ''
        self.is_current_user = None

    def set_is_current_user(self, is_current_user):
        """Set whether it is current user or not.

        Args:
            is_current_user(bool): True if it is current user else false.

        """
        self.is_current_user = is_current_user

    def get_is_current_user(self):
        """Get whether it is current user or not.

        Returns:
            bool: True if it is current user else false.

        """
        return self.is_current_user
     
    def set_comment_id(self, comment_id):
        """Set comment id.
     
        Args:
            comment_id(str): Comment id.
 
        """
        self.comment_id = comment_id

    def get_comment_id(self):
        """Get comment id.
 
        Returns:
            str: Comment id.

        """
        return self.comment_id
  
    def set_contact_id(self, contact_id):
        """Set contact id.
        
        Args: 
            contact_id(str): Contact id.
  
        """
        self.contact_id = contact_id

    def get_contact_id(self):
        """Get contact id.
     
        Returns:
            str: Contact id.
 
        """
        return self.contact_id
   
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

    def set_description(self, description):
        """Set description.
     
        Args:
            description(str): Description.
 
        """
        self.description = description
 
    def get_description(self):
        """Get descritpion.

        Returns:
            str: Description.

        """
        return self.description

    def set_commented_by_id(self, commented_by_id):
        """Set commented by id.

        Args:
            commented_by_id(str): Commented by id.

        """
        self.commented_by_id = commented_by_id
 
    def get_commented_by_id(self):
        """Get commented by id.

        Returns:
            str: Commented by id.
        
        """
        return self.commented_by_id
  
    def set_commented_by(self, commented_by):
        """Set commented by.

        Args:
            commented_by(str): Commented by.

        """
        self.commented_by = commented_by

    def get_commented_by(self):
        """Get commented by.

        Returns: 
            str: Commented by.

        """
        return self.commented_by

    def set_date(self, date):
        """Set date.

        Args: 
            date(str): Date.

        """
        self.date = date

    def get_date(self):
        """Get date.

        Returns: 
            str: Date.
         
        """
        return self.date
   
    def set_date_description(self, date_description):
        """Set date description.
        
        Args: 
            date_description(str): Date description.

        """
        self.date_description = date_description
 
    def get_date_description(self):
        """Get date description.

        Returns:
            str: Date description.
 
        """
        return self.date_description

    def set_time(self, time):
        """Set time.
     
        Args:
            time(str): Time.
        
        """
        self.time = time

    def get_time(self):
        """Get time.

        Returns:
            str: Time.

        """
        return self.time     

    def set_transaction_id(self, transaction_id):
        """Set transaction id.
 
        Args:
            transaction_id(str): Transaction id.

        """
        self.transaction_id = transaction_id
 
    def get_transaction_id(self): 
        """Get transaction id.
 
        Returns:
            str: Transaction id.

        """
        return self.transaction_id

    def set_transaction_type(self, transaction_type):
        """Set transaction type.
         
        Args:
            transaction_type(str): Transaction type.

        """
        self.transaction_type = transaction_type

    def get_transaction_type(self):
        """Get transaction type.
 
        Returns:
            str: Transaction type.

        """
        return self.transaction_type
   
    def set_is_entity_deleted(self, is_entity_deleted):
        """Set whether entity is deleted or not.
 
        Args:  
            is_entity_deleted(bool): True if entity is deleted else False.
      
        """
        self.is_entity_deleted = is_entity_deleted

    def get_is_entity_deleted(self):
        """Get whether entity is deleted or not.

        Returns: 
            bool: True if entity is deleted else False.

        """
        return self.is_entity_deleted
    
    def set_operation_type(self, operation_type):
        """Set operation type.
     
        Args: 
            operatipon_type(str): Operation type.

        """
        self.operation_type = operation_type
 
    def get_operation_type(self):
        """Get operation type.
        
        Returns:
            str: Operation type.
 
        """
        return self.operation_type
   
    def set_comment_type(self, comment_type):
        """Set comment type.

        Args: 
            comment_type(Str): Comment type.

        """  
        self.comment_type = comment_type

    def get_comment_type(self):
        """Get comment type.
     
        Returns:
            str: Comment type.

        """
        return self.comment_type

    def set_estimate_id(self, estimate_id):
        """Set estimate id.
 
        Args:
            estimate_id(str): Estimate id.

        """
        self.estimate_id = estimate_id

    def get_estimate_id(self):
        """Get estimate id.
 
        Returns: 
            str: Estimate id.

        """
        return self.estimate_id

    def set_invoice_id(self, invoice_id):
        """Set invoice id.
        
        Args:
            invoice_id(str): Invoice id.

        """
        self.invoice_id = invoice_id

    def get_invoice_id(self):
        """Get invoice id.

        Returns:
            str: Invoice id.

        """
        return self.invoice_id

    def set_payment_expected_date(self, payment_expected_date):
        """Set payment expected date.
 
        Args: 
            payment_expected_date(str): Payment expected date.

        """
        self.payment_expected_date = payment_expected_date

    def get_payment_expected_date(self):
        """Get payment expected date.

        Returns:
            str: Payment expected date.

        """
        return self.payment_expected_date

    def set_show_comment_to_clients(self, show_comment_to_clients):
        """Set whether to show comment to clients.

        Args:
            show_comment_to_client(bool): True to show comment to 
                clients else False.

        """
        self.show_comment_to_clients = show_comment_to_clients

    def get_show_comment_to_clients(self):
        """Get whether to show comment to clients.

        Returns:
            bool: True to show comment to clients else False.
 
        """
        return self.show_comment_to_clients


    def set_recurring_invoice_id(self, recurring_invoice_id):
        """Set recurring invoice id.
 
        Args: 
            recurring_invoice_id(str): Recurring invoice id.
      
        """ 
        self.recurring_invoice_id = recurring_invoice_id

    def get_recurring_invoice_id(self):
        """Get recurring invoice id.
       
        Returns:
            str: Recurring invoice id.
     
        """
        return self.recurring_invoice_id
  
    def set_creditnote_id(self, creditnote_id):
        """Set creditnote id.

        Args:
            creditnote_id (str): Creditnote id.
 
        """
        self.creditnote_id = creditnote_id
 
    def get_creditnote_id(self):
        """Get creditnote id.
 
        Args:
            str: Creditnote id.

        """
        return self.creditnote_id
   
    def set_expense_id(self, expense_id):
        """Set expense id.

        Args:
            expense_id(str): Expense id.

        """
        self.expense_id = expense_id

    def get_expense_id(self): 
        """Get expense id.
 
        Returns:
            str: Expense id.

        """
        return self.expense_id

    def set_recurring_expense_id(self, recurring_expense_id): 
        """Set recurring expense id.

        Args:
            recurring_expense_id(str): Recurring expense id.

        """
        self.recurring_expense_id = recurring_expense_id

    def get_recurring_expense_id(self):
        """Get recurring expense id.

        Returns:
            str: Recurring expense id.

        """
        return self.recurring_expense_id

    def set_bill_id(self, bill_id):
        """Set bill id.

        Args:
            bill_id(str): Bill id.

        """
        self.bill_id = bill_id

    def get_bill_id(self):
        """Get bill id.

        Returns:
            str: Bill id.

        """
        return self.bill_id

    def set_project_id(self, project_id):
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

