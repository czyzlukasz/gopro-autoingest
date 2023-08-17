import logging

from http_connector import HttpClient
from video_ingest import VideoIngester

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    client = HttpClient("10.5.5.9", 8080)
    video_info = client.get_video_info()
    video_ingester = VideoIngester("10.5.5.9", 8080)
    video_ingester.main_loop(video_info[1:4])
