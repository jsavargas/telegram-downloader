# -*- coding: utf-8 -*-
print("\033c")

import os
from time import sleep, time, strftime, localtime
from datetime import datetime
import asyncio
import logging
import uvloop
from pyrogram import Client, filters
from config import *
from env import Env
from downloader import download_file  # Importar la función download_file desde downloader.py
from utils import get_file_name, format_file_size, create_download_summary  # Importar las funciones desde utils.py


if os.path.exists("bot_4" + ".session"): os.remove("bot_4" + ".session")

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# Variables globales
folder_name = ""
last_forward_time = 0
###
uvloop.install()
logger = logging.getLogger(__name__)


app = Client("bot_4", api_id = int(api_id), api_hash = api_hash, bot_token = bot_token, workers=2, max_concurrent_transmissions=2)
with app:
    print("BOT.Torrent 4.0 : ", dt_string)
    app.send_message(int(usuario_id), mensaje_inicio)
###
# Arranque
@app.on_message(filters.command("start"))
async def send_welcome(client, message):
    await message.reply_text(mensaje_inicio)
    sleep(3)
    await message.delete()


@app.on_message(filters.document)
async def download_document(client, message):
    global folder_name, last_forward_time


    start_msg = await message.reply_text(f":: {get_file_name(message)}", reply_to_message_id=message.id)
    summary = await download_file(message)
    await start_msg.edit_text(summary)


    return 

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if message.document.file_name.endswith('.torrent'):
        download_path = os.path.join(directorio_torrent, message.document.file_name)
    else:
        if not folder_name or (time() - last_forward_time > 30):
            folder_name = f"Otros_{now.minute}_{message.document.file_name.split('.')[0]}"
            print(dt_string + " Carpeta: " + folder_name)
            last_forward_time = time()
            
        full_path = os.path.join(directorio_multimedia, folder_name)
        download_path = os.path.join(full_path, message.document.file_name)
        if time() - last_forward_time > 30: folder_name = ""
    print( " : " + message.document.file_name)
    #await message.reply_text(" : " + message.document.file_name)

    start_time = time()
    start_hour = strftime("%H:%M:%S", localtime(start_time))

    start_msg = await message.reply_text(f":: {message.document.file_name}", reply_to_message_id=message.id)

    await asyncio.sleep(0.4)
    end_file_path = await message.download(download_path, block = True)

    end_time = time()
    end_hour = strftime("%H:%M:%S", localtime(end_time))

    elapsed_time = end_time - start_time
    file_size = os.path.getsize(end_file_path)
    download_speed = file_size / elapsed_time / 1024  # KB/s

    # Convertir el tamaño del archivo a una unidad legible
    if file_size < 1024:
        size_str = f"{file_size} bytes"
    elif file_size < 1024 * 1024:
        size_str = f"{file_size / 1024:.2f} KB"
    else:
        size_str = f"{file_size / (1024 * 1024):.2f} MB"

    # Crear el mensaje de resumen
    summary = (
        f"**Descarga completada**\n\n"
        f"**Nombre del archivo:** {message.document.file_name}\n"
        f"**Tamaño del archivo:** {size_str}\n"
        f"**Hora de inicio:** {start_hour}\n"
        f"**Hora de finalización:** {end_hour}\n"
        f"**Tiempo de descarga:** {elapsed_time:.2f} segundos\n"
        f"**Velocidad de descarga:** {download_speed:.2f} KB/s"
    )

    #await message.reply_text(summary, reply_to_message_id=message.id)
    await start_msg.edit_text(summary)
    #await message.delete()

# No reconocido
@app.on_message(filters.media)
async def download(client, message):
      print("No soportado : ", message.media)
# Eco
@app.on_message(filters.text & filters.private)
async def echo(client, message):
    await message.reply(message.text)
    sleep(3)
    await message.delete()



if __name__ == "__main__":
    app.run()

