from typing import final


@final
class HeroNotFoundError(Exception):
	"""Exception raises when hero is not found"""

@final
class FailedFetchHeroFromExternalAPIException(Exception):
	"""Exception raises when fetching hero from external api fails"""