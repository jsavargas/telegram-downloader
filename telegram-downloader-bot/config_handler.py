import os
import configparser
from env import Env


class ConfigHandler:
    def __init__(self):
        self.env = Env()
        self.default_extensions = {'jpg': '/download/images'}
        self.default_group_paths = {'-100123456': '/download/completed'}
        self.default_rename_group = {'-100123456': 'yes'}
        self.default_keywords = {'tanganana': '/download/completed'}

        self.config_file = os.path.join(self.env.CONFIG_PATH, "config.ini")
        self.config = self._initialize_config()
        self.config.read(self.config_file)
    
    
    def _create_default_config(self):
        if not os.path.exists(self.config_file):
            print("_create_default_config")
            self.config['DEFAULT'] = {'default_path': os.getenv('DEFAULT_PATH', self.env.DOWNLOAD_COMPLETED_PATH)}
            self.config['EXTENSIONS'] = self.default_extensions
            self.config['GROUP_PATHS'] = self.default_group_paths
            self.config['RENAME_GROUP'] = self.default_rename_group
            self.config['KEYWORDS'] = self.default_keywords
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)

    def _initialize_config(self):
        config = configparser.ConfigParser()
        if not config.read(self.config_file):
            self._create_default_config()

        if not config.has_section("EXTENSIONS"):
            config.add_section("EXTENSIONS")
            config['EXTENSIONS'] = self.default_extensions
            with open(self.config_file, "w") as config_file:
                config.write(config_file)
        if not config.has_section("GROUP_PATHS"):
            config.add_section("GROUP_PATHS")
            config["GROUP_PATHS"] = self.default_group_paths
            with open(self.config_file, "w") as config_file:
                config.write(config_file)
        if not config.has_section("RENAME_GROUP"):
            config.add_section("RENAME_GROUP")
            config["RENAME_GROUP"] = self.default_rename_group
            with open(self.config_file, "w") as config_file:
                config.write(config_file)
        if not config.has_section("KEYWORDS"):
            config.add_section("KEYWORDS")
            config["KEYWORDS"] = self.default_keywords
            with open(self.config_file, "w") as config_file:
                config.write(config_file)
        if 'default_path' not in config['DEFAULT']:
            config['DEFAULT']['default_path'] = self.env.DOWNLOAD_COMPLETED_PATH
            with open(self.config_file, 'w') as configfile:
                config.write(configfile)

        return config

    def get_download_path(self, origin_group, file_name, message = {}):
        self.config.read(self.config_file)
        extension = file_name.split('.')[-1]
        caption = message.caption if message.caption else None
        
        if extension == 'torrent': return self.env.DOWNLOAD_PATH_TORRENTS
        return (
            self.get_keyword_path(caption) or
            self.get_group_path(origin_group) or
            self.get_extension_path(extension)
        )

    def get_keyword_path(self, text):
        for keyword, path in self.config['KEYWORDS'].items():
            if keyword in text.lower():
                return path
        return None

    def get_group_path(self, group_id):
        return self.config['GROUP_PATHS'].get(str(group_id), None)

    def get_extension_path(self, extension):
        if extension == 'torrent': return self.env.DOWNLOAD_PATH_TORRENTS
        DEFAULT_PATH = self.config['DEFAULT']['default_path'] if "default_path" in self.config['DEFAULT'] else self.env.DOWNLOAD_COMPLETED_PATH
        return self.config['EXTENSIONS'].get(extension, DEFAULT_PATH)

    def get_file_rename(self, group_id, file_name, message):
        self.config.read(self.config_file)
        print(f"group_id: {group_id}, file_name: {file_name}")
        if not self.config['RENAME_GROUP'].get(str(group_id), None):
            return file_name

        if not message.caption:
            return file_name

        ext = file_name.split('.')[-1]
        caption = message.caption
        return f"{caption}.{ext}"
        

    def add_path(self, ext, path):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        if 'EXTENSIONS' not in config:
            config['EXTENSIONS'] = {}
        config['EXTENSIONS'][ext] = path
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

    def add_group_path(self, group_id, path):
        self.config['GROUP_PATHS'][str(group_id)] = path
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def add_keyword_path(self, keyword, path):
        self.config['KEYWORDS'][keyword] = path
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def add_rename_group(self, group_id):
        self.config['RENAME_GROUP'][group_id] = 'yes'
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def remove_rename_group(self, group_id):
        if group_id in self.config['RENAME_GROUP']:
            del self.config['RENAME_GROUP'][group_id]
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)
