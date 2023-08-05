#$Id$

from books.model.PageContext import PageContext

class VendorPaymentList: 
    """This class is used to create object for vendor payments list."""
    def __init__(self):
        """Initialize the parameters for Vendor payments list."""
        self.vendor_payments = []
        self.page_context = PageContext()

    def set_vendor_payments(self, vendor_payments):
        """Set vendor payments.

        Args: 
            vendor_payments(instance): Vendor payments object.

        """
        self.vendor_payments.append(vendor_payments)

    def get_vendor_payments(self): 
        """Get vendor payments.

        Returns:
            list of instance: List of vendor payments object.
       
        """
        return self.vendor_payments

    def set_page_context(self, page_context):
        """Set page context.

        Args:
            page_context(instance): Page context object.

        """
        self.page_context = page_context

    def get_page_context(self):
        """Get page context.

        Returns:
            instance: Page context object.

        """
        return self.page_context

 
