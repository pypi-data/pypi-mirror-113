#$Id$

class PaymentList:
    """This class is used to create object for payment list."""
    def __init__(self):
        """Initialize parameters for Payment list object."""
        self.payments = []

    def set_payments(self, payment):
        """Set payments.

        Args: 
            payment(instance): Payment object.

        """
        self.payments.append(payment)
   
    def get_payments(self):
        """Get payment.

        Returns:
            list of instance: List of payment object.

        """
        return self.payments
