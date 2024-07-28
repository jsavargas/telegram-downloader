import os
import configparser
from env import Env


class ConfigHandler:
    def __init__(self):
        self.env = Env()
        self.config_path = os.path.join(self.env.CONFIG_PATH, "config.ini")
        self._initialize_config()

    def _initialize_config(self):
        if not os.path.exists(self.config_path):
            config = configparser.ConfigParser()
            
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

    def get_download_path(self, ext):
        config = configparser.ConfigParser()
        config.read(self.config_path)
        return config['EXTENSIONS'].get(ext, config['DEFAULT']['default_path'])

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