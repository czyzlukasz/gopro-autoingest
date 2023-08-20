from os import getenv

GOPRO_IP: str = getenv("GOPRO_IP", "10.5.5.9")
GOPRO_PORT: int = int(getenv("GOPRO_PORT", 8080))
LOWEST_DOWNLOAD_SPEED_MBYTES_PER_SECOND: float = int(getenv("LOWEST_DOWNLOAD_SPEED", 5))
ENABLE_CONNECTION_CONFIRMATION_BEEP: bool = bool(getenv("ENABLE_CONNECTION_CONFIRMATION_BEEP", "1"))

LOG_FILE: str = getenv("LOG_FILE", "./log.log")
LOGGING_LEVEL: str = getenv("LOGGING_LEVEL", "DEBUG")

STAGING_DIR: str = getenv("STAGING_DIR", "tmp/staging")
STORAGE_DIR: str = getenv("STORAGE_DIR", "./tmp/output")

OUTPUT_VIDEO_CRF: int = int(getenv("OUTPUT_VIDEO_CRF", "30"))
OUTPUT_VIDEO_NAME_FORMAT: str = getenv("OUTPUT_VIDEO_NAME", "%m.%d.%Y %H%M")
