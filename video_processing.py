import logging
from time import sleep


def process_video(video_path: str) -> bool:
    """
    Mock function for testing purposes
    :param video_path: Path to the directory containing video chapters
    :return: True if processing went successful
    """
    """"""
    logger = logging.getLogger()
    logger.info(f"Processing video {video_path}")
    sleep(3)
    logger.info(f"Finished processing video {video_path}")
    return True
