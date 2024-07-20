# utils.py
import os
import time
from env import Env

class Utils:
    def __init__(self):

        self.env = Env()
        self.permissions_folder = 0o777
        self.permissions_file = 0o755
        self.PUID = self.env.PUID 
        self.PGID = self.env.PGID
        self.change_permissions()

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
        download_folder = download_info['download_folder']
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
            f"**Download Folder:** {download_folder}\n"
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

    def change_permissions(self):
        os.chown(self.env.DOWNLOAD_PATH, self.PUID, self.PGID)

    def change_permissions_owner(self, file_name):
        """Changes the permissions and owner of the specified file."""
        try:
            if os.path.isfile(file_name): os.chmod(file_name, self.permissions_file)
            elif os.path.isdir(file_name): os.chmod(file_name, self.permissions_folder)
            else: os.chmod(file_name, self.permissions_file)
            os.chown(file_name, self.PUID, self.PGID)
            print(f"Successfully changed permissions and owner of {file_name}")
        except Exception as e:
            print(f"Failed to change permissions and owner: {e}")

    def getDownloadFolder(self, file_name):

        download_folder = self.env.DOWNLOAD_PATH
        final_path = os.path.join(self.env.DOWNLOAD_PATH, file_name)

        try:
            if file_name.endswith(".torrent"):
                download_folder = self.env.DOWNLOAD_PATH_TORRENTS
    
            # Create the download folder if needed
            self.create_folders(download_folder)

            # Construct the final path
            final_path = os.path.join(download_folder, file_name)

            print(f"getDownloadFolder: download_folder: {download_folder}, final_path: {final_path}")  # Enhanced logging

            return download_folder, final_path

        except Exception as e:
            print(f"getDownloadFolder Failed: {e}")
            return download_folder, final_path

    def getDownloadFolderTemp(self, file_name):
        final_path = os.path.join(self.env.DOWNLOAD_INCOMPLETED_PATH, file_name)
        try:
            self.create_folders(final_path)
            return final_path
        except Exception as e:
            print(f"getDownloadFolderTemp Failed: {e}")
            return final_path

    def create_folders(self, folder_name):
        try:
            print(f"create_folders path: {folder_name}")
            # Verificar si la folder_name es un archivo
            if os.path.isfile(folder_name):
                print(f"create_folders isfile: {folder_name}")
                base_directory = os.path.dirname(folder_name)
                os.makedirs(base_directory, exist_ok=True) 
                self.change_permissions_owner(base_directory)
            elif os.path.isdir(folder_name):
                print(f"create_folders isdir: {folder_name}")
                os.makedirs(folder_name, exist_ok=True) 
                self.change_permissions_owner(folder_name)
            else:
                print(f"create_folders else: {folder_name}")
                dirname = os.path.dirname(folder_name)
                base_directory = os.path.basename(folder_name)
                if "." not in base_directory:
                    os.makedirs(folder_name, exist_ok=True) 
                else:
                    os.makedirs(dirname, exist_ok=True) 
                print(f"create_folders else: [{folder_name}] [{base_directory}] [{dirname}] " )


        except FileExistsError as e:
            print(f"The folder {folder_name} already exists: {e}")
        except Exception as e:
            print(f"create_folders Exception: {folder_name}: {e}")

    def startTime(self):
        start_time = time.time()
        start_hour = time.strftime("%H:%M:%S", time.localtime(start_time))

        return start_time, start_hour

    def endTime(self):
        end_time = time.time()
        end_hour = time.strftime("%H:%M:%S", time.localtime(end_time))

        return end_time, end_hour

    def elapsedTime(self, start_time, end_time):
        elapsed_time = end_time - start_time
        
        return elapsed_time
        
    def getSize(self, file_path):
        size_str = ""
        try:
            file_size = os.path.getsize(file_path)

            if file_size < 1024:
                size_str = f"{file_size} bytes"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.2f} KB"
            else:
                size_str = f"{file_size / (1024 * 1024):.2f} MB"

        except Exception as e:
            print(f"getSize Exception: {file_path}: {e}")
            file_size = 0
        return file_size, size_str
