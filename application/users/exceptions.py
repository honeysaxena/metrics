from fastapi import HTTPException

class LoginRequiredException(HTTPException):
    pass

class UserHasAccountException(Exception):
      """user already has account with this email"""


class InvalidEmailException(Exception):
      """Invalid Email"""


class InvalidUserIDException(Exception):
    """Invalid User ID"""