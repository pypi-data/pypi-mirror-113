#$Id$

class CreditNoteRefundList:
    """This class is used to create object for Creditnotes Refund."""
    def __init__(self):
        """Initialize parameters for creditnotes refund list."""
        self.creditnote_refunds=[]
        self.page_context={}
   
    def set_creditnote_refunds(self, creditnote_refunds):
        """Set creditnote refunds.
   
        Args:
            creditnote_refunds(instance): Creditnote refunds object.
 
        """
        self.creditnote_refunds.append(creditnote_refunds)
 
    def get_creditnote_refunds(self):
        """Get creditnote refunds
        
        Returns:
            list: List of creditnote refunds.

        """
        return self.creditnote_refunds

    def set_page_context(self, page_context):
        """Set page context.
        
        Returns:
            page_context(instance): Page context object.
 
        """
        self.page_context=page_context

    def get_page_context(self):
        """Get page context.

        Returns:
            instance: Page context object.

        """
        return self.page_context
