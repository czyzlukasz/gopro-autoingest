import requests
from typing import List
from dataclasses import dataclass

import ingest_config
from file_management import parse_media_list, VideoInfo


class RequestFailedException(Exception):
    def __init__(self, response: requests.Response):
        super().__init__(f"Request {response.request.url} returned {response}")


@dataclass
class GoProStatus:
    battery_available: bool
    remaining_space: int  # Value in bytes


class HttpClient:
    """
    HTTP client interfacing with GoPro's API.
    All magic values are documented in https://github.com/KonradIT/goprowifihack
    and should be more-or-less compatible for GoPro 4 up to GoPro 8.
    """

    RESPONSE_OK = 200

    def execute_json_command(self, api_command: str) -> dict:
        """
        Send the request and return the
        :param api_command: API request string
        :return: JSON response if successful, exception is thrown otherwise
        """
        response = requests.get(f"http://{ingest_config.GOPRO_IP}:{ingest_config.GOPRO_PORT}/{api_command}", timeout=2)
        if response.status_code is not self.RESPONSE_OK:
            raise RequestFailedException(response)
        return response.json()

    def get_gopro_status(self) -> GoProStatus:
        """
        Get GoPro status with basic information. Use this as healthcheck and/or heartbeat command
        :return: GoPro status info
        """
        response = self.execute_json_command("gp/gpControl/status")

        return GoProStatus(battery_available=response["status"]["1"], remaining_space=response["status"]["54"])

    def shutdown_camera(self):
        """
        Sends camera into sleep mode
        """
        self.execute_json_command("gp/gpControl/command/system/sleep")

    def enable_beeping(self):
        """
        Enable 'locate' mode that causes the camera to scream. Loud!
        """
        self.execute_json_command("gp/gpControl/command/system/locate?p=1")

    def disable_beeping(self):
        """
        Disable 'locate' mode
        """
        self.execute_json_command("gp/gpControl/command/system/locate?p=0")

    def get_video_info(self) -> List[VideoInfo]:
        response = self.execute_json_command("gp/gpMediaList")
        return parse_media_list(response["media"])
