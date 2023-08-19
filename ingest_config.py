from os import getenv

GOPRO_IP: str = getenv("GOPRO_IP", "10.5.5.9")
GOPRO_PORT: int = int(getenv("GOPRO_PORT", 8080))
LOWEST_DOWNLOAD_SPEED_MBYTES_PER_SECOND: float = int(getenv("LOWEST_DOWNLOAD_SPEED", 5))

LOG_FILE: str = getenv("LOG_FILE", "./log.log")
LOGGING_LEVEL: str = getenv("LOGGING_LEVEL", "INFO")

DOWNLOAD_DIR: str = getenv("DOWNLOAD_DIR", "./tmp")
STAGING_DIR: str = getenv("STAGING_DIR", "./tmp/staging")
