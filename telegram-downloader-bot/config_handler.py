import os
import configparser
from env import Env


class ConfigHandler:
    def __init__(self):
        self.env = Env()
        self.config_path = os.path.join(self.env.CONFIG_PATH, "config.ini")
        self._initialize_config()

    def _initialize_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_path):
            config.read(self.config_path)
        
        if not os.path.exists(self.config_path):
            # Sección por defecto
            config['DEFAULT'] = {
                'default_path': os.getenv('DEFAULT_PATH', self.env.DOWNLOAD_COMPLETED_PATH)
            }
            
            # Ejemplo de rutas por extensión
            config['EXTENSIONS'] = {
                'pdf': '/download/pdf',
                'jpg': '/download/images',
                'mp4': '/download/videos'
            }
            
            # Ejemplo de rutas por grupo
            config['GROUP_PATHS'] = {}
            
            with open(self.config_path, 'w') as configfile:
                config.write(configfile)

        if not config.has_section("GROUP_PATHS"):
            config.add_section("GROUP_PATHS")
            config["GROUP_PATHS"] = {}
            with open(self.config_path, "w") as config_file:
                config.write(config_file)
        if not config.has_section("EXTENSIONS"):
            config.add_section("EXTENSIONS")
            config['EXTENSIONS'] = {
                'pdf': '/download/pdf',
                'jpg': '/download/images',
                'mp4': '/download/videos'
            }
            with open(self.config_path, "w") as config_file:
                config.write(config_file)

    def get_download_path(self, ext):
        if ext == 'torrent': return self.env.DOWNLOAD_PATH_TORRENTS
        config = configparser.ConfigParser()
        config.read(self.config_path)
        DEFAULT_PATH = config['DEFAULT']['default_path'] if config['DEFAULT'] else self.env.DOWNLOAD_COMPLETED_PATH
        return config['EXTENSIONS'].get(ext, DEFAULT_PATH)

    def get_group_path(self, group_id):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        return config['GROUP_PATHS'].get(str(group_id), None)

    def add_path(self, ext, path):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        if 'EXTENSIONS' not in config:
            config['EXTENSIONS'] = {}
        config['EXTENSIONS'][ext] = path
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)

    def add_group_path(self, group_id, path):
        try:
            config = configparser.ConfigParser()
            config.read(self.config_path)
            if 'GROUP_PATHS' not in config:
                config['GROUP_PATHS'] = {}
            config['GROUP_PATHS'][group_id] = path
            with open(self.config_path, 'w') as configfile:
                config.write(configfile)

        except Exception as e:
            print(f"ConfigHandler add_group_path Exception: {e}")