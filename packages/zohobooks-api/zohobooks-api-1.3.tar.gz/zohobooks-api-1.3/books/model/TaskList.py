#$Id$

from books.model.PageContext import PageContext

class TaskList:
    """This class is used to create object for tasks list."""
    def __init__(self):
        """Initialize parameters for tasks list object."""
        self.tasks = []
        self.page_context = PageContext()
 
    def set_tasks(self, task):
        """Set tasks.

        Args:
            task(instance): Task object.

        """
        self.tasks.append(task)

    def get_tasks(self): 
        """Get tasks.

        Returns: 
            list of instance: List of tasks object.

        """
        return self.tasks

    def set_page_context(self, page_context): 
        """Set page context.

        Args:
            page_context(instance): Page context. 

        """
        self.page_context = page_context

    def get_page_context(self):
        """Get page context.

        Returns:
            instance: Page context.

        """
        return self.page_context
