import requests
from dataclasses import dataclass

from file_management import parse_media_list
from video_downloader import download_video


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

    def __init__(self, ip_address: str, port: int):
        """
        Construct connection-capable HTTP client
        :param ip_address: Address of GoPro camera. Most common value is 10.5.5.9
        :param port: Port that exposes GoPro's api. Most common value is 8080
        """
        self.ip_address = ip_address
        self.port = port

    def execute_json_command(self, api_command: str) -> dict:
        """
        Send the request and return the
        :param api_command: API request string
        :return: JSON response if successful, exception is thrown otherwise
        """
        response = requests.get(f"http://{self.ip_address}:{self.port}/{api_command}", timeout=2)
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

    def get_video_info(self):
        response = self.execute_json_command("gp/gpMediaList")
        return parse_media_list(response["media"])


client = HttpClient("10.5.5.9", 8080)

gopro_status = client.get_gopro_status()
video_info = client.get_video_info()
print(video_info)
download_video("10.5.5.9", 8080, video_info[0], "./movie")
