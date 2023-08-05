#$Id$

class TemplateList:
    """This method is used to create object for Template list."""
    def __init__(self):
        """Initilaize parameters for Template list."""
        self.templates = []

    def set_templates(self, template):
        """Set templates.

        Args:
            template(instance): Template object.

        """ 
        self.templates.append(template)

    def get_templates(self):
        """Get templates.

        Returns:
            list of instance: List of templates object.

        """
        return self.templates
