from data_handler import FileDataHandler
from downloadPathManager import DownloadPathManager
from utils import Utils
from env import Env
from logger_config import logger
from info_handler import InfoMessages

import os
import shutil

class CommandController:
    def __init__(self):
        self.downloadPathManager = DownloadPathManager()
        self.env = Env()
        self.utils = Utils()
        self.data_handler = FileDataHandler()
        self.info_handler = InfoMessages()

    def is_reply(self, message):
        return message.reply_to_message is not None

    async def setPathExtension(self, client, message):

        try:
            if self.is_reply(message):
                ext = self.info_handler.getFileExtension(message.reply_to_message)

                if ext and len(message.command) > 1:
                    path = message.command[-1]
                    path = self.downloadPathManager.setPathExtension(ext, path)
                    logger.info(f"setPathExtension path: {path}")
                    await message.reply_text(f"Path for .{ext} added: {path}.")
                if ext and len(message.command) == 1:
                    path = self.downloadPathManager.setPathExtension(ext, ext)
                    logger.info(f"setPathExtension path: {path}")
                    await message.reply_text(f"Path for .{ext} added: {path}.")
            else:
                if len(message.text.split()) == 3:
                    ext, path = message.text.split()[1:]
                    self.downloadPathManager.setPathExtension(ext, path)
                    await message.reply_text(f"Path for .{ext} added: {path}.")
                else:
                    await message.reply_text("Usage: /addpathextension <extension> <path>")

        except Exception as e:
            logger.error(f"setPathExtension => Exception: {e}")

    
    
    async def renameFiles(self, client, message):
        try:
            command = message.command[0]

            if self.is_reply(message):
                file_info = self.data_handler.get_download_file(message.reply_to_message_id)
                logger.info(f"rename_file file_name      : {file_info}")

                if file_info and len(message.command) > 1:
                    new_name = message.command[1]
                    new_filename = self.utils.combine_paths(file_info, new_name)
                    logger.info(f"rename_file update_download_files : {new_name} => {new_filename}")
                    logger.info(f"rename_file if new_name : {new_name} => {new_filename}")

                    new_dir = os.path.dirname(new_filename)
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)
                    dest = shutil.move(file_info, new_filename)  

                    logger.info(f"rename_file os.rename : [{file_info}], [{new_filename}] => [{dest}]")
                    update_download_files = self.data_handler.update_download_files(message.reply_to_message_id, new_filename)
                    logger.info(f"rename_file os.rename update_download_files: [{update_download_files}]")
                    if update_download_files:
                        await message.reply_text(f"File renamed to {dest}")
                    return True

                else:
                    downloadFile = self.downloadPathManager.getNewDownloadPath(message.reply_to_message)
                    logger.info(f"[!] rename_file downloadFile   : {downloadFile}")
                    logger.info(f"[!] rename_file origin_group   : {downloadFile['origin_group']}")
                    logger.info(f"[!] rename_file download_path  : {downloadFile['download_path']}")
                    logger.info(f"[!] rename_file file_name      : {downloadFile['file_name']}")
                    logger.info(f"[!] rename_file filename       : {downloadFile['filename']}")
                    logger.info(f"[!] rename_file fullfilename   : {downloadFile['fullfilename']}")
                    logger.info(f"[!] rename_file file_size      : {downloadFile['file_size']}")
                    logger.info(f"[!] rename_file file_info      : {file_info}")
          
                    if file_info == downloadFile['fullfilename']:
                        await message.reply_text(f"File renamed to {file_info}.")
                        return
                    else:

                        reply = await message.reply_text(f"moving to {downloadFile['fullfilename']}.")
                        new_name = self.utils.shutil_move(file_info, downloadFile['fullfilename'])
                        update_download_files = self.data_handler.update_download_files(message.reply_to_message_id, downloadFile['fullfilename'])
                        logger.info(f"rename_file update_download_files      ::: {update_download_files}")
            
                        if update_download_files: await reply.edit_text(f"File renamed to {downloadFile['fullfilename']}.")
                        else: await reply.edit_text(f"error moving file {downloadFile['fullfilename']}.")

        except Exception as e:
            logger.error(f"rename_file => Exception: {e}")
            await message.reply_text(f"File renamed Exception: {e}.")
