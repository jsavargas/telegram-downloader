# -*- coding: utf-8 -*-
print("\033c")

import os
import time
from datetime import datetime
import asyncio
import logging
import uvloop
from pyrogram import Client, filters, __version__ as pyrogram_version
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from env import Env
from utils import Utils 
from print_utils import PartialPrinter
from config_manager import ConfigurationManager

BOT_VERSION = "5.0.0.7"

uvloop.install()
logger = logging.getLogger(__name__)

printer = PartialPrinter()
utils = Utils()
env = Env()

utils.removeFiles()

msg_txt = ""
app = Client("telegramBot", api_id = int(env.API_ID), api_hash = env.API_HASH, bot_token = env.BOT_TOKEN, workers=env.MAX_CONCURRENT_TRANSMISSIONS, max_concurrent_transmissions=env.MAX_CONCURRENT_TRANSMISSIONS)

while True:
    try:
        with app:
            now = datetime.now()
            dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
            msg_txt = "Telegram Downloader Bot Started\n\n"
            msg_txt += f"bot version: {BOT_VERSION}\n"
            msg_txt += f"pyrogram version: {pyrogram_version}\n"
            #msg_txt += f"yt-dlp version: 2024.05.27"
            
            print("Telegram Downloader Bot Started : ", dt_string)
            app.send_message(int(env.AUTHORIZED_USER_ID[0]), msg_txt)
            printer.print_variable("BOT_VERSION", BOT_VERSION)
            printer.print_variable("PYROGRAM_VERSION", pyrogram_version)
            printer.print_variables()
            break  # Salir del bucle si el mensaje se envía exitosamente
    except FloodWait as e:
        print(f"FloodWait: Esperando {e.value} segundos antes de reintentar...")
        #time.sleep(e.value)  # Esperar el tiempo indicado antes de reintentar
        remaining_time = e.value
        while remaining_time > 0:
            print(f"Remaining time: {remaining_time} seconds", flush=True)
            time.sleep(30)
            remaining_time -= 30


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
    attempt = 0
    file_path = ""
    try:
        print("\ndownload_document")
        print("download_document: ", message)
        user_id = message.from_user.id if message.from_user else None
        
        print(f"download_document user_id: [{user_id}] => [{env.AUTHORIZED_USER_ID}]")

        if str(user_id) in env.AUTHORIZED_USER_ID:

            file_name = getFileName(message)
            start_msg = await message.reply_text(f"Downloading file: {file_name}", reply_to_message_id=message.id)

            download_folder, file_name_download = utils.getDownloadFolder(file_name)
            start_time, start_hour = utils.startTime()

            while attempt < env.MAX_RETRIES:
            
                try:
                    file_path = await message.download(file_name=file_name_download, block=True)
                    print(f"File downloaded to: {file_path}")
                    break
                except Exception as e:
                    attempt += 1
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt == env.MAX_RETRIES:
                        print("Maximum retries reached. Download failed.")
                        # Optionally, you can handle the failure case here, like logging or notifying.



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

    except Exception as e:
        print(f"download_document Exception: {message}: {e}")

    if env.IS_DELETE: await message.delete()

@app.on_message(filters.media)
async def download(client: Client, message: Message):
      print("No soportado : ", message.media)
      print("No soportado : ", message)

# Arranque
@app.on_message(filters.command("start"))
async def send_welcome(client: Client, message: Message):
    print(f"send_welcome start: {Message}", flush=True)
    await message.reply_text(msg_txt)

@app.on_message(filters.command(["help", "move", "folder"]))
async def my_handler(client, message):
    try:

        print(message)
        message_str = str(message)
        with open("messages.txt", "a") as file:
            file.write(f"{message_str} \n\n\n")
        

        if message.text == "/move" and message.reply_to_message_id:
            print(f"/move reply_to_message_id: {message.reply_to_message_id}")
            if message.reply_to_message:
                file_name = getFileName(message.reply_to_message)
                download_folder, file_name_download = utils.getDownloadFolder(file_name)

                # 'origin_group': message.forward_from.id if message.forward_from else message.forward_from_chat.id if message.forward_from_chat else None ,

                group_id = message.reply_to_message.forward_from.id if message.reply_to_message.forward_from else message.reply_to_message.forward_from_chat.id if message.reply_to_message.forward_from_chat else None
                print(f"/move file_name: {file_name} => {group_id}")
                print(f"/move download_folder: {download_folder} => {file_name_download}")
                move = utils.moveFile(group_id, file_name_download)
                print(f"/move move: {file_name_download} => {move}")
                await message.reply_text(f"move: {file_name_download} to {move}")

        if message.text == "/folder" and message.reply_to_message_id:
            group_id = message.reply_to_message.forward_from.id if message.reply_to_message.forward_from else message.reply_to_message.forward_from_chat.id if message.reply_to_message.forward_from_chat else None
            createGroupFolder = utils.createGroupFolder(group_id)
            if createGroupFolder:
                await message.reply_text(f"create folder: {createGroupFolder}")

    except Exception as e:
        logging.error(f"Error al manejar el mensaje: {e}")



if __name__ == "__main__":

    print("__main__ : ")
    app.run()
    print("__main__ : ")
