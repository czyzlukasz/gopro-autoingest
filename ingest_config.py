from os import getenv

GOPRO_IP: str = getenv("GOPRO_IP", "10.5.5.9")
GOPRO_PORT: int = int(getenv("GOPRO_PORT", 8080))
LOWEST_DOWNLOAD_SPEED_MBYTES_PER_SECOND: float = int(getenv("LOWEST_DOWNLOAD_SPEED", 5))

LOG_FILE: str = getenv("LOG_DIR", "/storage/logs")
LOGGING_LEVEL: str = getenv("LOGGING_LEVEL", "DEBUG")

STAGING_DIR: str = getenv("STAGING_DIR", "/storage/staging")
STORAGE_DIR: str = getenv("STORAGE_DIR", "/storage/videos")

OUTPUT_VIDEO_NAME_FORMAT: str = getenv("OUTPUT_VIDEO_NAME", "%m.%d.%Y %H%M")

ENABLE_CONNECTION_CONFIRMATION_BEEP: bool = bool(getenv("ENABLE_CONNECTION_CONFIRMATION_BEEP", 1))
ENABLE_CAMERA_VIDEO_REMOVAL: bool = bool(getenv("ENABLE_CAMERA_VIDEO_REMOVAL", 0))
ENABLE_PROCESSED_VIDEO_REMOVAL: bool = bool(getenv("ENABLE_PROCESSED_VIDEO_REMOVAL", 0))
