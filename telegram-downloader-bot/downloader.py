import os
import time
from pyrogram.types import Message
from utils import create_download_summary, format_file_size
from env import Env

async def download_file(message: Message) -> str:
    file_name = get_file_name(message)
    start_time = time.time()
    start_hour = time.strftime("%H:%M:%S", time.localtime(start_time))

    max_retries = 5
    attempt = 0

    while attempt < max_retries:
        try:

            # Descarga del archivo
            file_path = await message.download(file_name=os.path.join(Env.DOWNLOAD_DIR, file_name), block=True)
            end_time = time.time()
            end_hour = time.strftime("%H:%M:%S", time.localtime(end_time))

            elapsed_time = end_time - start_time
            file_size = os.path.getsize(file_path)
            download_speed = file_size / elapsed_time / 1024  # KB/s

            size_str = format_file_size(file_size)
            
            download_info = {
                'file_name': file_name,
                'size_str': size_str,
                'start_hour': start_hour,
                'end_hour': end_hour,
                'elapsed_time': elapsed_time,
                'download_speed': download_speed,
                'origin_group': message.chat.id if message.chat else None,
                'attempt': attempt
            }
            
            print(f"get_file_name: {file_name}, {file_size}")

            if file_size <= 0:
                attempt += 1
            else:
                summary = create_download_summary(download_info)

                return summary

        except RPCError as e:
            if "AUTH_BYTES_INVALID" in str(e):
                attempt += 1
                if attempt == max_retries:
                    return f"Error al descargar **{file_name}** ({file_type}): {str(e)}. Máximo número de intentos alcanzado."
            else:
                return f"Error al descargar **{file_name}** ({file_type}): {str(e)}"

        time.sleep(2)  # Esperar 2 segundos antes de reintentar

    return f"Error al descargar **{file_name}** ({file_type})."

def get_file_name(message: Message) -> str:
    if message.document:
        return message.document.file_name
    elif message.photo:
        return f"{message.photo.file_unique_id}.jpg"
    elif message.video:
        return message.video.file_name
    elif message.audio:
        return message.audio.title
    else:
        return "Archivo"


