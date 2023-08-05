#$Id$

from books.model.PageContext import PageContext

class CustomerPaymentList:
    """This class is used to create object for customer payment list."""
    def __init__(self):
        """Initialize parameters for customer payments."""
        self.customer_payments = []
        self.page_context = PageContext()

    def set_customer_payments(self, customer_payments):
        """Set customer payments.
   
        Args:
            customer_payments(instance): Customer Payments object.

        """
        self.customer_payments.append(customer_payments)

    def get_customer_payments(self):
        """Get customer payments.
        
        Returns:
            list: List of customer payments object.

        """
        return self.customer_payments

    def set_page_context(self,page_context):
        """Set page context.

        Args: 
            page_context(instance): Page context object.

        """
        self.page_context=page_context

    def get_page_context(self):
        """Get page context.

        Returns:
            instance: page context object.
          
        """
        return self.page_context
 
