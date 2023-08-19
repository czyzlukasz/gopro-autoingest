import logging
from time import sleep


def process_video(video_path: str):
    """Mock function for testing purposes"""
    logger = logging.getLogger()
    logger.info(f"Processing video {video_path}")
    sleep(3)
    logger.info(f"Finished processing video {video_path}")
