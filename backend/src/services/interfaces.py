from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from fastapi import UploadFile


class ImageUploadServiceProtocol(Protocol):
    @abstractmethod
    def _validate_image(self, file: UploadFile) -> None: ...

    @abstractmethod
    def _process_image(self, source_file_path: str, dest_file_path: str) -> None: ...

    @abstractmethod
    async def upload_image(self, file: UploadFile, hero_id: UUID) -> str: ...

    @abstractmethod
    async def delete_image(self, image_url: str) -> None: ...
