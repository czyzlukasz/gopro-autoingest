import logging
import os.path
import subprocess
import tempfile
from os import makedirs

from typing import List, IO

import ingest_config
from file_management import VideoInfo


def get_input_file_names(video: VideoInfo):
    """
    Create list of absolute paths to video's chapters
    :param video: Info of the video being processed
    :return: List of absolute paths
    """
    return [f"{ingest_config.STAGING_DIR}/{video.video_number}/{chapter.file_name}" for chapter in video.chapters]


def prepare_input_file(input_files: List[str]) -> IO:
    """
    Create special file with instructions for the ffmpeg's concat
    :param input_files: List of absolute paths to videos to concatenate
    :return: File handle with instructions
    """
    temp_file = open(ingest_config.INPUT_FILE_PATH, "w+")
    temp_file.writelines([f"file \'{input_path}\'\n" for input_path in input_files])
    temp_file.close()
    return temp_file


def get_output_file_name(video: VideoInfo, suffix="") -> str:
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


def prepare_ffmpeg_spell(input_file_name: str, output_file: str) -> List[str]:
    """
    Generate ready-to-execute spell
    :param input_file_name: File containing video file paths to concat
    :param output_file: Path where final video will be stored
    :return: Final spell
    """
    return ["ffmpeg", "-safe", "0", "-f", "concat", "-i", input_file_name,
            "-map", "0:v", "-map", "0:a", "-map", "0:3",
            "-copy_unknown", "-tag:2", "gpmd", "-c", "copy", output_file]


def process_video(download_path: str, video_info: VideoInfo) -> bool:
    """
    Combine multiple chapters and render them to a single video.
    :param download_path: Directory where all chapters are located
    :param video_info: Info of the video being processed
    :return: True if the processing went successful, false otherwise
    """
    logger = logging.getLogger()

    input_file_names = get_input_file_names(video_info)
    output_file_name = get_output_file_name(video_info)

    logger.info(f"Processing video {video_info.video_number} to {output_file_name}")

    # Prepare output directory to make ffmpeg happy
    makedirs(ingest_config.STORAGE_DIR, exist_ok=True)

    # ffmpeg's concat can only read from file thus special file is needed
    # TODO: Remove that file
    input_file = prepare_input_file(input_file_names)
    ffmpeg_spell = prepare_ffmpeg_spell(input_file.name, output_file_name)
    logger.debug(f"Prepared ffmpeg spell: {ffmpeg_spell}")
    try:
        subprocess.run(ffmpeg_spell, check=True)
    except subprocess.CalledProcessError as exception:
        logger.error(f"Failed to process video (generic exception): {type(exception)} {exception}")
        return False
    else:
        logger.info(f"Finished processing video {video_info.video_number}")
        return True
