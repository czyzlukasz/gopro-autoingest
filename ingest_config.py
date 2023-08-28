from os import getenv

# IP address of the camera
GOPRO_IP: str = getenv("GOPRO_IP", "10.5.5.9")
# Port of the API. This value should stay default unless some port forwarding was done
GOPRO_PORT: int = int(getenv("GOPRO_PORT", 8080))
# Lowest acceptable download speed in MegaBytes per second.
# This value should be kept at a reasonable level to avoid long download process
LOWEST_DOWNLOAD_SPEED_MBYTES_PER_SECOND: float = int(getenv("LOWEST_DOWNLOAD_SPEED", 5))

# Directory where all logs will be stored
LOG_DIR: str = getenv("LOG_DIR", "/storage/logs")
# Log level for logging library
LOGGING_LEVEL: str = getenv("LOGGING_LEVEL", "INFO")

# Internal file used as an input for ffmpeg concat
INPUT_FILE_PATH: str = getenv("INPUT_FILE_PATH", "/tmp/input_file.txt")
# Directory where all videos from camera will be downloaded to
STAGING_DIR: str = getenv("STAGING_DIR", "/storage/staging")
# Directory where all processed videos will be stored
STORAGE_DIR: str = getenv("STORAGE_DIR", "/storage/videos")

# Format of output file names. Note that this value should be valid in terms of the datetime.strftime function
# Keep in mind that the limitation of the filesystem apply as well (e.g. no colons on Windows!)
OUTPUT_VIDEO_NAME_FORMAT: str = getenv("OUTPUT_VIDEO_NAME", "%m.%d.%Y %H%M")

# Enable camera beeping when program successfully connects to the camera
ENABLE_CONNECTION_CONFIRMATION_BEEP: bool = bool(getenv("ENABLE_CONNECTION_CONFIRMATION_BEEP", 1))
# Enable video deletion from camera after video gets downloaded to staging area
ENABLE_CAMERA_VIDEO_REMOVAL: bool = bool(getenv("ENABLE_CAMERA_VIDEO_REMOVAL", 0))
# Enable video deletion from staging area after video gets processed and put into the storage area
ENABLE_PROCESSED_VIDEO_REMOVAL: bool = bool(getenv("ENABLE_PROCESSED_VIDEO_REMOVAL", 0))
