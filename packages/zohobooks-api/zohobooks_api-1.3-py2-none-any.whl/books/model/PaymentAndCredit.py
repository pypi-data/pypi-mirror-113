#$Id$

class PaymentAndCredit:
    """This class is used to create object for Payments and Credits."""
    def __init__(self): 
        """Initialize parameters for payments and credits."""
        self.invoice_payments=[]
        self.apply_creditnotes=[]

    
    def set_payments(self,payments):
        """Set payments.

        Args:
            payments(instace): Payemnts object.

        """
        self.invoice_payments.append(payments)

    def get_payments(self):
        """Get payments.

        Returns:
            instance: Payments object.

        """
        return self.invoice_payments

    def set_apply_creditnotes(self,credits):
        """Set apply creditnotes.
 
        Args:
            credits(instance): Credits object.

        """
        self.apply_creditnotes.append(credits)

    def get_apply_creditnotes(self):
        """Get apply creditnotes.

        Returns:
            instance: Credits object.
        
        """
        return self.apply_creditnotes

   
