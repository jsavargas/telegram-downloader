import json
import os
from datetime import datetime

from env import Env


class FileDataHandler:
    def __init__(self):
        self.env = Env()
        self.data_path = self.env.DOWNLOAD_FILES_DB
        self.downloads = self.load_from_json()
        self.limit = 5000
        self.max_items = 5000

    def save_to_json(self):
        with open(self.data_path, "w") as file:
            json.dump(self.downloads[-self.max_items :], file, indent=2)

    def load_from_json(self):
        try:
            if os.path.exists(self.data_path):
                with open(self.data_path, "r") as data_path:
                    data = json.load(data_path)
                    return data[-5000:]

        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"load_from_json Exception: {e}")
            return []

    def add_download_files(self, user_id, origin_group, message_id, original_filename):
        try:
            download_info = {
                "user_id": user_id,
                "origin_group": origin_group,
                "message_id": message_id,
                "original_filename": original_filename,
                "new_filename": None,
                "download_date": str(datetime.now()),
                "update_date": None,  # Will be updated when necessary
            }

            # Add download information
            self.downloads.append(download_info)

            # Save to the JSON file
            self.save_to_json()
        except Exception as e:
            print(f"add_download_files Exception: {user_id}, {e}")

    def update_download_files(self, message_id, new_filename):
        print(
            f"update_download_files => record: {message_id}, {new_filename}"
        )

        try:
            for record in self.downloads:
                if (record["message_id"] == message_id):
                    record["new_filename"] = new_filename
                    record["update_date"] = str(datetime.now())

                    self.save_to_json()

                    return True
            return False

        except Exception as e:
            print(f"update_download_files => Exception: {e}")
            return None

    def get_download_file(self, message_id):
        self.downloads = self.load_from_json()

        found_element = next(
            (
                download_info["new_filename"] if download_info.get("new_filename") is not None else download_info["original_filename"]
                for download_info in self.downloads
                if download_info["message_id"] == message_id
            ),
            None,
        )
        return found_element
