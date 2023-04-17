from google.cloud import storage
import json
from flask_login import UserMixin
from flaskr.backend import Backend

class User(UserMixin):
    """User class inherits from UserMixin for calling common function to handle page states.

    Functions inherited: is_authenticated, is_active, and is_anonymous.
    Attributes:
        username: String indicating user's id to authenticate.
    """

    def __init__(self, username, perms):
        """Initializes the User based on their username.

        Args:
          username: Defines identifier for User.
          perms: Designates permissions for user, either "default" or "admin"
        """
        self.username = username
        self.perms = perms

    def get_id(self):
        """Initializes the instance based on spam preference.

        Args:
          likes_spam: Defines if instance exhibits this preference.
        """
        return self.username
