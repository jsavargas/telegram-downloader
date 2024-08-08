import os
import configparser
from env import Env
from info_handler import InfoMessages


class ConfigHandler:
    def __init__(self):
        self.env = Env()
        self.info_handler = InfoMessages()

        self.default_extensions = {'jpg': '/download/images'}
        self.default_group_paths = {'-100123456': '/download/completed'}
        self.default_rename_group = {'-100123456': 'yes'}
        self.default_keywords = {'tanganana': '/download/completed'}
        self.default_group_paths = {'-100123456': '/download/completed'}
        self.default_regex_rename = {'-100123456': '/old_text/new_text/'}
        self.default_settings = {'chars_to_replace ': '|/'}

        self.config_file = os.path.join(self.env.CONFIG_PATH, "config.ini")
        self.config = self._initialize_config()
        self.config.read(self.config_file)
    
    
    def _create_default_config(self, config):
        if not os.path.exists(self.config_file):
            config['DEFAULT'] = {'default_path': os.getenv('DEFAULT_PATH', self.env.DOWNLOAD_COMPLETED_PATH)}
            config['EXTENSIONS'] = self.default_extensions
            config['GROUP_PATHS'] = self.default_group_paths
            config['RENAME_GROUP'] = self.default_rename_group
            config['KEYWORDS'] = self.default_keywords
            config['REGEX_RENAME'] = self.default_regex_rename
            config['SETTINGS'] = self.default_settings
            with open(self.config_file, 'w') as configfile:
                config.write(configfile)
            return config

    def _initialize_config(self):
        config = configparser.ConfigParser()
        if not config.read(self.config_file):
            config = self._create_default_config(config)

        config = self.createNewSection(config, "EXTENSIONS", self.default_extensions)        
        config = self.createNewSection(config, "GROUP_PATHS", self.default_group_paths)        
        config = self.createNewSection(config, "RENAME_GROUP", self.default_rename_group)        
        config = self.createNewSection(config, "KEYWORDS", self.default_keywords)        
        config = self.createNewSection(config, "REGEX_RENAME", self.default_regex_rename)        
        config = self.createNewSection(config, "SETTINGS", self.default_settings)        
        
        if 'default_path' not in config['DEFAULT']:
            config['DEFAULT']['default_path'] = self.env.DOWNLOAD_COMPLETED_PATH
            with open(self.config_file, 'w') as configfile:
                config.write(configfile)

        return config

    def createNewSection(self, config, SECTION, VALUE):
        if not config.has_section(SECTION):
            config.add_section(SECTION)
            config[SECTION] = VALUE
            with open(self.config_file, "w") as config_file:
                config.write(config_file)
        return config

    def get_chars_to_replace(self):
        return self.config['SETTINGS'].get('chars_to_replace', '')

    def get_new_download_path(self, message, origin_group='', file_name=''):
        origin_group = self.info_handler.get_originGroup(message)
        file_name = self.info_handler.getFileName(message)
        file_size = self.info_handler.getFileSize(message)

        #print(f"get_download_path origin_group: {origin_group}, file_name: {file_name}")
        self.config.read(self.config_file)
        extension = file_name.split('.')[-1]
        caption = message.caption if message.caption else None
        
        if extension == 'torrent': return self.env.DOWNLOAD_PATH_TORRENTS

        download_path = (
            self.get_keyword_path(caption) or
            self.get_group_path(origin_group) or
            self.get_extension_path(extension)
        )

        filename = self.get_file_rename(message,origin_group,file_name)
        filename = self.get_file_rename_regex(message,origin_group,filename)

        return {
            'origin_group' : origin_group,
            'download_path' : download_path,
            'file_name' : file_name,
            'filename' : filename,
            'fullfilename' : os.path.join(download_path, filename),
            'file_size' : file_size,
        }

    def get_download_path(self, message, origin_group='', file_name=''):
        origin_group = self.info_handler.get_originGroup(message)
        file_name = self.info_handler.getFileName(message)

        #print(f"get_download_path origin_group: {origin_group}, file_name: {file_name}")
        self.config.read(self.config_file)
        extension = file_name.split('.')[-1]
        caption = message.caption if message.caption else None
        
        if extension == 'torrent': return self.env.DOWNLOAD_PATH_TORRENTS
        return (
            self.get_keyword_path(caption) or
            self.get_group_path(origin_group) or
            self.get_extension_path(extension)
        )

    def get_file_rename(self, message, group_id='', file_name=''):
        self.config.read(self.config_file)
        if not self.config['RENAME_GROUP'].get(str(group_id), None):
            return file_name

        if not message.caption:
            return file_name

        ext = file_name.split('.')[-1]
        caption = message.caption
        return f"{caption}.{ext}"

    def get_file_rename_regex(self, message, group_id='', file_name=''):
        self.config.read(self.config_file)
        if not self.config['RENAME_GROUP'].get(str(group_id), None):
            return file_name

        if not message.caption:
            return file_name

        ext = file_name.split('.')[-1]
        caption = message.caption
        return file_name


    def get_keyword_path(self, text):
        if not text: return None
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
        self.config.read(self.config_file)
        self.config['KEYWORDS'][keyword] = path
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def del_keyword_path(self, keyword):
        self.config.read(self.config_file)
        if keyword in self.config['KEYWORDS']:
            del self.config['KEYWORDS'][keyword]
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def add_rename_group(self, group_id):
        self.config.read(self.config_file)
        self.config['RENAME_GROUP'][group_id] = 'yes'
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def del_rename_group(self, group_id):
        self.config.read(self.config_file)
        if group_id in self.config['RENAME_GROUP']:
            del self.config['RENAME_GROUP'][group_id]
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)


