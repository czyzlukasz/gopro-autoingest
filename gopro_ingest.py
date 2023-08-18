import logging

import ingest_config
from http_connector import HttpClient
from video_ingest import VideoIngester

if __name__ == '__main__':
    logging.basicConfig(level=ingest_config.LOGGING_LEVEL)

    client = HttpClient()
    video_info = client.get_video_info()
    video_ingester = VideoIngester()
    video_ingester.main_loop(video_info[1:4])
