from typing import final


@final
class InvalidHeroNameException(Exception):
  """Raises when invalid name to hero entity is provided"""

@final
class DomainValidationError(Exception):
  """Raise when entity validation error occurs"""