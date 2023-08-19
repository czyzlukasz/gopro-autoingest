import concurrent.futures
import logging
from shutil import rmtree as rm_rf
from typing import List

from file_management import VideoInfo
from video_processing import process_video
from video_downloader import download_video
import ingest_config


class VideoIngester:
    def __init__(self):
        self.process_pool = concurrent.futures.ThreadPoolExecutor(1)
        self.successfully_processed_videos: List[VideoInfo] = []

    @staticmethod
    def get_staging_path(video: VideoInfo) -> str:
        return f"{ingest_config.STAGING_DIR}/{video.video_number}"

    def process_video(self, video: VideoInfo, staging_path: str):
        if process_video(staging_path):
            self.successfully_processed_videos.append(video)

    def remove_processed_videos_from_staging(self):
        logger = logging.getLogger()

        logger.info(
            f"Successfully processed {len(self.successfully_processed_videos)} videos. Removing them from staging area")

        for video in self.successfully_processed_videos:
            staging_path = VideoIngester.get_staging_path(video)
            logger.debug(f"Calling rm -rf on {staging_path}")
            # TODO: uncomment that when ready
            # rm_rf(staging_path)

    def main_loop(self, videos: List[VideoInfo]):
        """
        Main worker loop that downloads and processes the videos concurrently.

        :param videos: List of videos to download and process
        """

        logger = logging.getLogger()
        process_future = None

        for video in videos:
            staging_path = VideoIngester.get_staging_path(video)
            if not download_video(video, staging_path):
                logger.warning("Skipping video processing due to the download failure")
                continue

            process_future = self.process_pool.submit(self.process_video, video, staging_path)

        # Wait for lass processing thread to finish
        if process_future is not None:
            process_future.result()

        self.remove_processed_videos_from_staging()
