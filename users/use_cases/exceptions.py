class ExistingUserException(Exception):
    msg = "An user already exists with this email"


class UserNotFoundException(Exception):
    msg = "User not found"
