import logging
import wget
import threading
from os import makedirs, path

import ingest_config
from file_management import VideoInfo, ChapterInfo


def download_chapter(chapter: ChapterInfo, destination_path: str):
    """
    Download single file from GoPro
    :param ip_address: Address of GoPro camera. Most common value is 10.5.5.9
    :param port: Port that exposes GoPro's api. Most common value is 8080
    :param chapter: Valid ChapterInfo object
    :param destination_path: Path to the destination file where downloaded chapter will be stored
    """
    logger = logging.getLogger()

    if path.isfile(destination_path):
        logger.info(f"Chapter {chapter.file_name} is already downloaded. Skipping")
        return
    full_address = f"http://{ingest_config.GOPRO_IP}:{ingest_config.GOPRO_PORT}/videos/DCIM/{chapter.parent_directory}/{chapter.file_name}"
    wget.download(full_address, destination_path)


def download_video(video: VideoInfo, destination_path: str) -> bool:
    """
    Download single video consisting of multiple chapters.
    Chapters will be stored in specified destination directory with chapters saved as destination_path/chapter_number.mp4
    :param ip_address: Address of GoPro camera. Most common value is 10.5.5.9
    :param port: Port that exposes GoPro's api. Most common value is 8080
    :param video: Valid VideoInfo object
    :param destination_path: Path to the destination directory where downloaded video will be stored

    :return: True if video was downloaded successfully, false otherwise
    """

    logger = logging.getLogger()
    logger.info(f"Downloading {len(video.chapters)} chapters of video {video.video_number} to {destination_path}")

    makedirs(destination_path, exist_ok=True)
    for idx, chapter in enumerate(video.chapters):
        logger.info(f"Downloading chapter #{idx + 1} {chapter.file_name} ({chapter.file_size / 1e6:.1f}MB)")

        # Calculate time required to download a chapter based on minimal expected download speed
        # Note that minimal value here is for miscellaneous procedures (setting up the connection etc.)
        download_timeout = max(chapter.file_size / (ingest_config.LOWEST_DOWNLOAD_SPEED_MBYTES_PER_SECOND * 1e6), 5)

        download_thread = threading.Thread(target=download_chapter,
                                           args=(chapter, f"{destination_path}/{chapter.file_name}"))
        download_thread.start()
        download_thread.join(download_timeout)
        # Apparently this is a way to check if thread timed out
        if download_thread.is_alive():
            logger.warning(f"Downloading chapter failed: timeout ({download_timeout}s)")
            return False

    logger.info(f"Downloaded video {video.video_number}")
    return True
