#$Id$

class Template:
    """This class is used to create object for templates."""
    def __init__(self):
        """Initialize the parameters for templates object."""
        self.template_name = ''
        self.template_id = ''
        self.template_type = ''
   
    def set_template_name(self, template_name):
        """Set template name.

        Args: 
            template_name(str): Template name.

        """
        self.template_name = template_name

    def get_template_name(self):
        """Get template name.
 
        Returns:
            str: Template name.

        """
        return self.template_name

    def set_template_id(self, template_id):
        """Set template id.

        Args: 
            template_id(str): Template id.

        """
        self.template_id = template_id

    def get_template_id(self):
        """Get template id.

        Returns:
            str: Template id.

        """
        return self.template_id

    def set_template_type(self, template_type):
        """Set template type.

        Args:
            template_type(str): Template type.
      
        """
        self.template_type = template_type

    def get_template_type(self):
        """Get template type.

        Returns:
            str: Template type.

        """
        return self.template_type


