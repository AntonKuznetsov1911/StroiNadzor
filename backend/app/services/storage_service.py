"""
Сервис для работы с файловым хранилищем (S3)
"""
import os
from typing import BinaryIO
from minio import Minio
from minio.error import S3Error
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class StorageService:
    """Сервис для работы с S3-совместимым хранилищем"""

    def __init__(self):
        # Извлечение хоста из URL (убираем http://)
        endpoint = settings.S3_ENDPOINT.replace('http://', '').replace('https://', '')

        self.client = Minio(
            endpoint,
            access_key=settings.S3_ACCESS_KEY,
            secret_key=settings.S3_SECRET_KEY,
            secure=False  # True для HTTPS
        )

        self.bucket_name = settings.S3_BUCKET_NAME

        # Создание bucket если не существует
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Проверка и создание bucket"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Bucket {self.bucket_name} created")
            else:
                logger.info(f"Bucket {self.bucket_name} already exists")
        except S3Error as e:
            logger.error(f"Error checking/creating bucket: {str(e)}")

    def upload_file(
        self,
        file_data: BinaryIO,
        object_name: str,
        content_type: str = "application/octet-stream"
    ) -> str:
        """
        Загрузка файла в хранилище

        Args:
            file_data: Бинарные данные файла
            object_name: Имя объекта в хранилище
            content_type: MIME тип файла

        Returns:
            URL загруженного файла
        """
        try:
            # Получаем размер файла
            file_data.seek(0, 2)  # Переход в конец файла
            file_size = file_data.tell()
            file_data.seek(0)  # Возврат в начало

            self.client.put_object(
                self.bucket_name,
                object_name,
                file_data,
                file_size,
                content_type=content_type
            )

            # Формирование URL
            file_url = f"{settings.S3_ENDPOINT}/{self.bucket_name}/{object_name}"

            logger.info(f"File uploaded: {file_url}")
            return file_url

        except S3Error as e:
            logger.error(f"Error uploading file: {str(e)}")
            raise

    def delete_file(self, object_name: str):
        """Удаление файла из хранилища"""
        try:
            self.client.remove_object(self.bucket_name, object_name)
            logger.info(f"File deleted: {object_name}")
        except S3Error as e:
            logger.error(f"Error deleting file: {str(e)}")
            raise

    def get_file_url(self, object_name: str, expires: int = 3600) -> str:
        """
        Получение временного URL для доступа к файлу

        Args:
            object_name: Имя объекта
            expires: Время жизни URL в секундах (по умолчанию 1 час)

        Returns:
            Временный URL
        """
        try:
            url = self.client.presigned_get_object(
                self.bucket_name,
                object_name,
                expires=expires
            )
            return url
        except S3Error as e:
            logger.error(f"Error generating URL: {str(e)}")
            raise


# Singleton instance
storage_service = StorageService()
