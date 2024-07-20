# -*- coding: utf-8 -*-
print("\033c")

import os
from time import sleep, time, strftime, localtime
from datetime import datetime
import asyncio
import logging
import uvloop
from pyrogram import Client, filters, __version__ as pyrogram_version
from pyrogram.types import Message
from env import Env
#from downloader import download_file, get_file_name  # Importar la función download_file desde downloader.py
#from utils import format_file_size, create_download_summary, removeFiles  # Importar las funciones desde utils.py
from utils import Utils 
from print_utils import PartialPrinter

BOT_VERSION = "5.0.0.6"

uvloop.install()
logger = logging.getLogger(__name__)

printer = PartialPrinter()
utils = Utils()
env = Env()

utils.removeFiles()

msg_txt = ""
app = Client("telegramBot", api_id = int(env.API_ID), api_hash = env.API_HASH, bot_token = env.BOT_TOKEN, workers=env.MAX_CONCURRENT_TRANSMISSIONS, max_concurrent_transmissions=env.MAX_CONCURRENT_TRANSMISSIONS)
with app:
    now = datetime.now()
    dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
    msg_txt = "Telegram Downloader Bot Started\n\n"
    msg_txt += f"bot version: {BOT_VERSION}\n"
    msg_txt += f"pyrogram version: {pyrogram_version}\n"
    #msg_txt += f"yt-dlp version: 2024.05.27"
    
    print("Telegram Downloader Bot Started : ", dt_string)
    app.send_message(int(env.AUTHORIZED_USER_ID), msg_txt)
    printer.print_variable("BOT_VERSION", BOT_VERSION)
    printer.print_variable("PYROGRAM_VERSION", pyrogram_version)
    printer.print_variables()



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
        return message.audio.title
    else:
        print("message: ", message)
        return "Archivo"

@app.on_message(filters.document | filters.photo | filters.video | filters.audio | filters.animation)
async def download_document(client: Client, message: Message):
    print("download_document: ", message)
    attempt = 0
    start_msg = await message.reply_text(f"Downloading file: {getFileName(message)}", reply_to_message_id=message.id)

    file_name = getFileName(message)
    download_folder, file_name_download = utils.getDownloadFolder(file_name)
    start_time, start_hour = utils.startTime()

    file_path = await message.download(file_name=file_name_download, block=True)


    end_time, end_hour = utils.endTime()
    elapsed_time = utils.elapsedTime(start_time, end_time)
    file_size, size_str = utils.getSize(file_path)
    download_speed = file_size / elapsed_time / 1024  # KB/s

    download_info = {
        'file_name': file_name,
        'download_folder': download_folder,
        'size_str': size_str,
        'start_hour': start_hour,
        'end_hour': end_hour,
        'elapsed_time': elapsed_time,
        'download_speed': download_speed,
        'origin_group': message.forward_from.id if message.forward_from.id else None,
        'retries': attempt
    }

    ## file_name_download = getFolderDownload()
    ## startTime()
    ## file_path = await message.download(file_name=file_name_download, block=True)
    ## endTime()
    ## downloadInfo() # summary
    ## changePermissionsFile() 

    #summary = await download_file(message)

    
    summary = utils.create_download_summary(download_info)
    await start_msg.edit_text(summary)

    if env.IS_DELETE: await message.delete()

@app.on_message(filters.media)
async def download(client: Client, message: Message):
      print("No soportado : ", message.media)
      print("No soportado : ", message)

# Arranque
@app.on_message(filters.command("start"))
async def send_welcome(client: Client, message: Message):
    await message.reply_text(msg_txt)
    sleep(3)
    await message.delete()

if __name__ == "__main__":
    app.run()

