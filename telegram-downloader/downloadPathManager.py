from config_handler import ConfigKeys, ConfigHandler
from env import Env
from info_handler import InfoMessages
from logger_config import logger

import os
import re

class DownloadPathManager:
    def __init__(self):
        self.config_handler = ConfigHandler()
        self.env = Env()
        self.info_handler = InfoMessages()

    def get_chars_to_replace(self):
        return self.config_handler.get_value(ConfigKeys.SETTINGS.value, "chars_to_replace")

    def getDefaultPath(self):
        return self.config_handler.get_value(ConfigKeys.DEFAULT.value, "default_path")
    
    def getBasePath(self, path):
        if not path.startswith('/'):
            return os.path.join(self.env.DOWNLOAD_PATH, path)
        return path

    def getDefaultPathExtension(self, extension):
        switch = {
            'torrent': self.env.DOWNLOAD_PATH_TORRENTS
        }
        return switch.get(extension, None)

    def getPathExtension(self, key):
        path = self.getDefaultPathExtension(key)
        return path if path else self.config_handler.get_value(ConfigKeys.EXTENSIONS.value, key) or self.getDefaultPath()

    def setPathExtension(self, key, value):
        value = value.replace(".", "")
        value = self.getBasePath(value)
        return self.config_handler.add_key(ConfigKeys.EXTENSIONS.value, key, value)

    def delPathExtension(self, key, value):
        return self.config_handler.delete_key(ConfigKeys.EXTENSIONS.value, key)

    def getPathGroup(self, key):
        return self.config_handler.get_value(ConfigKeys.GROUP_PATH.value, key)
    
    def setPathGroup(self, key, value):
        return self.config_handler.add_key(ConfigKeys.GROUP_PATH.value, key, value)

    def getPathKeywords(self, key):
        sections = self.config_handler.get_values(ConfigKeys.KEYWORDS.value, key)
        logger.info(f"[!] if getPathKeywords key : [{key}]")
        if not key: return None
        for section in sections:
            if section in key.lower():
                return sections[section]
                logger.info(f"[!] if getPathKeywords section : [{section}] => [{sections[section]}]")

        return None
        return self.config_handler.get_values(ConfigKeys.KEYWORDS.value, key)
    
    def setPathKeywords(self, key, value):
        return self.config_handler.add_key(ConfigKeys.KEYWORDS.value, key, value)

    def delPathKeywords(self, key):
        return self.config_handler.delete_key(ConfigKeys.KEYWORDS.value, key)

    def setRenameGroup(self, key):
        return self.config_handler.add_key(ConfigKeys.RENAME_GROUP.value, key, 'yes')

    def delRenameGroup(self, key):
        return self.config_handler.delete_key(ConfigKeys.RENAME_GROUP.value, key)

    def getFileRenameRegex(self, message, group_id, file_name):
        if not self.config_handler.get_value(ConfigKeys.RENAME_GROUP.value, group_id):
            return file_name
        if not message.caption:
            return file_name
        ext = file_name.split('.')[-1]
        caption = message.caption
        return file_name

    def getFileRename(self, message, group_id, file_name):
        #logger.info(f"[!] get_file_rename message   : {message}")
        logger.info(f"[!] get_file_rename group_id   : {group_id}")
        logger.info(f"[!] get_file_rename file_name   : {file_name}")

        if not self.config_handler.get_value(ConfigKeys.RENAME_GROUP.value, group_id):
            return file_name

        if not message.caption:
            return file_name

        ext = file_name.split('.')[-1]
        caption = message.caption
        logger.info(f"[!] get_file_rename caption   : {caption}")
        return f"{caption}.{ext}"

    def getDownloadPathT(self, message, origin_group, file_name):
        origin_group = self.info_handler.get_originGroup_test(message)
        if not file_name:
            file_name = self.info_handler.getFileName(message)

        extension = file_name.split('.')[-1]
        textName = message.caption if message.caption else file_name
        
        if extension == 'torrent': return self.env.DOWNLOAD_PATH_TORRENTS

        returnPathDownload = (
            self.getPathKeywords(textName) or
            self.getPathGroup(origin_group) or
            self.getPathExtension(extension)
        )

        print(f"[!] returnPathDownload:: [{returnPathDownload}]")
        return returnPathDownload


    def getNewDownloadPath(self, message, origin_group='', file_name=''):
        origin_group = self.info_handler.get_originGroup_test(message)
        file_name = self.info_handler.getFileName(message)
        file_size = self.info_handler.getFileSize(message)

        logger.info(f"[!] getNewDownloadPath origin_group   : {origin_group}")
        logger.info(f"[!] getNewDownloadPath file_name   : {file_name}")
        logger.info(f"[!] getNewDownloadPath file_size   : {file_size}")

        extension = file_name.split('.')[-1]
        caption = message.caption if message.caption else None
        
        if extension == 'torrent': return self.env.DOWNLOAD_PATH_TORRENTS

        download_path = (
            self.getPathKeywords(caption) or
            self.getPathGroup(origin_group) or
            self.getPathExtension(extension)
        )

        filename = self.getFileRename(message,origin_group,file_name)
        filename = self.getFileRenameRegex(message,origin_group,filename)

        return {
            'origin_group' : origin_group,
            'download_path' : download_path,
            'file_name' : file_name,
            'filename' : filename,
            'fullfilename' : os.path.join(download_path, filename),
            'file_size' : file_size,
        }

    def rename(self, message, origin_group, file_name):

        logger.info(f"[!] rename origin_group   : {origin_group}")
        logger.info(f"[!] rename file_name   : {file_name}")

        pattern = '[' + re.escape(self.get_chars_to_replace()) + ']'
        file_name = re.sub(pattern, '', file_name)

        value = self.config_handler.get_value(ConfigKeys.REMOVE_PATTERNS.value, origin_group)
        logger.info(f"[!] rename value : {value}")
        if value:
            file_name = file_name.replace(value,"")
        else:
            pattern = self.config_handler.get_values(ConfigKeys.REMOVE_PATTERNS.value, origin_group)
            for value in pattern:
                if value.startswith("pattern"):
                    logger.info(f"[!] rename pattern : {value} => {pattern[value]}")
                    file_name = file_name.replace(pattern[value],"")

        return file_name

    #  downloadPathManager.setRenameGroup
    #   config_handler


if __name__ == "__main__":
    download_path_manager = DownloadPathManager()

    #print(f"set path_extension:: {download_path_manager.setPathExtension("mp4", "/download/mp4")}")
    #print(f"set path_extension:: {download_path_manager.setPathExtension("mp3", "/download/music")}")
    #
    #print(f"get path_extension:: {download_path_manager.getPathExtension("torrent")}")
    #print(f"get path_extension:: {download_path_manager.getPathExtension("jpg")}")
    #print(f"get path_extension:: {download_path_manager.getPathExtension("mp3")}")
    #
    #
    #print(f"get getPathGroup:: {download_path_manager.getPathGroup(-1001186275022)}")
    #print(f"get setPathGroup:: {download_path_manager.setPathGroup(-1001186275022, "/download/1001186275022")}")
    #

    #print(f"get getPathKeywords:: {download_path_manager.getPathKeywords('Hugh')}")
    print(f"get getPathKeywords:: {download_path_manager.getPathKeywords('The Changeling.flac')}")
    #print(f"get getPathKeywords:: {download_path_manager.getPathKeywords("Espejismo - Hugh Howey.epub")}")
    #print(f"get getPathKeywords:: {download_path_manager.getPathKeywords("Espejismo - Hugh Howey")}")
    #print(f"get setPathKeywords:: {download_path_manager.setPathKeywords("tanganana", "/download/tanganana")}")
    #print(f"get delPathKeywords:: {download_path_manager.delPathKeywords("tangananaaaa")}")


    #result = download_path_manager.rename("Hugh", "-100123456", "Espejismo -| Hugh Howey.epub")
    #print(f"get rename:: {result}")


    #result = download_path_manager.rename("Hugh", "-100123456", "Espejismo -[tif_ Hugh Howey.epub")
    #print(f"get rename:: {result}")


