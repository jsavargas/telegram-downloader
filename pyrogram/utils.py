# utils.py

from pyrogram.types import Message

def get_file_type(message: Message) -> str:
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
