import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Basic Settings
    app_name: str = "TrueCopy API"
    debug_mode: bool = False
    api_v1_str: str = "/api/v1"

    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0" 

    # Celery Configuration - 0 : Task Queue & 1 : Result Backend
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    # Temporary Input Image Storage
    temporary_upload_directory: str = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "temp_uploads")

    # Hardware Acceleration - mps for Apple Silicon, cpu for fallback
    model_device: str = "mps"

    # loads variable from env file
    class Config:
        env_file = ".env"
        extra = "ignore"

# Instance of Settings class
settings = Settings()