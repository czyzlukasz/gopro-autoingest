import threading
from typing import List

from file_management import VideoInfo
from video_processing import process_video
from video_downloader import download_video
import ingest_config


class VideoIngester:
    def main_loop(self, videos: List[VideoInfo]):
        """
        Main worker loop that downloads and processes the videos concurrently.
        Note that multiple processing steps may overlap.

        :param videos: List of videos to download and process
        """
        threads = []

        for video in videos:
            download_path = f"{ingest_config.DOWNLOAD_DIR}/{video.video_number}"

            # Step 1: Download
            download_thread = threading.Thread(
                target=download_video, args=(video, download_path))
            threads.append(download_thread)
            download_thread.start()
            download_thread.join(ingest_config.VIDEO_DOWNLOAD_TIMEOUT)

            # Step 2: Process
            process_thread = threading.Thread(target=process_video, args=(download_path,))
            threads.append(process_thread)
            process_thread.start()

        [thread.join() for thread in threads]
