import concurrent.futures
import logging
from typing import List

from file_management import VideoInfo
from video_processing import process_video
from video_downloader import download_video
import ingest_config


class VideoIngester:
    def __init__(self):
        self.process_pool = concurrent.futures.ThreadPoolExecutor(1)

    @staticmethod
    def get_staging_path(video: VideoInfo) -> str:
        return f"{ingest_config.STAGING_DIR}/{video.video_number}"

    def main_loop(self, videos: List[VideoInfo]):
        """
        Main worker loop that downloads and processes the videos concurrently.

        :param videos: List of videos to download and process
        """

        process_future = None
        for video in videos:
            staging_path = VideoIngester.get_staging_path(video)
            if not download_video(video, staging_path):
                logging.warning("Skipping video processing due to the download failure")
                continue
            process_future = self.process_pool.submit(process_video, staging_path)

        # Wait for lass processing thread to finish
        if process_future is not None:
            process_future.result()
