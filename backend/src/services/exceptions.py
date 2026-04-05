from typing import final

@final
class ImageValidationError(Exception):
	"""Raises when image validation error occurs (size, mime type, etc.)"""

@final
class ImageProcessingError(Exception):
	"""
	Raises when something goes wrong while image processing (conversion, saving, etc)
	"""