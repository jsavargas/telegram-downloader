# utils.py
import os
from env import Env

class Utils:
    def __init__(self):

        self.env = Env()
        self.permissions_folder = 0o644
        self.permissions_file = 0o644
        self.owner = "root"
        self.PUID = self.env.PUID 
        self.PGID = self.env.PGID 

    def format_file_size(self, file_size: int) -> str:
        if file_size < 1024:
            return f"{file_size} bytes"
        elif file_size < 1024 * 1024:
            return f"{file_size / 1024:.2f} KB"
        else:
            return f"{file_size / (1024 * 1024):.2f} MB"

    def create_download_summary(self, download_info):
        """
        Creates a download summary message based on the download information.

        Args:
        - download_info (dict): Dictionary with the following structure:
            {
                'file_name': str,
                'size_str': str,
                'start_hour': str,
                'end_hour': str,
                'elapsed_time': float,
                'download_speed': float,
                'origin_group': str or None (optional)
            }
        
        Returns:
        - str: Formatted download summary message.
        """
        file_name = download_info['file_name']
        size_str = download_info['size_str']
        start_hour = download_info['start_hour']
        end_hour = download_info['end_hour']
        elapsed_time = download_info['elapsed_time']
        download_speed = download_info['download_speed']
        origin_group = download_info.get('origin_group', None)
        retries = download_info.get('retries', None)

        summary = (
            f"**Download completed**\n\n"
            f"**File Name:** {file_name}\n"
            f"**File Size:** {size_str}\n"
            f"**Start Time:** {start_hour}\n"
            f"**End Time:** {end_hour}\n"
            f"**Download Time:** {elapsed_time:.2f} seconds\n"
            f"**Download Speed:** {download_speed:.2f} KB/s"
        )

        if origin_group:
            summary += f"\n**Origin Group:** {origin_group}"
        if retries:
            summary += f"\n**Retries:** {retries}"

        return summary

    def removeFiles(self):
        if os.path.exists("telegramBot.session"): 
            os.remove("telegramBot.session")

    def change_permissions_owner(self, file_name):
        """Changes the permissions and owner of the specified file."""
        try:
            os.chmod(file_name, self.permissions_folder)
            os.chown(file_name, self.PUID, self.PGID)
            print(f"Successfully changed permissions and owner of {file_path}")
        except Exception as e:
            print(f"Failed to change permissions and owner: {e}")

