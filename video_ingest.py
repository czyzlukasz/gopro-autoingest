import logging
import threading
from typing import List

from file_management import VideoInfo
from video_processing import process_video
from video_downloader import download_video


class VideoIngester:
    def __init__(self, ip_address: str, port: int):
        """
        Construct connection-capable HTTP client
        :param ip_address: Address of GoPro camera. Most common value is 10.5.5.9
        :param port: Port that exposes GoPro's api. Most common value is 8080
        """
        self.ip_address = ip_address
        self.port = port

    def main_loop(self, videos: List[VideoInfo]):
        """
        Main worker loop that downloads and processes the videos concurrently.
        Note that multiple processing steps may overlap.

        :param videos: List of videos to download and process
        """
        threads = []

        for video in videos:
            download_path = f"./tmp/video/{video.video_number}"

            # Step 1: Download
            download_thread = threading.Thread(
                target=download_video, args=(self.ip_address, self.port, video, download_path))
            threads.append(download_thread)
            download_thread.start()
            download_thread.join()

            # Step 2: Process
            process_thread = threading.Thread(target=process_video, args=(download_path,))
            threads.append(process_thread)
            process_thread.start()

        [thread.join() for thread in threads]
