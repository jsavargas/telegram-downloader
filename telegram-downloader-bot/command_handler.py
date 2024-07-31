import os

from pyrogram import Client, filters, __version__ as pyrogram_version
from pyrogram.types import Message
from pyrogram import enums

from file_data_handler import FileDataHandler
from config_handler import ConfigHandler
from utils import Utils
from env import Env

class CommandHandler:
    def __init__(self, config):
        self.config_handler = ConfigHandler()
        self.env = Env()
        self.file_data_handler = FileDataHandler()

        self.command_dict = {
            "help": self.handle_help,
            "version": self.handle_version,
            "pyrogram": self.handle_pyrogram_version,
            "ytdlp": self.handle_ytdlp_version,
            "id": self.handle_id,
            "rename": self.rename_file,
            "addpath": self.add_path,
            "addgroup": self.add_group,
            "addkeyword": self.add_keyword_path,
            "delkeyword": self.del_keyword_path,
            "addrenamegroup": self.add_rename_group,
            "delrenamegroup": self.del_rename_group,
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

            print(f"process_command:: {command}")
            handler_method = self.command_dict.get(command)

            if self._function_accepts_args(handler_method):
                return await handler_method(client, message)
            else:
                return await handler_method()

        except Exception as e:
            print(f"process_command => Exception: {e}")

    def _function_accepts_args(self, func):
        # Verificar si la función acepta argumentos adicionales
        return hasattr(func, "__code__") and func.__code__.co_argcount > 1


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
        command = message.command[0]

        if command == "rename" and message.reply_to_message:
            if len(message.command) < 2:
                await message.reply_text("Usage: /rename <new_name>")
                return

            new_name = message.command[1]
            reply_message = message.reply_to_message


            if message.reply_to_message.document:
                new_name = message.command[1]
                old_file_id = message.reply_to_message.document.file_id
                file_info = self.file_data_handler.get_file_data_by_file_id(old_file_id)
                
                if file_info:
                    old_file_path = file_info["file_path"]
                    new_file_path = os.path.join(os.path.dirname(old_file_path), new_name)
                    os.rename(old_file_path, new_file_path)
                    self.file_data_handler.update_file_name(file_id=old_file_id, new_name=new_name)
                    await message.reply_text(f"File renamed to {new_name}.")
                else:
                    await message.reply_text("File not found in the records.")
        else:
            await message.reply_text("Please reply to a document message with the new name.")

    async def add_path(self, client: Client, message: Message):
        if len(message.text.split()) == 3:
            ext, path = message.text.split()[1:]
            self.config_handler.add_path(ext, path)
            await message.reply_text(f"Path for .{ext} added: {path}.")
        else:
            await message.reply_text("Usage: /addpath <extension> <path>")

    async def add_group(self, client: Client, message: Message):
        if message.reply_to_message and message.reply_to_message.document:
            group_id = message.chat.id
            path = message.text.split(" ", 1)[1]
            self.config_handler.add_group_path(group_id, path)
            await message.reply_text(f"Path for group {group_id} added: {path}.")
        else:
            await message.reply_text("Please reply to a document message with the path.")
    
    async def add_keyword_path(self, client: Client, message: Message):
        if len(message.command) < 3:
            await message.reply_text("Usage: /addkeyword <keyword> <path>", parse_mode=enums.ParseMode.DISABLED)
            return

        path = message.command[-1]
        keywords = message.command[1:-1]

        print(f"add_keyword keywords: {' '.join(keywords)}, path: {path}")

        self.config_handler.add_keyword_path(' '.join(keywords).lower(), path)
        await message.reply_text(f"Path for keyword '{' '.join(keywords)}' added: {path}.")

    async def del_keyword_path(self, client: Client, message: Message):
        if len(message.command) < 2:
            await message.reply_text("Usage: /delkeyword <keyword>", parse_mode=enums.ParseMode.DISABLED)
            return

        keywords = message.command[1:]

        print(f"delkeyword keywords: {' '.join(keywords)}")

        self.config_handler.del_keyword_path(' '.join(keywords).lower())
        await message.reply_text(f"Path for keyword '{' '.join(keywords)}' remove")

    async def add_rename_group(self, client: Client, message: Message):        
        try:
            group_id = message.reply_to_message.forward_from_chat.id if message.reply_to_message and message.reply_to_message.forward_from_chat else None
            print(f"add_rename_group group_id: {group_id}")
            if not group_id and len(message.command) < 2:
                await message.reply_text("Usage: /addrenamegroup <group_id>", parse_mode=enums.ParseMode.DISABLED)
                return

            if not group_id and not len(message.command) < 2:
                group_id = message.command[1]

            self.config_handler.add_rename_group(str(group_id))
            await message.reply_text(f"Group ID {group_id} added to rename group list.")
        except Exception as e:
            print(f"add_rename_group Exception: {e}")

    async def del_rename_group(self, client: Client, message: Message):
        try:
            group_id = message.reply_to_message.forward_from_chat.id if message.reply_to_message and message.reply_to_message.forward_from_chat else None
            if not group_id and len(message.command) < 2:
                await message.reply_text("Usage: /delrenamegroup <group_id>", parse_mode=enums.ParseMode.DISABLED)
                return
            if not group_id and not len(message.command) < 2:
                group_id = message.command[1]
                
            self.config_handler.del_rename_group(str(group_id))
            await message.reply_text(f"Group ID {group_id} removed to rename group list.")
        except Exception as e:
            print(f"del_rename_group Exception: {e}")
