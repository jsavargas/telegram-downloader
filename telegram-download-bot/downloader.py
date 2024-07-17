import os
import time
from pyrogram.types import Message
from utils import get_file_name, create_download_summary, format_file_size
from env import Env

async def download_file(message: Message) -> str:
    file_name = get_file_name(message)
    start_time = time.time()
    start_hour = time.strftime("%H:%M:%S", time.localtime(start_time))

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
            'origin_group': message.id
        }

        summary = create_download_summary(download_info)

        return summary

    except Exception as e:
        return f"Error al descargar **{file_name}**: {str(e)}"
