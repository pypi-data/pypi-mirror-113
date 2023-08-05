#$Id$

from books.model.PageContext import PageContext

class CommentList: 
    """This class is used to create object for comments."""
    def __init__(self):
        """Initialize parameters for Comments list."""
        self.comments = []
        self.page_context = PageContext()

    def set_comments(self, comment):
        """Set comments.
      
        Args:
            comment(instance): Comment object.
        
        """
        self.comments.append(comment)
   
    def get_comments(self):
        """Get comments.
        
        Returns:
            list: List of comments object.
  
        """
        return self.comments

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


   
