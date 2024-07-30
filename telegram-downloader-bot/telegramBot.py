# -*- coding: utf-8 -*-
print("\033c")

import os
import re
import time
from datetime import datetime
import logging
import uvloop
import asyncio
import yt_dlp

from pyrogram import Client, filters, __version__ as pyrogram_version
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait, RPCError


from env import Env
from utils import Utils 
from print_utils import PartialPrinter
from file_data_handler import FileDataHandler
from config_handler import ConfigHandler
from command_handler import CommandHandler
from url_downloader import URLDownloader  # Import the class
from pending_handler import PendingMessagesHandler

BOT_VERSION = "5.0.0-r30"

uvloop.install()


env = Env()
utils = Utils()
printer = PartialPrinter()
downloadFilesDB = FileDataHandler()
config_handler = ConfigHandler()
command_handler = CommandHandler()
url_downloader = URLDownloader()
pendingMessagesHandler = PendingMessagesHandler()

utils.removeFiles()

msg_txt = ""
#app = Client("telegramBot", api_id = int(env.API_ID), api_hash = env.API_HASH, bot_token = env.BOT_TOKEN, workers=env.MAX_CONCURRENT_TRANSMISSIONS, max_concurrent_transmissions=env.MAX_CONCURRENT_TRANSMISSIONS)
app = Client("telegramBot", api_id = int(env.API_ID), api_hash = env.API_HASH, bot_token = env.BOT_TOKEN, sleep_threshold=10, no_updates=True, takeout=True)
app = Client("telegramBot", api_id = int(env.API_ID), api_hash = env.API_HASH, bot_token = env.BOT_TOKEN)



# Semaphore to limit the number of simultaneous downloads
semaphore = asyncio.Semaphore(3)

# Regex to detect URLs in a message
URL_REGEX = re.compile(r'https?://\S+')


while True:
    try:
        with app:
            now = datetime.now()
            dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
            msg_txt = "Telegram Downloader Bot Started\n\n"
            msg_txt += f"bot version: {BOT_VERSION}\n"
            msg_txt += f"pyrogram version: {pyrogram_version}\n"
            msg_txt += f"yt_dlp version: {yt_dlp.version.__version__}\n"
            #msg_txt += f"yt-dlp version: 2024.05.27"
            
            print("Telegram Downloader Bot Started : ", dt_string)
            app.send_message(int(env.AUTHORIZED_USER_ID[0]), msg_txt)
            printer.print_variable("BOT_VERSION", BOT_VERSION)
            printer.print_variable("PYROGRAM_VERSION", pyrogram_version)
            printer.print_variable("YTDLP_VERSION", yt_dlp.version.__version__)
            printer.print_variables()
            break  # Salir del bucle si el mensaje se envía exitosamente
    except FloodWait as e:
        print(f"FloodWait: Esperando {e.value} segundos antes de reintentar iniciar...\n {e}")
        remaining_time = e.value
        while remaining_time > 0:
            print(f"Remaining time: {remaining_time} seconds", flush=True)
            time.sleep(60)
            remaining_time -= 60


def getFileName(message: Message) -> str:
    if message.document:
        print("message.document: ", message.document)
        return message.document.file_name
    elif message.photo:
        print("message.photo: ", message.photo)
        return f"{message.photo.file_unique_id}.jpg"
    elif message.video:
        print("message.video: ", message.video)
        return message.video.file_name if message.video.file_name else f"{message.video.file_unique_id}.{message.video.mime_type.split('/')[-1]}"
    elif message.animation:
        print("message.animation: ", message.animation)
        return message.animation.file_name if message.animation.file_name else f"{message.animation.file_unique_id}.{message.animation.mime_type.split('/')[-1]}"
    elif message.audio:
        print("message.audio: ", message.audio)
        return message.audio.file_name if message.audio.file_name else f"{message.audio.title}.{message.audio.mime_type[-3:]}"
        return message.audio.title
    else:
        print("message: ", message)
        return "Archivo"

def getFileSize(message: Message) -> str:
    if message.document:
        print("message.document: ", message.document)
        return message.document.file_size
    elif message.photo:
        print("message.photo: ", message.photo)
        return message.photo.file_size
    elif message.video:
        print("message.video: ", message.video)
        return message.video.file_size #if message.video.file_size else f"{message.video.file_unique_id}.{message.video.mime_type.split('/')[-1]}"
    elif message.animation:
        print("message.animation: ", message.animation)
        return message.animation.file_size #if message.animation.file_size else f"{message.animation.file_unique_id}.{message.animation.mime_type.split('/')[-1]}"
    elif message.audio:
        print("message.audio: ", message.audio)
        return message.audio.file_size #if message.audio.file_name else f"{message.audio.title}.{message.audio.mime_type[-3:]}"
    else:
        print("message: ", message)
        return 0


@app.on_message(filters.document | filters.photo | filters.video | filters.audio | filters.animation)
async def handle_files(client: Client, message: Message):
    pendingMessagesHandler.add_pending_message(message.id, message)
    
    attempt = 0
    file_path = ""

    async with semaphore:

            print("\ndownload_document")
            #print("download_document: ", message)
            
            start_msg = await message.reply_text(f"Pendiente de descarga: ", reply_to_message_id=message.id)
            
            user_id = message.from_user.id if message.from_user else None
            origin_group = message.forward_from.id if message.forward_from else message.forward_from_chat.id if message.forward_from_chat else None

            print(f"download_document user_id: [{user_id}] => [{env.AUTHORIZED_USER_ID}]")

            if str(user_id) in env.AUTHORIZED_USER_ID:
                file_name = getFileName(message)
                _FileSize = getFileSize(message)
                ext = file_name.split('.')[-1]
                download_path = config_handler.get_group_path(origin_group) or config_handler.get_download_path(ext)

                await start_msg.edit_text(f"Downloading file: {file_name}")

                file_name_download = os.path.join(download_path, file_name)

                start_time, start_hour = utils.startTime()

                #while attempt < env.MAX_RETRIES:
                while attempt < 100:
                    try:

                        print(f"[!!] File download start : [{attempt}]  {file_name_download}")
                        file_path = await message.download(file_name=file_name_download)


                        if _FileSize == os.path.getsize(file_path):
                            print(f"[!!] File download finish: [{attempt}] {file_path},  [{_FileSize}] == [{os.path.getsize(file_path)}] => [{message.id}]")

                            pendingMessagesHandler.remove_pending_message(message.id, message)
                            downloadFilesDB.add_download_files(
                                message.from_user.id,
                                origin_group,
                                message.id, 
                                file_path
                            )

                            break

                        print(f"[!!] File download FloodWait: [{attempt}] {file_path}  _FileSize [{_FileSize}] getsize: [{os.path.getsize(file_path)}]")
                        
                        if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
                            print(f"File download failed: {file_path}, {os.path.getsize(file_path)}")
                            attempt += 1
                            await start_msg.edit_text(f"Downloading file: {file_name} \nwait 60 seconds\nretry: {attempt}")
                            time.sleep(60)


                    except FloodWait as e:
                        print(f"FloodWait Exception: {e} ")
                        await message.reply_text(f"Downloading file FloodWait: {e}", reply_to_message_id=message.id)
                        time.sleep(60)

                    except Exception as e:
                        print(f"Exception Exception: {e} ")
                        await message.reply_text(f"Downloading file Exception: {e}", reply_to_message_id=message.id)
                        attempt += 1
                        print(f"Attempt {attempt} failed: {e}")
                        time.sleep(60)
                        if attempt == env.MAX_RETRIES:
                            print("Maximum retries reached. Download failed.")
                            # Optionally, you can handle the failure case here, like logging or notifying.


                if not _FileSize == os.path.getsize(file_path):
                    await start_msg.edit_text(f"Downloading failed: {file_name}\nretry: {attempt}")
                    return False
                
                end_time, end_hour = utils.endTime()
                elapsed_time = utils.elapsedTime(start_time, end_time)
                file_size, size_str = utils.getSize(file_path)
                download_speed = file_size / elapsed_time / 1024  # KB/s

                download_info = {
                    'file_name': file_name,
                    'download_folder': download_path,
                    'size_str': size_str,
                    'start_hour': start_hour,
                    'end_hour': end_hour,
                    'elapsed_time': elapsed_time,
                    'download_speed': download_speed,
                    'origin_group': message.forward_from.id if message.forward_from else message.forward_from_chat.id if message.forward_from_chat else None ,
                    'retries': attempt
                }

                ## file_name_download = getFolderDownload()
                ## startTime()
                ## file_path = await message.download(file_name=file_name_download, block=True)
                ## endTime()
                ## downloadInfo() # summary
                ## changePermissionsFile() 

                #summary = await download_file(message)

                ## TODO
                ## guardar archivo descargado en json de descargas, para poder 
                ##  renombrar
                ##  mover
                ##  etc
                ## 

                summary = utils.create_download_summary(download_info)
                await start_msg.edit_text(summary)
            else:
                await message.reply_text("No tienes permiso para descargar este archivo.")

            if env.IS_DELETE: await message.delete()


async def progress_callback(current, total):
    """Callback function to report download progress."""
    # Optionally, you can implement more detailed progress reporting here
    #print(f"Downloaded {current}/{total} bytes.")
    pass


@app.on_message(filters.private)
async def hello(client, message):
    await message.reply("Hello from Pyrogram!")


@app.on_message(filters.media)
async def download(client: Client, message: Message):
    print("No soportado : ", message)


# Register command handler
@app.on_message(filters.command(["help", "move", "folder", "addgroup"]))
async def handle_commands(client: Client, message: Message):
    print("handle_commands : ", message)
    await command_handler.handle_commands(client, message)


@app.on_message(filters.text)
async def handle_text_messages(client, message: Message):
    print("handle_text_messages : ", message)
    async with semaphore:
        urls = URL_REGEX.findall(message.text)
        if urls:
            for url in urls:
                await url_downloader.download_from_url(client, message, url)  # Use the class method


@app.on_callback_query(filters.regex(r'^subject_.*'))
async def handle_callback_query(client, callback_query: CallbackQuery):
    await url_downloader.handle_callback_query(client, callback_query)


if __name__ == "__main__":

    print("Telegram Downloader Bot Started")
    app.run()
    print("Telegram Downloader Bot Finish")
