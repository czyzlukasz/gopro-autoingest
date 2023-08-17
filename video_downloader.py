import logging
import wget
from os import makedirs
from file_management import VideoInfo, ChapterInfo


def download_chapter(ip_address: str, port: int, chapter: ChapterInfo, destination_path: str):
    """
    Download single file from GoPro
    :param ip_address: Address of GoPro camera. Most common value is 10.5.5.9
    :param port: Port that exposes GoPro's api. Most common value is 8080
    :param chapter: Valid ChapterInfo object
    :param destination_path: Path to the destination file where downloaded chapter will be stored
    """
    full_address = f"http://{ip_address}:{port}/videos/DCIM/{chapter.parent_directory}/{chapter.file_name}"
    wget.download(full_address, destination_path)


def download_video(ip_address: str, port: int, video: VideoInfo, destination_path: str):
    """
    Download single video consisting of multiple chapters.
    Chapters will be stored in specified destination directory with chapters saved as destination_path/chapter_number.mp4
    :param ip_address: Address of GoPro camera. Most common value is 10.5.5.9
    :param port: Port that exposes GoPro's api. Most common value is 8080
    :param video: Valid VideoInfo object
    :param destination_path: Path to the destination directory where downloaded video will be stored
    """
    makedirs(destination_path, exist_ok=True)
    logging.info(f"Downloading {len(video.chapters)} chapters to {destination_path}")
    for idx, chapter in enumerate(video.chapters):
        logging.info(f"Downloading chapter #{idx + 1} {chapter.file_name} ({chapter.file_size / 1e6:.1f}MB)")
        download_chapter(ip_address, port, chapter, f"{destination_path}/{idx}.mp4")
