import filetype
import asyncio
import aiofiles
import structlog

from typing import final
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import UploadFile
from PIL import Image, ImageFilter, UnidentifiedImageError

from src.services.utils import transform_max_size_in_mb_to_readable_format
from src.services.exceptions import ImageProcessingError, ImageValidationError

logger = structlog.get_logger(__name__)


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class ImageUploadService:
	upload_dir_path: str
	temp_dir_path: str
	max_file_size: int
	allowed_mimes: list[str]
	max_width: int
	max_height: int

	def _validate_image(self, file: UploadFile) -> None:
		if file.size is None or file.size > self.max_file_size:
			max_mb = transform_max_size_in_mb_to_readable_format(self.max_file_size)

			raise ImageValidationError(
				f"{file.filename} exceeds max file size: {max_mb}MB"
			)
		
		first_chunk = file.file.read(2048)
		file.file.seek(0)
		mime_type = filetype.guess(first_chunk)

		if mime_type is None or mime_type.mime not in self.allowed_mimes:
			raise ImageValidationError(
				f"{file.filename} is not an image. \n"
				f"Allowed types: {", ".join(self.allowed_mimes)}"
			)
		
	def _process_image(self, source_file_path: str, dest_file_path: str) -> None:
		Path(dest_file_path).parent.mkdir(parents=True, exist_ok=True)
		image_max_size = (self.max_width, self.max_height)
		quality_rate = 95

		with Image.open(source_file_path) as img:
			if img.mode not in ("RGB", "RGBA"):
				img = img.convert("RGBA")

			img.thumbnail(image_max_size, Image.Resampling.LANCZOS)
			img = img.filter(
				ImageFilter.UnsharpMask(radius=1, percent=80, threshold=2)
			)
			img.save(
				dest_file_path, "WEBP", quality=quality_rate, method=6, optimize=True
			)

	async def upload_image(
			self,
			file: UploadFile,
			hero_id: UUID
	) -> str:
		if file is None:
			raise ImageProcessingError(
				f"File was not provided"
		)

		temp_dir = Path(self.temp_dir_path)
		temp_dir.mkdir(parents=True, exist_ok=True)

		upload_dir = Path(self.upload_dir_path)
		upload_dir.mkdir(parents=True, exist_ok=True)

		temp_path = None

		try:
			await asyncio.to_thread(self._validate_image, file)
			logger.debug(
				"Image has been validated",
				hero_id=str(hero_id),
				filename=file.filename
			)

			file_extension = Path(file.filename).suffix
			file_id = uuid4()
			temp_path = temp_dir / f"{file_id}{file_extension}"

			async with aiofiles.open(temp_path, "wb") as f:
				chunk_size = 1024 * 1024
				while chunk := await file.read(chunk_size):
					await f.write(chunk)

			logger.debug("Image has been saved to temp directory")

			final_path = upload_dir / f"{file_id}.webp"
			await asyncio.to_thread(
				self._process_image,
				str(temp_path),
				str(final_path)
			)

			img_url = f"/{self.upload_dir_path}/{file_id}.webp"
			logger.info(
				"Image has been uploaded successfully",
				url=img_url
			)

			return img_url

		except ImageValidationError:
			raise

		except UnidentifiedImageError as e:
			raise ImageValidationError(
            "Uploaded file is corrupted and cannot be processed"
      ) from e

		except OSError as e:
			raise ImageProcessingError(
                f"Failed to process image: {e}"
      ) from e

		except Exception as e:
			raise ImageProcessingError(
                "Unexpected error while processing image"
      ) from e

		finally:
			if temp_path and temp_path.exists():
				temp_path.unlink()

	async def delete_image(self, image_url: str) -> None:
		filepath = Path(self.upload_dir_path) / Path(image_url).name
		if filepath.exists():
			await asyncio.to_thread(filepath.unlink)
			logger.info("Image has been deleted", filename=filepath.name)
			


