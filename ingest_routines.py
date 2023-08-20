import datetime
import logging
from os import makedirs

import ingest_config


def setup_logging():
    makedirs(ingest_config.LOG_FILE, exist_ok=True)
    logging.basicConfig(level=ingest_config.LOGGING_LEVEL)
    logger = logging.getLogger()
    handler = logging.FileHandler(
        f"{ingest_config.LOG_FILE}/{datetime.datetime.now().strftime(ingest_config.OUTPUT_VIDEO_NAME_FORMAT)}.log",
        'w+')

    handler.setFormatter(logging.Formatter(fmt='%(asctime)s|%(levelname)s: %(message)s'))
    logger.addHandler(handler)


def log_parameters():
    logger = logging.getLogger()
    logger.debug("Ingest parameters")
    logger.debug(f"GOPRO_IP: {ingest_config.GOPRO_IP}")
    logger.debug(f"GOPRO_PORT: {ingest_config.GOPRO_PORT}")
    logger.debug(f"LOWEST_DOWNLOAD_SPEED_MBYTES_PER_SECOND: {ingest_config.LOWEST_DOWNLOAD_SPEED_MBYTES_PER_SECOND}")
    logger.debug(f"LOG_FILE: {ingest_config.LOG_FILE}")
    logger.debug(f"LOGGING_LEVEL: {ingest_config.LOGGING_LEVEL}")
    logger.debug(f"STAGING_DIR: {ingest_config.STAGING_DIR}")
    logger.debug(f"STORAGE_DIR: {ingest_config.STORAGE_DIR}")
    logger.debug(f"OUTPUT_VIDEO_NAME_FORMAT: {ingest_config.OUTPUT_VIDEO_NAME_FORMAT}")


def download_videos():
    raise NotImplementedError


def process_videos():
    raise NotImplementedError


def remove_processed_videos():
    raise NotImplementedError


def archive_video():
    raise NotImplementedError
