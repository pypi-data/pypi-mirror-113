#$Id$

class Email:
    """This class is used to create a Email object."""
    def __init__(self):
        """Initialize the parameters for email object."""
        self.to_mail_ids = []
        self.cc_mail_ids = []
        self.subject = ''
        self.body = ''
        self.send_from_org_email_id = None
        self.file_name = ''
        self.contact_id = ''
        self.customer_id = ''
        self.gateways_configured = None
        self.attachment_name = ''
        self.to_contacts = [] 
        self.from_emails = []
        self.error_list = []
        self.email_templates = []
        self.deprecated_placeholders_used = []
        self.gateways_associated = None
        self.attach_pdf = None
        self.file_name_without_extension = None

    def set_to_mail_ids(self, to_mail_ids):
        """Set the list of email address of the recipients.
         
        Args:
            to_mail_ids(list): List of email address of the recipients.
        
        """
        self.to_mail_ids.extend(to_mail_ids)
 
    def get_to_mail_ids(self):
        """Get the list of email address of the recipients.
         
        Returns:
            list: List of email address of recipients.
 
        """
        return self.to_mail_ids

    def set_cc_mail_ids(self, cc_mail_ids):
        """Set the list of email address of the recipients to be cced.
  
        Args:
            cc_mail_ids(list): List of email address of the recipients to be 
                cced.
 
        """
        self.cc_mail_ids.extend(cc_mail_ids)
 
    def get_cc_mail_ids(self): 
        """Get the list of email address of the recipients to be cced.
     
        Returns:
            list: List of email address of the recipients to be cced.

        """ 
        return self.cc_mail_ids

    def set_subject(self, subject):
        """Set subject for the email.
     
        Args:
            subject(str): Subject for the email.
 
        """
        self.subject = subject
 
    def get_subject(self): 
        """Get subject of the email.
       
        Returns:
            str: Subject of the email.
        
        """  
        return self.subject

    def set_body(self, body):
        """Set body for the email.
      
        Args:
            body(str): Body for the mail.
      
        """
        self.body = body
   
    def get_body(self):
        """Get body of the mail.
       
        Returns:
            str: Body of the mail.
 
        """
        return self.body

    def set_send_from_org_email_id(self, send_from_org_email_id):
        """Set the boolean to trigger the email from the organization's 
            email address.
        
        Args:
            send_from_org_email_id(bool): True to send email from the 
                organization's email address else False.
     
        """
        self.send_from_org_email_id = send_from_email_id
 
    def get_send_from_org_email_id(self):
        """Get whether to send email from organization's email adress or not.
        
        Returns:
            bool: True send email from organization's email address else False.
 
        """
        return self.send_from_org_email_id
 
    def set_file_name(self, file_name):
        """Set file name that is attached with email.
 
        Args:
            file_name(str): Name of the file that is attached with mail.

        """
        self.file_name = file_name

    def get_file_name(self):
        """Get file name that is attached with email.
 
        Returns: 
            str: Name of the file that is attached.
 
        """
        return self.file_name

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

    def set_customer_id(self, customer_id):
        """Set customer id.
        
        Args:
            customer_id(str): Customer id.
 
        """
        self.customer_id = customer_id

    def get_customer_id(self):
        """Get customer id.
         
        Returns:
            str: Customer id.

        """
        return self.customer_id
  
    def set_gateways_configured(self, gateways_configured):
        """Set gateways configured.
         
        Args:
            gateways_configured(str): Gateways configured.
        
        """  
        self.gateways_configured = gateways_configured

    def get_gateways_configure(self):
        """Get gateways configured.
        
        Returns:
            str: Gateways configured.
       
        """
        return self.gateways_configured
  
    def set_attachment_name(self, attachment_name):
        """Set attachment name.
        
        Args:
            attachment_name(str): Attachment name.
        
        """
        self.attachment_name = attachment_name

    def get_attachment_name(self):
        """Get attachment name.
        
        Returns:
            str: Attachment name.
        
        """
        return self.attachment_name

    def set_to_contacts(self, to_contacts):
        """Set the details for the contacts for which mail has to be sent.
     
        Args:
            to_contacts(instance): To_contacts object.
 
        """
        self.to_contacts.append(to_contacts)
 
    def get_to_contacts(self):
        """Get the details of the contacts for which mail has to be sent.
        
        Returns:
            list: List of to_contacts object.
 
        """
        return self.to_contacts

    def set_from_emails(self, from_emails):
        """Set from email details.
 
        Args:
            from_emails(instance): From emails object.
       
        """ 
        self.from_emails.append(from_emails)

    def get_from_emails(self):
        """Get from email details.
        
        Returns:
            list: lList of from_emails object.

        """
        return self.from_emails

    def set_error_list(self, error_list):
        """Set error list.
       
        Args:
            error_list(list): List of errors.
      
        """
        self.error_list.extend(error_list)
 
    def get_error_list(self):
        """Get error list.
        
        Returns:
            list: List of errors.
         
        """
        return self.error_list
   
    def set_email_templates(self, email_template):  
        """Set email templates.
      
        Args: 
            email_template(instance): Email templates object.

        """
        self.email_templates.append(email_template)
 
    def get_email_templates(self):
        """Get email templates.
          
        Returns:
            list: List of email templates object.
        
        """
        return self.email_templates

    def set_deprecated_placeholders_used(self, deprecated_placeholders_used):
        """Set deprecated placeholders used.
         
        Args:
            set_deprecated_placeholders_used(list): List of deprecated 
                placeholders.
        
        """
        self.deprecated_placeholders_used.extend(deprecated_placeholders_used)

    def get_deprecated_placeholders_used(self):
        """Get deprecated placeholders used.
       
        Returns:
            list: List of deprecated placeholders.
 
        """
        return self.deprecated_placeholders_used

    def set_gateways_associated(self, gateways_associated):
        """Set whether gateways are associated or not.
         
        Args:
            gateways_associated(bool): True if gateways are associated else 
                False.

        """
        self.set_gateways_associated = gateways_associated

    def get_gateways_associated(self):
        """Get whether gateways are associated or not.
 
        Returns:
            bool: True if gateways are associated else False.

        """
        return self.gateways_associated

    def set_attach_pdf(self, attach_pdf):
        """Set whether pdf is attached or not.
 
        Args:
            attach_pdf(bool): True if pdf is attached else False.
 
        """
        self.attach_pdf = attach_pdf
 
    def get_attach_pdf(self):
        """Get whether pdf is attached or not.
        
        Returns:
            bool: True if pdf is attached else False.
 
        """
        return self.attach_pdf
   
    def set_file_name_without_extension(self, file_name_without_extension):
        """Set file name without extension.
         
        Args:
            file_name_without_extension(str): File name without extension.
       
        """
        self.file_name_without_extension = file_name_without_extension

    def get_file_name_without_extension(self):
        """Get filename without extension.
         
        Returns:
            str: File name without extension.
 
        """  
        return self.file_name_without_extension

    def to_json(self):
        """This method is used to convert email object to Json object.

        Returns:
            dict: Dictionary containing json object for email object.

        """
        email = {}
        email['subject'] = self.subject
        email['body'] = self.body
        email['to_mail_ids'] = self.to_mail_ids
        if not self.cc_mail_ids:
            email['cc_mail_ids'] = self.cc_mail_ids
        if self.send_from_org_email_id:
            email['send_from_org_email_id'] = self.sed_from_org_email_id
        return email
  

