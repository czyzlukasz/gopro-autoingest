import argparse

import ingest_routines

FUNCTION_MAP = {
    'download': ingest_routines.download_videos,
    'process': ingest_routines.process_videos,
    'archive': ingest_routines.archive_video,
}

if __name__ == '__main__':
    ingest_routines.setup_logging()
    ingest_routines.log_parameters()

    parser = argparse.ArgumentParser(
        prog='GoPro Auto-ingest',
        description='Automatically upload GoPro footage to a destination of Your choice')
    parser.add_argument('command', choices=FUNCTION_MAP)
    args = parser.parse_args()

    FUNCTION_MAP[args.command]()
