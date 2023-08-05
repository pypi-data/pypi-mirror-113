#$Id$

class CreditNoteRefund:
    """This class is used to create object for creditnotes refund."""
    def __init__(self):
        """Initialize parameters for creditnotes refund object."""
        self.date = ''
        self.refund_mode = ''
        self.reference_number = ''
        self.amount = 0.0
        self.exchange_rate = 0.0
        self.from_account_id = ''
        self.from_account_name = ''
        self.description = ''
        self.creditnote_refund_id = ''
        self.creditnote_id = ''
        self.creditnote_number = ''
        self.customer_name = ''
        self.amount_bcy = ''
        self.amount_fcy = ''

    def set_date(self, date):
        """Set the date at which the credit note is created.
        
        Args:
            date(str): Date.
        
        """
        self.date = date

    def get_date(self):
        """Get date at which the credit note is created.
        
        Returns:
            str: Date.

        """ 
        return self.date
  
    def set_refund_mode(self, refund_mode):
        """Set the mode of refund for the credit note refund amount.
       
        Args:
            refund_mode(str): Refund mode .
 
        """
        self.refund_mode = refund_mode
 
    def get_refund_mode(self):
        """Get the mode of refund for the credit note refund amount.
 
        Returns:
            str: Refund mode.

        """
        return self.refund_mode
   
    def set_reference_number(self, reference_number):
        """Set reference number for the refund recorded.
        
        Args:
            reference_number(str): Reference number.
       
        """
        self.reference_number = reference_number
 
    def get_reference_number(self):
        """Get reference number for the refund recorded.
       
        Returns:
            str: Reference number.
       
        """
        return self.reference_number
  
    def set_amount(self, amount):
        """Set amount refunded from the credit note.
        
        Args:
            amount(float): Amount.
  
        """
        self.amount = amount

    def get_amount(self):
        """Get amount refunded from the credit note.
      
        Returns:
            float: Amount.
   
        """
        return self.amount
 
    def set_exchange_rate(self, exchange_rate):
        """Set exchange rate of the currency.
         
        Args: 
            exchange_rate(float): Exchange rate.
        
        """
        self.exchange_rate = exchange_rate
 
    def get_exchange_rate(self):
        """Get exchange rate of the currency.
        
        Returns:
            float: Exchange rate.
            
        """
        return self.exchange_rate
   
    def set_from_account_id(self, from_account_id):
        """Set the account id from which credit note is refunded.
       
        Args:
            from_account_id(str): The account id from which credit note is 
                refunded.

        """
        self.from_account_id = from_account_id

    def get_from_account_id(self):
        """Get the account id from which credit note is refunded.
 
        Returns:
            str: The account id from which credit note is refunded.
         
        """
        return self.from_account_id
   
    def set_description(self, description):
        """Set description for the refund.
        
        Args:
            description(str): Description for the refund.

        """
        self.description = description
 
    def get_description(self):
        """Get descriptioon for the refund.
   
        Returns:
            str: Description for the refund.

        """
        return self.description

    def set_creditnote_refund_id(self, creditnote_refund_id):
        """Set creditnote refund id.
        
        Args:
            creditnote_refund(str): Id of the creditnote refund.
        
        """
        self.creditnote_refund_id = creditnote_refund_id

    def get_creditnote_refund_id(self):
        """Get creditnote refund id.
        
        Returns:
            str: Id of the creditnote refund.
 
        """
        return self.creditnote_refund_id
  
    def set_creditnote_id(self, creditnote_id):
        """Set credit note id.
          
        Args:
            creditnote_id(str): Id of the creditnote.
 
        """
        self.creditnote_id = creditnote_id
 
    def get_creditnote_id(self):
        """Get Id of the credit note.
         
        Returns:
            str: Id of the creditnote.

        """ 
        return self.creditnote_id
  
    def set_from_account_name(self, from_account_name):
        """Set account name from which credit note is refunded.
       
        Args:
            from_account_name(str): Account name from which credit note is 
                refunded.
       
        """ 
        self.from_account_name = from_account_name

    def get_from_account_name(self):
        """Get account name from which credit note is refunded.
       
        Returns:
            str: Account name from which credit note is refunded.
       
        """ 
        return self.from_account_name

    def set_creditnote_number(self, creditnote_number):
        """Set creditnote number of the creditnote.
  
        Args:
            creditnote_number(str): Creditnote number of creditnote.

        """
        self.creditnote_number = creditnote_number

    def get_creditnote_number(self):
        """Get creditnote number of the creditnote.
         
        Returns:
            str: Creditnote number of creditnote.
     
        """
        return self.creditnote_number

    def set_customer_name(self, customer_name):
        """Set customer name.
       
        Args:
            customer_name(str): Customer name.
     
        """
        self.customer_name = customer_name

    def get_customer_name(self):
        """Get customer name.
        
        Returns:
            str: Customer name.
        
        """
        return self.customer_name

    def set_amount_bcy(self, amount_bcy):
        """Set amount bcy.
      
        Args:
            amount_bcy(str): Amount_bcy.
      
        """
        self.amount_bcy = amount_bcy
 
    def get_amount_bcy(self):
        """Get amount bcy.
      
        Returns:
            str: Amount_bcy.

        """
        return self.amount_bcy
  
    def set_amount_fcy(self, amount_fcy):
        """Set amount fcy.
        
        Args: 
            amount_fcy(str): Amount fcy.

        """
        self.amount_fcy = amount_fcy

    def get_amount_fcy(self):
        """Get amount fcy.
      
        Returns: 
            str: Amount fcy.

        """    
        return self.amount_fcy

    def to_json(self):
        """This method is used to convert creditnote refund object to json object.

        Returns:
            dict: Dictionary containing json object for credit note refund.

        """
        data = {}
        if self.date != '':
            data['date'] = self.date
        if self.refund_mode != '':
            data['refund_mode'] = self.refund_mode
        if self.reference_number != '':
            data['reference_number'] = self.reference_number
        if self.amount > 0:
            data['amount'] = self.amount
        if self.exchange_rate > 0 :
            data['exchange_rate'] = self.exchange_rate
        if self.from_account_id != '':
            data['from_account_id'] = self.from_account_id
        if self.description != '':
            data['description'] = self.description
        if self.creditnote_id != '':
            data['creditnote_id'] = self.creditnote_id
        return data

  

