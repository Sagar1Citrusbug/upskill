import uuid
from dataclasses import dataclass
from dataclass_type_validator import dataclass_validate
from django.conf import settings
import random
import string


def generate_password() -> str:
    # Generate a random password of length 16
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for _ in range(16))

    return password


def asdict(o, skip_empty=False):
    return {k: v for k, v in o.__dict__.items() if not (skip_empty and v is None)}


@dataclass_validate(before_post_init=True)
@dataclass(frozen=True)
class UserID:
    """
    A value object used to generate the UserID in market models
    """

    value: uuid.UUID
