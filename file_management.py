import glob
import logging
import os
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List
from collections import defaultdict
import datetime

import ingest_config


@dataclass_json
@dataclass
class ChapterInfo:
    parent_directory: str
    file_name: str
    chapter_number: int
    date_created: datetime.datetime
    file_size: int


@dataclass_json
@dataclass
class VideoInfo:
    video_number: int
    date_created: datetime.datetime
    chapters: List[ChapterInfo]


class FileNameParser:
    """
    See https://community.gopro.com/s/article/GoPro-Camera-File-Naming-Convention for explanation.
    """

    def __init__(self, file_name: str):
        self.video_number = int(file_name[4:8])
        self.chapter_number = int(file_name[2:4])


def parse_chapters(media_list: List[dict]) -> List[ChapterInfo]:
    """
    Parse list of files into separate chapters (single video files).

    :param media_list: JSON dict from 'gpMediaList' request
    :return: List of found chapters
    """

    result: List[ChapterInfo] = []

    for directory_dict in media_list:
        directory = directory_dict["d"]
        files = directory_dict["fs"]
        for file in files:
            file_name = file["n"]
            parsed_file_name = FileNameParser(file_name)
            creation_date = datetime.datetime.fromtimestamp(int(file["cre"]))
            size = int(file["s"])

            chapter_info = ChapterInfo(
                parent_directory=directory,
                file_name=file_name,
                chapter_number=parsed_file_name.chapter_number,
                date_created=creation_date,
                file_size=size)
            result.append(chapter_info)

    return result


def parse_media_list(media_list: List[dict]) -> List[VideoInfo]:
    """
    Parse list of files into separate videos (compositions of chapters). Each video consists of at leas one chapter

    :param media_list: JSON dict from 'gpMediaList' request
    :return: List of found videos
    """

    result: List[VideoInfo] = []

    # Step one: find video numbers with corresponding chapters
    chapters = parse_chapters(media_list)
    videos = defaultdict(list)
    for chapter in chapters:
        parsed_file_name = FileNameParser(chapter.file_name)
        videos[parsed_file_name.video_number].append(chapter)

    # Step two: aggregate chapters of each video together
    for video_number in videos:
        video_chapters = sorted(videos[video_number], key=lambda item: item.chapter_number)
        first_chapter: ChapterInfo = video_chapters[0]

        video_info = VideoInfo(
            video_number=video_number,
            date_created=first_chapter.date_created,
            chapters=video_chapters
        )
        result.append(video_info)

    return result


def get_video_info_from_staging() -> List[VideoInfo]:
    """
    Fetch all staged videos that contain video_info.json file and parse them to VideoInfo
    :return: List of VideoInfo found
    """
    result: List[VideoInfo] = []
    video_info_paths = glob.glob(f"{ingest_config.STAGING_DIR}/*[1000-9999]/video_info.json")
    for video_info_path in video_info_paths:
        with open(video_info_path, "r") as video_info_file:
            video_info = VideoInfo.from_json(video_info_file.read())
            result.append(video_info)
    return result
