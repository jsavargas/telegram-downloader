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

        help_text = textwrap.dedent('''
            Welcome to the bot!

            Available commands:

            /id - Displays the user/group ID.
                - Usage: Simply type /id and the bot will respond with the ID of the current chat, whether it is a user or a group.
            

            /addpathextension <extension> <NewDirectory> - Crea una regla de ruta de descargad e archivo segun extension
                - Uso: Responde a un mensaje que contenga un archivo con /addpathextension seguido del nuevo nombre que deseas para la carpeta. Si no agregas una ruta
                - Ejemplo: Si recibes un documento y quieres crear una regla para que esos archivos vayan a una carpeta "MiCarpeta", responde al mensaje con /addpathextension MiCarpeta, luego puedes escribir /move para mover el archivo a la nueva ruta creada con /addpathextension
                    - /addpathextension 
                    - /addpathextension <REPLY> /NuevoDirectorio
                    - /addpathextension <extension> /NuevoDirectorio


            /rename <new_name> - Rename the replied message file.
                - Usage: Reply to a message containing a file with /rename followed by the new name you want for the file.
                - Example: If you receive a document and want to rename it to "MyDocument", reply to the message with /rename MyDocument.
                    - /rename 
                    - /rename /NewDirectory
                    - /rename newFileName
                    - /rename NewFileName.ext
                    - /rename Directory/NewFileName.ext
                - Note: The new name must not contain special characters that are not allowed in file names. You can also use /rename alone and it will rename according to the config.ini file rules


            /move <new_folder> - Mueve el archivo del mensaje respondido.
                - Uso: Responde a un mensaje que contenga un archivo con /move seguido del nuevo nombre que deseas para la carpeta. Si no agregas una ruta, se movera a la carpeta segun las para el archivo o grupo en el archivo config.ini
                - Ejemplo: Si recibes un documento y quieres moverlo a "MiDocumento", responde al mensaje con /move MiDocumento.
                    - /move 
                    - /move /NuevoDirectorio

            /addgroup <group_id> <new_folder> - Crea una nueva regla para descargar los archivos de este grupo en una carpeta especifica.
                - Uso: Responde a un mensaje que contenga un archivo con /addgroup seguido del nuevo nombre que deseas para la carpeta.
                - Ejemplo: Si recibes un documento y quieres crear una regla para que esos archivos vayan a una carpeta "MiCarpeta", responde al mensaje con /addgroup MiCarpeta, luego puedes escribir /move para mover el archivo a la nueva ruta creada con /addgroup
                    - /addgroup 
                    - /addgroup <REPLY> /NuevoDirectorio
                    - /addgroup <group_id> /NuevoDirectorio

            /delgroup DEVELOP <new_folder> - Crea una nueva regla para descargar los archivos de este grupo en una carpeta especifica.
                - Uso: Responde a un mensaje que contenga un archivo con /addgroup seguido del nuevo nombre que deseas para la carpeta.
                - Ejemplo: Si recibes un documento y quieres crear una regla para que esos archivos vayan a una carpeta "MiCarpeta", responde al mensaje con /addgroup MiCarpeta, luego puedes escribir /move para mover el archivo a la nueva ruta creada con /addgroup
                    - /addgroup 
                    - /addgroup /NuevoDirectorio


            /addrenamegroup <group_id> - Crea una regla para renombrar archivos en base al texto del mensaje en el archivo a descargar.
                - Uso: Responde a un mensaje que contenga un archivo con /addrenamegroup para que sea agregada una nueva regla en el archivo config.ini.
                - Ejemplo: Si recibes un documento y quieres que su nombre sea el contenido del mensaje, responde al mensaje con /addrenamegroup. Puede usarse despues /rename para renomrar el archivo descargado segun las regla anteriormente creada.
                    /addrenamegroup
                    /addrenamegroup <group Id>

            /delrenamegroup <group_id> - Crea una regla para renombrar archivos en base al texto del mensaje en el archivo a descargar.
                - Uso: Responde a un mensaje que contenga un archivo con /delrenamegroup para que sea agregada una nueva regla en el archivo config.ini.
                - Ejemplo: Si recibes un documento y quieres que su nombre sea el contenido del mensaje, responde al mensaje con /delrenamegroup. Puede usarse despues /rename para renomrar el archivo descargado segun las regla anteriormente creada.
                    /delrenamegroup
                    /delrenamegroup <group Id>

            Pronto se agregarán más comandos. ¡Mantente atento!

            Los comandos pueden usarse tanto en chats privados como en chats grupales.
            Asegúrate de que el bot tenga los permisos necesarios para acceder a mensajes y archivos en los chats grupales.
        
        
        
        ''')
        
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


        help_text = (
            "Welcome to the bot!\n\n"
            "Available commands:\n"
            "/id - Shows the user/group ID\n"
            "/rename <new_name> - Rename the file from the replied message.\n"
            "/addpath <extension> <path> - Add a download path for a specific file extension.\n"
            "/addgroup <path> - Add a download path for a specific group. Use by replying to a message in the group.\n"
            "/addkeyword <keyword1> <keyword2> ... <path> - Add download paths for messages containing specific keywords or phrases.\n"
            "/delkeyword <keyword1> <keyword2> ... <path> - Remove download paths for messages containing specific keywords or phrases.\n"
            "/addrenamegroup <group_id> - Adds a group ID to the rename group list\n"
            "/delrenamegroup <group_id> - Remove a group ID to the rename group list\n"
            "/pyrogram - Displays the Telethon version\n"
            "/ytdlp - Displays the ytdlp version\n"
            "/version - Displays the bot version"

        )
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

    async def setPathExtension(self, client: Client, message: Message):
        await self.command_controller.setPathExtension(client, message)

    async def rename_file(self, client: Client, message: Message):
        await self.command_controller.renameFiles(client, message)


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





