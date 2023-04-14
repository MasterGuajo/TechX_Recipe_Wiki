from google.cloud import storage
import json
from flask_login import UserMixin


class User(UserMixin):
    """User class inherits from UserMixin for calling common function to handle page states.

    Functions inherited: is_authenticated, is_active, and is_anonymous.
    Attributes:
        username: String indicating user's id to authenticate.
    """

    def __init__(self, username):
        """Initializes the User based on their username.

        Args:
          username: Defines identifier for User.
        """
        self.username = username
        self.roles = "default"


    def get_id(self):
        """Initializes the instance based on spam preference.

        Args:
          likes_spam: Defines if instance exhibits this preference.
        """
        return self.username

    def is_admin(self):
        return True if self.privileges == "admin" else False

    class Role():
        name = "default"        

    class UserRole():
        id = 0
