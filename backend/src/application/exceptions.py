from typing import final


@final
class HeroNotFoundError(Exception):
	"""Exception raises when hero is not found"""