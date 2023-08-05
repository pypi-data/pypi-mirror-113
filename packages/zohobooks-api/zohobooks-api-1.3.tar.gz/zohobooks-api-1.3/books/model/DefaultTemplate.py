#$Id$

class DefaultTemplate:
    """This class is used to create object for default templates."""
    def __init__(self):
        """Initialize the parameters for default temmplates."""
        self.invoice_template_id = ''
        self.invoice_template_name = ''
        self.estimate_template_id = ''
        self.estimate_template_name = ''
        self.creditnote_template_id = ''
        self.creditnote_template_name = ''
        self.invoice_email_template_id = ''
        self.invoice_email_template_name = ''
        self.estimate_email_template_id = ''
        self.estimate_email_template_name = ''
        self.creditnote_email_template_id = ''
        self.creditnote_email_template_name = ''
                               
    def set_invoice_template_id(self, invoice_template_id):
        """Set default invoice template id used for this contact while 
            creating invoice.
    
        Args:
            invoice_template_id(str): Default invoice template id used for this
                contact while creating invoice.

        """
        self.invoice_template_id = invoice_template_id

    def get_invoice_template_id(self):
        """Get default invoice template id used for this contact while 
            creating invoice.
          
        Returns:
            str: Default invoice template id used for this contact while 
                creating invoice.
 
        """
        return self.invoice_template_id

    def set_invoice_template_name(self, invoice_template_name):
        """Set default invoice template name used for this contact while 
            creating invoice.
         
        Args:
            invoice_template_name(str): Default invoice template name used for 
                this contact while creating invoice.
  
        """
        self.invoice_template_name = invoice_template_name

    def get_invoice_template_name(self):
        """Get default invoice template name used for this contact while 
            creating invoice.
  
        Returns:
            str: Default invoice template name used for this contact while 
                creating invoice.
 
        """
        return self.invoice_template_name
  
    def set_estimate_template_id(self, estimate_template_id):
        """Set default estimate template id used for this contact while creating 
            estimate.
        
        Args:
            estimate_template_id(str): Default estimate template id used for  
                this contact while creating estimate.
 
        """
        self.estimate_template_id = estimate_template_id

    def get_estimate_template_id(self):
        """Get default estimate template id used for this contact while 
            creating estimate.
 
        Returns:
            str: Default estimate template id used for this contact while 
                creating estimate.
 
        """
        return self.estimate_template_id
  
    def set_estimate_template_name(self, estimate_template_name):
        """Set default estimate template name used for this contact while 
            creating estimate.
        
        Args: 
            estimate_template_name(str): Default estimate template name used 
                for this contact while creating estimate.

        """     
        self.estimate_template_name = estimate_template_name

    def get_estimate_template_name(self):
        """Get default estimate template name used for this contact while 
            creating estimate.
 
        Returns:
            str: Default estimate template name used for this contact while 
                creating estimate.
   
        """ 
        return self.estimate_template_name

    def set_creditnote_template_id(self, creditnote_template_id):
        """Set default creditnote template id used for this contact while 
            creating creditnote.
  
        Args: 
            creditnote_template_id(str): Default creditnote template id used 
                for this contact while creating creditnote.

        """ 
        self.creditnote_template_id = creditnote_template_id

    def get_creditnote_template_id(self):
        """Get default creditnote template id used for this contact while 
            creating creditnote.
   
        Returns: 
            str: Default creditnote template id used for this contact while 
                creating creditnote.
 
        """
        return self.creditnote_template_id
  
    def set_creditnote_template_name(self, creditnote_template_name):
        """Set default creditnote template name used for this contact while 
            creating creditnote.
  
        Args: 
            creditnote_template_name(str): Default creditnote template name 
                used for this contact while creating creditnote.

        """ 
        self.creditnote_template_name = creditnote_template_name

    def get_creditnote_template_name(self):
        """Get default creditnote template id used for this contact while 
            creating creditnote.
   
        Returns: 
            str: Default creditnote template id used for this contact while 
                creating creditnote.
 
        """
        return self.creditnote_template_name

    def set_invoice_email_template_id(self, invoice_email_template_id):
        """Set default invoice email template id used for this contact while 
            creating invoice.
        
        Args: 
            invoice_email_template_id(str): Default invoice template id used 
                for this contact while creating invoice

        """
        self.invoice_email_template_id = invoice_email_template_id

    def get_invoice_email_template_id(self):
        """Get default invoice email template id used for this contact while 
            creating invoice.
         
        Returns: 
            str: Default invoice email template id used for this contact while 
                creating invoice.
         
        """
        return self.invoice_email_template_id

    def set_invoice_email_template_name(self, invoice_email_template_name):
        """Set default invoice email template name used for this contact while 
            creating invocie.

        Args: 
            invoice_email_template_name(str): Default invoice email template 
                name used for this contact while creating invocie.

        """ 
        self.invoice_email_template_name = invoice_email_template_name
 
    def get_invoice_email_template_name(self):
        """Get default invoice email template name used for this contact while 
            creating invoice.
 
        Returns: 
            str: Default invoice email template name used for this contact while 
                creating invoice.
 
        """
        return self.invoice_email_template_name

    def set_estimate_email_template_id(self, estimate_email_template_id):
        """Set default estimate template id used for this contact while 
            creating estimate.
 
        Args: 
            estimate_email_template_id(str): Default estimate template id 
                used for this cotnact while creating estimate.
 
        """
        self.estimate_email_template_id = estimate_email_template_id
 
    def get_estimate_email_template_id(self):
        """Get default estimate email template id used for this contact while 
            creating estimate.
 
        Returns:
            str: Default estimate template id used for this cotnact while 
                creating estimate.
 
        """
        return self.estimate_email_template_id

    def set_estimate_email_template_name(self, estimate_email_template_name):
        """Set default estimate email template name used for this contact 
            while creating estimate.
        
        Args:
            estimate_email_template_name(str): Default estimate email template 
                name used for this contact while ccreating estimate.
 
        """
        self.estimate_email_template_name = estimate_email_template_name

    def get_estimate_email_template_name(self):
        """Get default estimate email template name used for this contact while
             creating estimate.
       
        Returns: 
            str: Default estimate email template name used for this contact
                while creating estimate.

        """
        return self.estimate_email_template_name
   
    def set_creditnote_email_template_id(self, creditnote_email_template_id):
        """Set default creditnote email template id used for this contact while
             creating creditnote.
 
        Args:
            creditnote_email_template_id(str): Default creditnote email 
                template id used for this contact while creating creditnote.
 
        """
        self.creditnote_email_template_id = creditnote_email_template_id

    def get_creditnote_email_template_id(self):
        """Get default creditnote email template id used for this contact while 
            creating creditnote.
        
        Returns:
            str: Default creditnote email template id used for this contact 
                while creating creditnote.

        """ 
        return self.creditnote_email_template_id

    def set_creditnote_email_template_name(self, 
                                           creditnote_email_template_name):
        """Set default creditnote email template name used for this contact 
            while creating creditnote.
 
        Args:
            creditnote_email_template_name(str): Default creditnote email 
                template name used for this contact while creating creditnote.
 
        """
        self.creditnote_email_template_name = creditnote_email_template_name

    def get_creditnote_email_template_name(self):
        """Get default creditnote email template name used for this contact 
            while creating creditnote.
        
        Returns:
            str: Default creditnote email template name used for this contact 
                while creating creditnote.

        """ 
        return self.creditnote_email_template_name
  

                        
    

