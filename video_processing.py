import logging
import os.path
from os import makedirs

import ffmpeg
from typing import List

import ingest_config
from file_management import VideoInfo, ChapterInfo


def get_output_file_name(video: VideoInfo, suffix=""):
    """
    Prepare path to the final output video.
    Note that in case of the file with the same name existing a suffix will be added.
    :param video: Info of the video being processed
    :param suffix: Suffix to be added to the final video name
    :return: Path to the output video
    """
    video_name = video.chapters[0].date_created.strftime(ingest_config.OUTPUT_VIDEO_NAME_FORMAT)
    file_name = f"{ingest_config.STORAGE_DIR}/{video_name}{suffix}.mp4"
    if os.path.isfile(file_name):
        return get_output_file_name(video, suffix + "X")
    return file_name


def concatenate_chapters(download_path: str, chapters: List[ChapterInfo]):
    """
    Create a stream consisting of chapters.
    Note that the stream will be in the same sequence that chapters in 'chapters' list
    :param download_path: Directory where all chapters are located
    :param chapters: List of chapters to concatenate
    :return: Concatenated stream
    """
    chapter_file_list = [ffmpeg.input(f"{download_path}/{chapter.file_name}") for chapter in chapters]
    return ffmpeg.concat(*chapter_file_list)


def process_video(download_path: str, video_info: VideoInfo) -> bool:
    """
    Combine multiple chapters and render them to a single video.
    :param download_path: Directory where all chapters are located
    :param video_info: Info of the video being processed
    :return: True if the processing went successful, false otherwise
    """
    logger = logging.getLogger()

    output_file_name = get_output_file_name(video_info)
    # Prepare output directory to make ffmpeg happy
    makedirs(ingest_config.STORAGE_DIR, exist_ok=True)
    logger.info(f"Processing video {video_info.video_number} to {output_file_name}")

    try:
        chapter_stream = concatenate_chapters(download_path, video_info.chapters)
        # TODO: add downscaling, if necessary. For now rendering with different CRF seems enough
        output_stream = ffmpeg.output(chapter_stream, output_file_name, vcodec='libx265',
                                      crf=ingest_config.OUTPUT_VIDEO_CRF)
        # Force overwriting destination file. This should not happen, but it prevents from being stuck indefinitely
        output_stream = output_stream.global_args("-y")
        output_stream.run()
    except ffmpeg.Error as exception:
        logger.error(f"Failed to process video: {type(exception)} {exception}")
        return False
    else:
        logger.info(f"Finished processing video {video_info.video_number}")
        return True
