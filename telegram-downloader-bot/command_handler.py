import os
import textwrap
import shutil

from pyrogram import Client, filters, __version__ as pyrogram_version
from pyrogram.types import Message
from pyrogram import enums

from data_handler import FileDataHandler
from config_handler import ConfigHandler
from utils import Utils
from env import Env
from logger_config import logger
from info_handler import InfoMessages

class CommandHandler:
    def __init__(self, config):
        self.config_handler = ConfigHandler()
        self.env = Env()
        self.utils = Utils()
        self.data_handler = FileDataHandler()
        self.info_handler = InfoMessages()

        self.command_dict = {
            "ehelp": self.ehandle_help,
            "help": self.handle_help,
            "version": self.handle_version,
            "pyrogram": self.handle_pyrogram_version,
            "ytdlp": self.handle_ytdlp_version,
            "id": self.handle_id,
            "rename": self.rename_file,
            "move": self.rename_file,
            "addpath": self.add_path,
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


    async def test(self, client: Client, message: Message):

        origin_group = self.info_handler.get_originGroup_test(message)
        logger.info(f"test origin_group : {origin_group}")


    async def ehandle_help(self, client: Client, message: Message):

        help_text = textwrap.dedent('''
            Welcome to the bot!

            Available commands:

            /id - Muestra el ID del usuario/grupo.
                - Uso: Simplemente escribe /id y el bot responderá con el ID del chat actual, ya sea un usuario o un grupo.

            /rename <new_name> - Renombrar el archivo del mensaje respondido.
                - Uso: Responde a un mensaje que contenga un archivo con /rename seguido del nuevo nombre que deseas para el archivo.
                - Ejemplo: Si recibes un documento y quieres renombrarlo a "MiDocumento", responde al mensaje con /rename MiDocumento.
                    - /rename 
                    - /rename /NuevoDirectorio
                    - /rename NuevoNombreDeArchivo
                    - /rename NuevoNombreDeArchivo.ext
                    - /rename Directorio/NuevoNombreDeArchivo.ext
                - Nota: El nuevo nombre no debe contener caracteres especiales que no estén permitidos en los nombres de archivos. Tambien puedes utilizar /rename solo y renombrara segun las reglas de archivo del config.ini


            /move <new_folder> - Mueve el archivo del mensaje respondido.
                - Uso: Responde a un mensaje que contenga un archivo con /move seguido del nuevo nombre que deseas para la carpeta.
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

        await message.reply_text(help_text, parse_mode=enums.ParseMode.DISABLED)

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


    async def rename_file(self, client: Client, message: Message):
        try:
            command = message.command[0]
            if not message.reply_to_message:
                await message.reply_text("Please reply to a document message with the new name.")
                return
            if message.reply_to_message:
                file_info = self.data_handler.get_download_file(message.reply_to_message_id)
                logger.info(f"rename_file file_name      : {file_info}")
                if file_info and len(message.command) > 1:
                    new_name = message.command[1]
                    new_filename = self.utils.combine_paths(file_info, new_name)
                    logger.info(f"rename_file update_download_files : {new_name} => {new_filename}")
                    if new_name: 
                        logger.info(f"rename_file if new_name : {new_name} => {new_filename}")
                        try:
                            new_dir = os.path.dirname(new_filename)
                            if not os.path.exists(new_dir):
                                os.makedirs(new_dir)
                            dest = shutil.move(file_info, new_filename)  
                        except Exception as e:
                            logger.info(f'Error renaming file: {e}')
                            await message.reply_text(f"Error renaming file.\n{e}")
                            return
                        logger.info(f"rename_file os.rename : [{file_info}], [{new_filename}] => [{dest}]")
                        update_download_files = self.data_handler.update_download_files(message.reply_to_message_id, new_filename)
                        logger.info(f"rename_file os.rename update_download_files: [{update_download_files}]")
                        if update_download_files:
                            await message.reply_text(f"File renamed to {dest}")
                        return 
            
                dataMessage = self.info_handler.getDataMessage(message.reply_to_message)
                logger.info(f"rename_file dataMessage: {dataMessage}")
                if dataMessage:
                    downloadFile = self.config_handler.get_new_download_path(message.reply_to_message)

                    if file_info == downloadFile['fullfilename']:
                        await message.reply_text(f"File renamed to {file_info}.")
                        return
                        
                    logger.info(f"rename_file downloadFile: {downloadFile}")
                    logger.info(f"rename_file reply_to_message_id: {message.reply_to_message_id}")
                    logger.info(f"rename_file origin_group   : {downloadFile['origin_group']}")
                    logger.info(f"rename_file download_path  : {downloadFile['download_path']}")
                    logger.info(f"rename_file file_name      : {downloadFile['file_name']}")
                    logger.info(f"rename_file filename       : {downloadFile['filename']}")
                    logger.info(f"rename_file fullfilename   : {downloadFile['fullfilename']}")
                    logger.info(f"rename_file file_size      : {downloadFile['file_size']}")

                    if file_info != downloadFile['fullfilename']:
                        new_name = os.rename(file_info, downloadFile['fullfilename'])
                        update_download_files = self.data_handler.update_download_files(message.reply_to_message_id, downloadFile['fullfilename'])
                    
                        logger.info(f"rename_file update_download_files      ::: {update_download_files}")
                    
                        if update_download_files: await message.reply_text(f"File renamed to {downloadFile['fullfilename']}.")
                        
        except Exception as e:
            print(f"rename_file => Exception: {e}")
            await message.reply_text(f"File renamed Exception: {e}.")
     

    async def add_path(self, client: Client, message: Message):
        if len(message.text.split()) == 3:
            ext, path = message.text.split()[1:]
            self.config_handler.add_path(ext, path)
            await message.reply_text(f"Path for .{ext} added: {path}.")
        else:
            await message.reply_text("Usage: /addpath <extension> <path>")

    async def add_group_path(self, client: Client, message: Message):
        try:

            group_id = self.info_handler.get_originGroup_test(message)

            logger.info(f"add_group_path group_id: {group_id}")
            if not group_id and len(message.command) < 2:
                await message.reply_text("Usage: /addgroup <group_id> <download-path>", parse_mode=enums.ParseMode.DISABLED)
                return

            if message.reply_to_message and group_id:
                logger.info(f"add_rename_group group_id : {group_id}")

                if len(message.command) > 1 :
                    path = message.command[1] 
                    new_path = path if path.startswith('/') else os.path.join(self.env.DOWNLOAD_PATH, path)
                    self.config_handler.add_group_path(group_id, new_path)
                    await message.reply_text(f"Path for group {group_id} added: {new_path}.")
                else:
                    new_path = os.path.join(self.env.DOWNLOAD_PATH, str(group_id).replace('-',''))
                    self.config_handler.add_group_path(group_id, new_path)
                    await message.reply_text(f"Path for group {group_id} added: {new_path}.")

            else:
                if len(message.command) == 2 :
                    group_id = message.command[1] 
                    new_path = os.path.join(self.env.DOWNLOAD_PATH, message.command[1] )
                    self.config_handler.add_group_path(group_id, new_path)
                    await message.reply_text(f"Path for group {group_id} added: {new_path}.")
                elif len(message.command) == 3 :
                    group_id = message.command[1] 
                    path = message.command[2] 
                    new_path = path if path.startswith('/') else os.path.join(self.env.DOWNLOAD_PATH, path)
                    self.config_handler.add_group_path(group_id, new_path)
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

        self.config_handler.add_keyword_path(' '.join(keywords).lower(), path)
        await message.reply_text(f"Path for keyword '{' '.join(keywords)}' added: {path}.")

    async def del_keyword_path(self, client: Client, message: Message):
        if len(message.command) < 2:
            await message.reply_text("Usage: /delkeyword <keyword>", parse_mode=enums.ParseMode.DISABLED)
            return

        keywords = message.command[1:]

        logger.info(f"delkeyword keywords: {' '.join(keywords)}")

        self.config_handler.del_keyword_path(' '.join(keywords).lower())
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
                self.config_handler.add_rename_group(str(group_id))
                await message.reply_text(f"Group ID {group_id} added to rename group list.")
                return



            elif not group_id and len(message.command) > 1:
                group_id = message.command[1]

                self.config_handler.add_rename_group(str(group_id))
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
                self.config_handler.add_rename_group(str(group_id))
                await message.reply_text(f"Group ID {group_id} removed to rename group list.")
                return


            elif not group_id and len(message.command) > 1:
                group_id = message.command[1]

                self.config_handler.add_rename_group(str(group_id))
                await message.reply_text(f"Group ID {group_id} removed to rename group list.")
                return
            else:
                await message.reply_text("Usage: /delrenamegroup <group_id>", parse_mode=enums.ParseMode.DISABLED)
                return

        except Exception as e:
            logger.error(f"del_rename_group Exception: {e}")


