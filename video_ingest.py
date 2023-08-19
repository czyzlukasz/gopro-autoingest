import concurrent.futures
import logging
import threading
from typing import List

from file_management import VideoInfo
from video_processing import process_video
from video_downloader import download_video
import ingest_config


class VideoIngester:
    def __init__(self):
        self.process_pool = concurrent.futures.ThreadPoolExecutor(1)

    @staticmethod
    def get_download_path(video: VideoInfo):
        return f"{ingest_config.DOWNLOAD_DIR}/{video.video_number}"

    def main_loop(self, videos: List[VideoInfo]):
        """
        Main worker loop that downloads and processes the videos concurrently.

        :param videos: List of videos to download and process
        """

        for video in videos:
            download_path = VideoIngester.get_download_path(video)
            if not download_video(video, download_path):
                logging.warning("Skipping video processing due to the download failure")
                continue
            self.process_pool.submit(process_video, download_path)
