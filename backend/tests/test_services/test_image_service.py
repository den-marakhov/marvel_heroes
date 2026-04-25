import pytest
from io import BytesIO
from unittest.mock import MagicMock, patch

from src.services.image_service import ImageUploadService
from src.services.exceptions import ImageProcessingError, ImageValidationError

class TestImageUploadService:

	@pytest.fixture
	def image_service(
		self,
		tmp_path
	) -> ImageUploadService:
		return ImageUploadService(
			upload_dir_path=str(tmp_path / "uploads"),
			temp_dir_path=str(tmp_path / "temp"),
			max_file_size=1024*1024*5,
			allowed_mimes=["image/jpeg", "image/png", "image/webp"],
			max_width=900,
			max_height=900
		)
	
	def test_too_large_file_size(
			self,
			image_service: ImageUploadService
	):
		file = MagicMock()
		file.filename = "some_huge_file.jpg"
		file.size = 1024 * 1024 * 6

		with pytest.raises(ImageValidationError):
			image_service._validate_image(file=file)

	@patch("src.services.image_service.filetype.guess")
	def test_invalid_file_mime_type(
		self, mock_guess, image_service: ImageUploadService
	):
		mock_guess.return_value = MagicMock(mime="application/pdf")

		file=MagicMock()
		file.filename = "doc.pdf"
		file.size = 1024 * 1024
		file.file = BytesIO(b"\x00" * 2048)

		with pytest.raises(ImageValidationError):
			image_service._validate_image(file=file)

		
