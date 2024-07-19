# -*- coding: utf-8 -*-
print("\033c")

import os
from time import sleep, time, strftime, localtime
from datetime import datetime
import asyncio
import logging
import uvloop
from pyrogram import Client, filters, __version__ as pyrogram_version
from env import Env
from downloader import download_file, get_file_name  # Importar la función download_file desde downloader.py
#from utils import format_file_size, create_download_summary, removeFiles  # Importar las funciones desde utils.py
from utils import Utils 
from print_utils import PartialPrinter

BOT_VERSION = "5.0.0.5"

uvloop.install()
logger = logging.getLogger(__name__)

printer = PartialPrinter()
utils = Utils()



utils.removeFiles()
#printer.print_variables()
#exit()
msg_txt = ""
app = Client("telegramBot", api_id = int(Env.API_ID), api_hash = Env.API_HASH, bot_token = Env.BOT_TOKEN, workers=Env.MAX_CONCURRENT_TRANSMISSIONS, max_concurrent_transmissions=Env.MAX_CONCURRENT_TRANSMISSIONS)
with app:
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
    msg_txt = "Telegram Downloader Bot Started\n\n"
    msg_txt += f"bot version: {BOT_VERSION}\n"
    msg_txt += f"pyrogram version: {pyrogram_version}\n"
    #msg_txt += f"yt-dlp version: 2024.05.27"
    
    print("Telegram Downloader Bot Started : ", dt_string)
    app.send_message(int(Env.AUTHORIZED_USER_ID), msg_txt)
    printer.print_variable("BOT_VERSION", BOT_VERSION)
    printer.print_variable("PYROGRAM", pyrogram_version)
    printer.print_variables()

###
# Arranque
@app.on_message(filters.command("start"))
async def send_welcome(client, message):
    await message.reply_text(msg_txt)
    sleep(3)
    await message.delete()


@app.on_message(filters.document | filters.photo)
async def download_document(client, message):
    print("download_document: ", get_file_name(message))

    start_msg = await message.reply_text(f"starting: {get_file_name(message)}", reply_to_message_id=message.id)
    summary = await download_file(message)
    await start_msg.edit_text(summary)

    if Env.IS_DELETE: await message.delete()



if __name__ == "__main__":
    app.run()

