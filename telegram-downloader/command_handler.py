import os
import textwrap
import shutil

from pyrogram import Client, filters, __version__ as pyrogram_version
from pyrogram.types import Message
from pyrogram import enums

from data_handler import FileDataHandler
from downloadPathManager import DownloadPathManager
from utils import Utils
from env import Env
from logger_config import logger
from info_handler import InfoMessages
from command_controller import CommandController
from command_help import CommandHelp

class CommandHandler:
    def __init__(self, config):
        self.downloadPathManager = DownloadPathManager()
        self.env = Env()
        self.utils = Utils()
        self.data_handler = FileDataHandler()
        self.info_handler = InfoMessages()
        self.command_controller = CommandController()

        self.command_dict = {
            "ehelp": self.ehandle_help,
            "help": self.handle_help,
            "version": self.handle_version,
            "pyrogram": self.handle_pyrogram_version,
            "ytdlp": self.handle_ytdlp_version,
            "id": self.handle_id,
            "rename": self.rename_file,
            "move": self.rename_file,
            "addpathextension": self.setPathExtension,
            "delpathextension": self.delPathExtension,
            "addgroup": self.add_group_path,
            "addkeyword": self.add_keyword_path,
            "delkeyword": self.del_keyword_path,
            "addrenamegroup": self.add_rename_group,
            "delrenamegroup": self.del_rename_group,
            "test": self.test,
        }
        self.command_keys = list(self.command_dict.keys())
        self.bot_version = config.BOT_VERSION
        self.yt_dlp_version = config.YT_DLP_VERSION
        self.pyrogram_version = pyrogram_version


    async def process_command(self, client: Client, message: Message):
        try:

            command = message.command[0]

            user_id = message.from_user.id if message.from_user else None
            if not str(user_id) in self.env.AUTHORIZED_USER_ID and not command == 'id':
                return False

            logger.info(f"process_command:: {command}")
            handler_method = self.command_dict.get(command)

            if self._function_accepts_args(handler_method):
                return await handler_method(client, message)
            else:
                return await handler_method()

        except Exception as e:
            logger.error(f"process_command => Exception: {e}")

    def _function_accepts_args(self, func):
        # Verificar si la función acepta argumentos adicionales
        return hasattr(func, "__code__") and func.__code__.co_argcount > 1

    def is_reply(self, message):
        return message.reply_to_message is not None

    async def test(self, client: Client, message: Message):

        origin_group = self.info_handler.get_originGroup_test(message)
        logger.info(f"test origin_group : {origin_group}")

    async def ehandle_help(self, client: Client, message: Message):

        help_text = CommandHelp.get_ehelp()
        
        while help_text:
            # Toma un fragmento de texto de hasta 4096 caracteres.
            chunk = help_text[:4096]
            if len(help_text) > 4096:
                # Encuentra el último espacio para no cortar palabras.
                split_index = chunk.rfind(" ")
                if split_index == -1:  # Si no hay espacios, corta en el límite.
                    split_index = 4096
                chunk = help_text[:split_index]
                help_text = help_text[split_index:].strip()
            else:
                help_text = ""  # Última parte.

            # Envía el fragmento.
            await client.send_message(message.chat.id, chunk)
        
        #await message.reply_text(help_text, parse_mode=enums.ParseMode.DISABLED)

    async def handle_help(self, client: Client, message: Message):


        help_text = CommandHelp.get_help()

        await message.reply_text(help_text, parse_mode=enums.ParseMode.DISABLED)

    async def handle_id(self, client: Client, message: Message):
        user_id = message.from_user.id if message.from_user else None
        await message.reply_text(f"id: {str(user_id)}")

    async def handle_version(self, client: Client, message: Message):
        await message.reply_text(f"version: {str(self.bot_version)}")

    async def handle_pyrogram_version(self, client: Client, message: Message):
        await message.reply_text(f"pyrogram version: {self.pyrogram_version}")

    async def handle_ytdlp_version(self, client: Client, message: Message):
        await message.reply_text(f"ytdlp version: {self.yt_dlp_version}")

    async def rename_file(self, client: Client, message: Message):
        await self.command_controller.renameFiles(client, message)

    async def setPathExtension(self, client: Client, message: Message):
        await self.command_controller.setPathExtension(client, message)

    async def delPathExtension(self, client: Client, message: Message):
        await self.command_controller.delPathExtension(client, message)



    ########## ------------------------------------------------------------------------------------

     


    async def add_group_path(self, client: Client, message: Message):
        try:

            group_id = self.info_handler.get_originGroup_test(message)

            logger.info(f"add_group_path group_id: {group_id}")
            if not group_id and len(message.command) < 2:
                await message.reply_text("Usage: /addgroup <group_id> <download-path>", parse_mode=enums.ParseMode.DISABLED)
                return

            if message.reply_to_message and group_id:
                logger.info(f"add_group_path group_id : {group_id}")

                if len(message.command) > 1 :
                    path = ' '.join(message.command[1:])
                    new_path = path if path.startswith('/') else os.path.join(self.env.DOWNLOAD_PATH, path)
                    self.downloadPathManager.setPathGroup(group_id, new_path)
                    await message.reply_text(f"Path for group {group_id} added: {new_path}.")
                    logger.info(f" [!] add_group_path group_id : {group_id} added: {new_path}")
                else:
                    new_path = os.path.join(self.env.DOWNLOAD_PATH, str(group_id).replace('-',''))
                    self.downloadPathManager.setPathGroup(group_id, new_path)
                    await message.reply_text(f"Path for group {group_id} added: {new_path}.")

            else:
                if len(message.command) == 2 :
                    group_id = message.command[1] 
                    new_path = os.path.join(self.env.DOWNLOAD_PATH, message.command[1] )
                    self.downloadPathManager.setPathGroup(group_id, new_path)
                    await message.reply_text(f"Path for group {group_id} added: {new_path}.")
                elif len(message.command) == 3 :
                    group_id = message.command[1] 
                    path = message.command[2] 
                    new_path = path if path.startswith('/') else os.path.join(self.env.DOWNLOAD_PATH, path)
                    self.downloadPathManager.setPathGroup(group_id, new_path)
                    await message.reply_text(f"Path for group {group_id} added: {new_path}.")
        except Exception as e:
            logger.error(f"add_group_path Exception: {e}")


    async def add_keyword_path(self, client: Client, message: Message):
        if len(message.command) < 3:
            await message.reply_text("Usage: /addkeyword <keyword> <path>", parse_mode=enums.ParseMode.DISABLED)
            return

        path = message.command[-1]
        keywords = message.command[1:-1]

        logger.info(f"add_keyword keywords: {' '.join(keywords)}, path: {path}")

        self.downloadPathManager.setPathKeywords(' '.join(keywords).lower(), path)
        await message.reply_text(f"Path for keyword '{' '.join(keywords)}' added: {path}.")

    async def del_keyword_path(self, client: Client, message: Message):
        if len(message.command) < 2:
            await message.reply_text("Usage: /delkeyword <keyword>", parse_mode=enums.ParseMode.DISABLED)
            return

        keywords = message.command[1:]

        logger.info(f"delkeyword keywords: {' '.join(keywords)}")

        self.downloadPathManager.delPathKeywords(' '.join(keywords).lower())
        await message.reply_text(f"Path for keyword '{' '.join(keywords)}' remove")

    async def add_rename_group(self, client: Client, message: Message):        
        try:
            group_id = self.info_handler.get_originGroup_test(message)

            logger.info(f"add_rename_group group_id: {group_id}")
            if not group_id and len(message.command) < 2:
                await message.reply_text("Usage: /addrenamegroup <group_id>", parse_mode=enums.ParseMode.DISABLED)
                return


            if message.reply_to_message and group_id:
                logger.info(f"add_rename_group group_id : {group_id}")
                self.downloadPathManager.setRenameGroup(str(group_id))
                await message.reply_text(f"Group ID {group_id} added to rename group list.")
                return



            elif not group_id and len(message.command) > 1:
                group_id = message.command[1]

                self.downloadPathManager.setRenameGroup(str(group_id))
                await message.reply_text(f"Group ID {group_id} added to rename group list.")
                return
            else:
                await message.reply_text("Usage: /addrenamegroup <group_id>", parse_mode=enums.ParseMode.DISABLED)
                return

        except Exception as e:
            logger.error(f"add_rename_group Exception: {e}")

    async def del_rename_group(self, client: Client, message: Message):
        try:


            group_id = self.info_handler.get_originGroup_test(message)

            logger.info(f"delrenamegroup group_id: {group_id}")
            if not group_id and len(message.command) < 2:
                await message.reply_text("Usage: /delrenamegroup <group_id>", parse_mode=enums.ParseMode.DISABLED)
                return


            if message.reply_to_message and group_id:
                logger.info(f"delrenamegroup group_id : {group_id}")
                self.downloadPathManager.setRenameGroup(str(group_id))
                await message.reply_text(f"Group ID {group_id} removed to rename group list.")
                return


            elif not group_id and len(message.command) > 1:
                group_id = message.command[1]

                self.downloadPathManager.setRenameGroup(str(group_id))
                await message.reply_text(f"Group ID {group_id} removed to rename group list.")
                return
            else:
                await message.reply_text("Usage: /delrenamegroup <group_id>", parse_mode=enums.ParseMode.DISABLED)
                return

        except Exception as e:
            logger.error(f"del_rename_group Exception: {e}")





