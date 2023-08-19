import logging

import ingest_config
from http_connector import HttpClient
from video_ingest import VideoIngester


def setup_logging():
    logging.basicConfig(level=ingest_config.LOGGING_LEVEL)
    logger = logging.getLogger()
    handler = logging.FileHandler(ingest_config.LOG_FILE, 'w+')

    handler.setFormatter(logging.Formatter(fmt='%(asctime)s|%(levelname)s: %(message)s'))
    logger.addHandler(handler)


if __name__ == '__main__':
    setup_logging()

    client = HttpClient()
    video_info = client.get_video_info()
    video_ingester = VideoIngester()
    video_ingester.main_loop(video_info[1:4])
