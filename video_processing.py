import logging
import ffmpeg
from typing import List

import ingest_config
from file_management import VideoInfo, ChapterInfo


def concatenate_chapters(download_path: str, chapters: List[ChapterInfo]):
    chapter_file_list = [ffmpeg.input(f"{download_path}/{chapter.file_name}") for chapter in chapters]
    return ffmpeg.concat(*chapter_file_list)


def process_video(video_path: str, video_info: VideoInfo):
    """Mock function for testing purposes"""
    logger = logging.getLogger()
    logger.info(f"Processing video {video_info.video_number}")
    chapter_stream = concatenate_chapters(video_path, video_info.chapters)
    # TODO: add downscaling, if necessary. For now rendering with different CRF seems enough
    output_stream = ffmpeg.output(chapter_stream, "out.mp4", vcodec='libx265', crf=ingest_config.OUTPUT_VIDEO_CRF)
    # Force overwriting destination file. This should not happen, but it prevents from being stuck indefinitely
    output_stream = output_stream.global_args("-y")
    try:
        output_stream.run()
    except ffmpeg.Error as exception:
        logger.error(f"Failed to process video: {type(exception)} {exception}")
        return False
    else:
        logger.info(f"Finished processing video {video_info.video_number}")
        return True
