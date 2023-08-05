#$Id$

class PaymentGateway:
    """This class is used to create object for payment gateway object."""
    def __init__(self):
        """Initialize parameters for Payment gateway object."""
        self.gateway_name = ''
        self.gateway_name_formatted = ''
        self.identifier = ''
        self.additional_field1 = ''
        self.additional_field2 = ''
        self.additional_field3 = ''
        self.deposit_to_account_id = ''
        self.deposit_to_account_name = ''
        self.configured = None

    def set_gateway_name(self, gateway_name):
        """Set gateway name associated with recurring profile.

        Args:
            gateway_name(str): Gateway name associated with recurring profile.
                Allowed values are paypal,  authorize_net,  payflow_pro,  
                 stripe, 2checkout and braintree.

        """
        self.gateway_name = gateway_name

    def get_gateway_name(self):
        """Get gateway name.

        Returns:
            str: Gateway name associated with recurring profile.
  
        """
        return self.gateway_name 
  
    def set_gateway_name_formatted(self, gateway_name_formatted):
        """Set gateway name formatted.

        Args:
            gateway_name_formatted(str): Gateway name formatted.
 
        """
        self.gateway_name_formatted = gateway_name_formatted
 
    def get_gateway_name_formatted(self):
        """Get gateway name formatted.

        Returns:
            str: Gateway name formatted.

        """
        return self.gateway_name_formatted
  
    def set_identifier(self, identifier):
        """Set identifier.

        Args: 
            identifier(str): Identifier.

        """
        self.identifier = identifier

    def get_identifier(self):
        """Get identifier.

        Returns:
            str: Identifier.

        """ 
        return self.identifier
  
    def set_additional_field1(self, additional_field1):
        """Set additional field1.  
        
        Args: 
            additional_field1(str): Paypal payment method.Allowed values are 
                standard and adaptive.
 
        """
        self.additional_field1 = additional_field1

    def get_additional_field1(self):
        """Get additional field1.

        Returns:
            str: Paypal payment method.

        """
        return self.additional_field1

    def set_additional_field2(self, additional_field2):
        """Set additional field2.  
        
        Args: 
            additional_field2(str): Paypal payment method.Allowed values are 
                standard and adaptive.
 
        """
        self.additional_field2 = additional_field2
  
    def get_additional_field2(self):
        """Get additional field2.

        Returns:
            str: Paypal payment method.

        """
        return self.additional_field2

    def set_additional_field3(self, additional_field3):
        """Set additional field3.  
        
        Args: 
            additional_field3(str): Paypal payment method.Allowed values are 
                standard and adaptive.
 
        """ 
        self.additional_field3 = additional_field3
  
    def get_additional_field3(self):
        """Get additional fiield3.

        Returns:
            str: Paypal payment method.

        """
        return self.additional_field3

    def set_deposit_to_account_id(self, deposit_to_account_id):
        """Set deposit to account id.

        Args:
            deposit_to_account_id(str): Deposit to account id.

        """
        self.deposit_to_account_id = deposit_to_account_id

    def get_deposit_to_account_id(self):
        """Get deposit to account id.

        Returns:
            str: Deposit to account id.

        """
        return self.deposit_to_account_id

    def set_deposit_to_account_name(self, deposit_to_account_name):
        """Set deposit to account name.
      
        Args: 
            deposit_to_account_name(str): Deposit to account name.

        """
        self.deposit_to_account_name = deposit_to_account_name

    def get_deposit_to_account_name(self):
        """Get deposit to account name.

        Returns:
            str: Deposit to account name.

        """
        return self.deposit_to_account_name

    def set_configured(self, configured):
        """Set Whether to configure or not.

        Args:
            configured(bool): Configured.

        """
        self.configured = configured

    def get_configured(self):
        """Get configured.
 
        Returns: 
            bool: Configured.

        """
        return self.configured

    def to_json(self):
        """This method is used to convert payment gateway object to json object.

        Returns:
            dict: Dictionary containing json object for payment gatewqay.

        """
        data = {}
        if self.gateway_name != '':
            data['gateway_name'] = self.gateway_name 
        if self.additional_field1 != '':
            data['additional_field1'] = self.additional_field1
        return data
