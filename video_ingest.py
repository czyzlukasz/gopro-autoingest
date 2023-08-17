import logging
import multiprocessing
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
        processes = []

        for video in videos:
            download_path = f"./tmp/video/{video.video_number}"

            # Step 1: Download
            download_process = multiprocessing.Process(
                target=download_video, args=(self.ip_address, self.port, video, download_path))
            processes.append(download_process)
            download_process.start()
            download_process.join()

            if download_process.exitcode != 0:
                logging.warning(f"Downloading failed: {download_process.exitcode}. Skipping video processing")
                continue

            # Step 2: Process
            process_process = multiprocessing.Process(target=process_video, args=(download_path,))
            processes.append(process_process)
            process_process.start()

        [process.join() for process in processes]
