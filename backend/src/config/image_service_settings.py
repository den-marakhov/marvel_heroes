from typing import final

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


@final
class ImageServiceSettings(BaseSettings):
    img_width: int = Field(..., alias="IMAGE_WIDTH")
    img_height: int = Field(..., alias="IMAGE_HEIGHT")
    max_file_size: int = Field(..., alias="MAX_IMAGE_FILE_SIZE")
    temp_dir: str = Field("temp", alias="TEMP_FOLDER_PATH")
    upload_dir: str = Field("uploads", alias="UPLOADS_FOLDER_PATH")
    allowed_types: list[str] = Field(
        ["image/png", "image/jpeg", "image/webp"], alias="ALLOWED_MIME_TYPES"
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
