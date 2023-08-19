import concurrent.futures
import threading
from typing import List

from file_management import VideoInfo
from video_processing import process_video
from video_downloader import download_video
import ingest_config


class ThreadWithReturnValue(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return: bool = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self, *args) -> bool:
        threading.Thread.join(self, *args)
        return self._return


class VideoIngester:
    def __init__(self):
        self.process_pool = concurrent.futures.ThreadPoolExecutor(1)

    @staticmethod
    def get_download_path(video: VideoInfo):
        return f"{ingest_config.DOWNLOAD_DIR}/{video.video_number}"

    @staticmethod
    def download_video(video: VideoInfo) -> bool:
        download_path = VideoIngester.get_download_path(video)
        download_thread = ThreadWithReturnValue(target=download_video, args=(video, download_path))
        download_thread.start()
        return download_thread.join()

    def main_loop(self, videos: List[VideoInfo]):
        """
        Main worker loop that downloads and processes the videos concurrently.
        Note that multiple processing steps may overlap.

        :param videos: List of videos to download and process
        """

        for video in videos:
            print(self.download_video(video))
            self.process_pool.submit(process_video, VideoIngester.get_download_path(video))
