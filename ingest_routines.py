import datetime
import logging
from os import makedirs
from time import sleep
from typing import List
from shutil import rmtree as rm_rf

import ingest_config
from file_management import VideoInfo, get_video_info_from_staging
from http_connector import HttpClient, RequestFailedException, RequestTimeoutException
from video_downloader import download_video
from video_processing import process_video


def setup_logging():
    makedirs(ingest_config.LOG_DIR, exist_ok=True)
    logging.basicConfig(level=ingest_config.LOGGING_LEVEL)
    logger = logging.getLogger()
    handler = logging.FileHandler(
        f"{ingest_config.LOG_DIR}/{datetime.datetime.now().strftime(ingest_config.OUTPUT_VIDEO_NAME_FORMAT)}.log",
        'w+', delay=True)

    handler.setFormatter(logging.Formatter(fmt='%(asctime)s|%(levelname)s: %(message)s'))
    logger.addHandler(handler)


def log_parameters():
    logger = logging.getLogger()
    logger.debug("Ingest parameters")
    logger.debug(f"GOPRO_IP: {ingest_config.GOPRO_IP}")
    logger.debug(f"GOPRO_PORT: {ingest_config.GOPRO_PORT}")
    logger.debug(f"LOWEST_DOWNLOAD_SPEED_MBYTES_PER_SECOND: {ingest_config.LOWEST_DOWNLOAD_SPEED_MBYTES_PER_SECOND}")
    logger.debug(f"LOG_DIR: {ingest_config.LOG_DIR}")
    logger.debug(f"LOGGING_LEVEL: {ingest_config.LOGGING_LEVEL}")
    logger.debug(f"STAGING_DIR: {ingest_config.STAGING_DIR}")
    logger.debug(f"STORAGE_DIR: {ingest_config.STORAGE_DIR}")
    logger.debug(f"OUTPUT_VIDEO_NAME_FORMAT: {ingest_config.OUTPUT_VIDEO_NAME_FORMAT}")
    logger.debug(f"ENABLE_CONNECTION_CONFIRMATION_BEEP: {ingest_config.ENABLE_CONNECTION_CONFIRMATION_BEEP}")
    logger.debug(f"ENABLE_CAMERA_VIDEO_REMOVAL: {ingest_config.ENABLE_CAMERA_VIDEO_REMOVAL}")
    logger.debug(f"ENABLE_PROCESSED_VIDEO_REMOVAL: {ingest_config.ENABLE_PROCESSED_VIDEO_REMOVAL}")


def download_videos():
    logger = logging.getLogger()
    client = HttpClient()

    try:
        client.get_gopro_status()
        videos = client.get_video_info()

        if ingest_config.ENABLE_CONNECTION_CONFIRMATION_BEEP:
            client.enable_beeping()
            sleep(5)
            client.disable_beeping()
    except (RequestFailedException, RequestTimeoutException):
        return

    logger.info(f"Found {len(videos)} videos that can be downloaded")
    for video in videos:
        staging_path = f"{ingest_config.STAGING_DIR}/{video.video_number}"
        successful = download_video(video, staging_path)
        if not successful:
            logger.warning("Skipping video processing due to the download failure")
        if ingest_config.ENABLE_CAMERA_VIDEO_REMOVAL:
            logger.debug(f"Removing video {video.video_number} from camera")
            client.delete_video(video)

    logger.info("Switching off camera")
    client.shutdown_camera()


def process_videos():
    logger = logging.getLogger()

    videos = get_video_info_from_staging()
    logger.info(f"Found {len(videos)} videos in staging area")

    successfully_processed_videos: List[VideoInfo] = []
    for video in videos:
        download_path = f"{ingest_config.STAGING_DIR}/{video.video_number}"
        successful = process_video(download_path, video)
        if successful:
            successfully_processed_videos.append(video)

    remove_processed_videos(successfully_processed_videos)


def remove_processed_videos(successfully_processed_videos: List[VideoInfo]):
    logger = logging.getLogger()

    logger.info(f"Successfully processed {len(successfully_processed_videos)} videos. Removing them from staging area")
    for video in successfully_processed_videos:
        staging_path = f"{ingest_config.STAGING_DIR}/{video.video_number}"
        logger.debug(f"Calling rm -rf on {staging_path}")
        if ingest_config.ENABLE_PROCESSED_VIDEO_REMOVAL:
            rm_rf(staging_path)


def archive_video():
    raise NotImplementedError
