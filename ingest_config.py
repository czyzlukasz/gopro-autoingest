from os import getenv

GOPRO_IP: str = getenv("GOPRO_IP", "10.5.5.9")
GOPRO_PORT: int = int(getenv("GOPRO_PORT", 8080))

LOGGING_LEVEL: str = getenv("LOGGING_LEVEL", "INFO")

DOWNLOAD_DIR: str = getenv("DOWNLOAD_DIR", "./tmp")
VIDEO_DOWNLOAD_TIMEOUT: float = 10000
