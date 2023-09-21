from dataclasses import dataclass

# from focus_power.infrastructure.logger.models import AttributeLogger
from rest_framework import status


@dataclass(frozen=True)
class BaseException(Exception):
    item: str
    message: str
    status_code: int = status.HTTP_400_BAD_REQUEST

    def error_data(self) -> dict:
        error_data = {"item": self.item, "message": self.message}
        return error_data

    def __str__(self):
        return "{}: {}".format(self.item, self.message)


# general exception classes with status codes


class Status401Exception(BaseException):
    def __init__(self, item, message):
        super().__init__(item, message, status_code=status.HTTP_401_UNAUTHORIZED)


class Status403Exception(BaseException):
    def __init__(self, item, message):
        super().__init__(item, message, status_code=status.HTTP_403_FORBIDDEN)


class Status404Exception(BaseException):
    def __init__(self, item, message):
        super().__init__(item, message, status_code=status.HTTP_404_NOT_FOUND)


class Status409Exception(BaseException):
    def __init__(self, item, message):
        super().__init__(item, message, status_code=status.HTTP_409_CONFLICT)


class Status422Exception(BaseException):
    def __init__(self, item, message):
        super().__init__(
            item, message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


# not used at anywhere
class AddUserException(BaseException):
    pass


# done
class UserAlreadyExistsException(Status409Exception):
    pass


# not used
class UserRoleException(BaseException):
    pass


# done
class CompanyNotFoundException(Status404Exception):
    pass


# done
class MiddlewareException(Status401Exception):
    pass


# done
class RoleNameAlreadyExistsException(Status409Exception):
    pass


# done
class RoleNameException(BaseException):
    pass


# done
class RoleException(BaseException):
    pass


# done
class CompanyNotExistsException(Status404Exception):
    pass


# done
class MailNotSendException(BaseException):
    pass


# done
class UserDeletionException(BaseException):
    pass


class MailNotSendException(BaseException):
    pass
