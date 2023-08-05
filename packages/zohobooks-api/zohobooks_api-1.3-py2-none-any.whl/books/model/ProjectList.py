#$Id$

from books.model.PageContext import PageContext

class ProjectList:
    """This class is used to create objects for projects list."""
    def __init__(self): 
        """Initialize parameters for Projects list."""
        self.projects = []
        self.page_context = PageContext()

    def set_projects(self, project):
        """Set projects.

        Args:
            project(instance): Project object.

        """
        self.projects.append(project)

    def get_projects(self):
        """Get projects.

        Returns:
            list of instance: List of projects object.

        """
        return self.projects

    def set_page_context(self, page_context):
        """Set page context.

        Args:
            page_cotext(instance): Page context object.

        """
        self.page_context = page_context

    def get_page_context(self):
        """Get page context.

        Returns:
            instance: Page context object.

        """
        return self.page_context
  
