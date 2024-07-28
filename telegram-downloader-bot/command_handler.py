from pyrogram import Client, filters
from pyrogram.types import Message
from file_data_handler import FileDataHandler
from config_handler import ConfigHandler
from utils import Utils
import os

class CommandHandler:
    def __init__(self):
        self.config_handler = ConfigHandler()
        self.file_data_handler = FileDataHandler()

    async def handle_commands(self, client: Client, message: Message):
        command = message.command[0]
        if command == "rename":
            await self.rename_file(client, message)
        elif command == "addpath":
            await self.add_path(client, message)
        elif command == "addgroup":
            await self.add_group(client, message)
        elif command == "addkeyword":
            await self.add_keyword(client, message)

    async def rename_file(self, client: Client, message: Message):
        if message.reply_to_message and message.reply_to_message.document:
            new_name = message.text.split(" ", 1)[1]
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
    
    async def add_keyword(self, client: Client, message: Message):
        if len(message.text.split()) >= 3:
            keyword = message.text.split()[1]
            path = message.text.split(" ", 2)[2]
            self.config_handler.add_keyword_path(keyword, path)
            await message.reply_text(f"Path for keyword '{keyword}' added: {path}.")
        else:
            await message.reply_text("Usage: /addkeyword <keyword> <path>")
