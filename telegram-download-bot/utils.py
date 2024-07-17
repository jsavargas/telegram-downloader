# utils.py

from pyrogram.types import Message

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

def format_file_size(file_size: int) -> str:
    if file_size < 1024:
        return f"{file_size} bytes"
    elif file_size < 1024 * 1024:
        return f"{file_size / 1024:.2f} KB"
    else:
        return f"{file_size / (1024 * 1024):.2f} MB"

def ccreate_download_summary(download_info):
    """
    Crea un mensaje de resumen para la descarga completada a partir de un objeto con la información de la descarga.
    
    Args:
    - download_info (dict): Diccionario con la siguiente estructura:
        {
            'file_name': str,
            'size_str': str,
            'start_hour': str,
            'end_hour': str,
            'elapsed_time': float,
            'download_speed': float
        }
    
    Returns:
    - str: Mensaje de resumen formateado.
    """
    summary = (
        f"**Descarga completada**\n\n"
        f"**Nombre del archivo:** {download_info['file_name']}\n"
        f"**Tamaño del archivo:** {download_info['size_str']}\n"
        f"**Hora de inicio:** {download_info['start_hour']}\n"
        f"**Hora de finalización:** {download_info['end_hour']}\n"
        f"**Tiempo de descarga:** {download_info['elapsed_time']:.2f} segundos\n"
        f"**Velocidad de descarga:** {download_info['download_speed']:.2f} KB/s\n"
        f"**From:** {download_info['from']} segundos"
    )
    return summary

def create_download_summary(download_info):
    """
    Creates a download summary message based on the download information.

    Args:
    - download_info (dict): Dictionary with the following structure:
        {
            'file_name': str,
            'size_str': str,
            'start_hour': str,
            'end_hour': str,
            'elapsed_time': float,
            'download_speed': float,
            'origin_group': str or None (optional)
        }
    
    Returns:
    - str: Formatted download summary message.
    """
    file_name = download_info['file_name']
    size_str = download_info['size_str']
    start_hour = download_info['start_hour']
    end_hour = download_info['end_hour']
    elapsed_time = download_info['elapsed_time']
    download_speed = download_info['download_speed']
    origin_group = download_info.get('origin_group', None)

    summary = (
        f"**Download completed**\n\n"
        f"**File Name:** {file_name}\n"
        f"**File Size:** {size_str}\n"
        f"**Start Time:** {start_hour}\n"
        f"**End Time:** {end_hour}\n"
        f"**Download Time:** {elapsed_time:.2f} seconds\n"
        f"**Download Speed:** {download_speed:.2f} KB/s"
    )

    if origin_group:
        summary += f"\n**Origin Group:** {origin_group}"

    return summary

