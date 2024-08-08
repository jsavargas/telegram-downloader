import os
import time
import aiohttp
import asyncio
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from utils import Utils
from config_handler import ConfigHandler

class URLDownloader:
    def __init__(self):
        self.default_download_type = os.getenv("DEFAULT_DOWNLOAD_TYPE", "video")
        self.pending_callbacks = {}  # To store pending callback queries
        self.config_handler = ConfigHandler()
        self.youtubeLinks = {}

    async def download_from_url(self, client: Client, message: Message, url: str):
        
        try:
            origin_group = message.forward_from.id if message.forward_from else message.forward_from_chat.id if message.forward_from_chat else None

            if 'youtube.com' in url or 'youtu.be' in url:
                await self.send_download_options(client, message, url)
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            file_name = url.split("/")[-1]
                            ext = file_name.split('.')[-1]
                            download_path = self.config_handler.get_download_path(origin_group, file_name, message)

                            file_path = os.path.join(download_path, file_name)
                            with open(file_path, 'wb') as f:
                                f.write(await response.read())
                            await message.reply_text(f"File {file_name} downloaded to: \n{file_path}")
        except Exception as e:
            print(f"Exception download_from_url: {e} ")
            await message.reply_text(f"Exception in download_from_url: {url}")


    async def send_download_options(self, client: Client, message: Message, url: str):
        buttons = [
            [InlineKeyboardButton("Download Video", callback_data=f"ytdown_video_{message.id}")],
            [InlineKeyboardButton("Download Audio", callback_data=f"ytdown_audio_{message.id}")],
            [InlineKeyboardButton("Download Both", callback_data=f"ytdown_both_{message.id}")]
        ]

        self.youtubeLinks[message.id] = url

        reply_markup = InlineKeyboardMarkup(buttons)
        prompt_message = await message.reply_text("Choose download type:", reply_markup=reply_markup)
        
        print(f"prompt_message: prompt_message.id [{prompt_message.id}]")

        self.pending_callbacks[prompt_message.id] = {
            "message": prompt_message,
            "url": url,
            "timestamp": asyncio.get_event_loop().time()
        }

        await asyncio.sleep(5)
        
        if prompt_message.id in self.pending_callbacks:
            print(f"default download [{ prompt_message.id}]")
            # No option selected, proceed with default download type
            await self.download_with_default_type(client, prompt_message, url)
            del self.pending_callbacks[prompt_message.id]

        #Delete the prompt message
        #await prompt_message.delete()

    async def download_with_default_type(self, client: Client, message: Message, url: str):
        download_type = self.default_download_type
        await self.download_youtube_content(client, message, url, download_type)

    def progress_hook(self, info):
        if info["status"] == "downloading":
            percent = info["_percent_str"]
            print(f"Descargando: {percent}")
        print(f"progress_hook Descargando title: {info['title']}")

    async def download_youtube_content(self, client: Client, message: Message, url: str, download_type: str):
        
        try:
            await message.edit("downloading video")
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': '/download/%(title)s.%(ext)s',
                "progress_hooks": [self.progress_hook],
            }
            
            if download_type == "audio":
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            
            if download_type == "video":
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
            
            if download_type == "both":
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
                ydl_opts['merge_output_format'] = 'mkv'
            
            start_time = time.time()

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:

                playlist_info = ydl.extract_info(url, download=False)
                
                # Verificar si es una lista de reproducción
                if 'entries' in playlist_info:
                    num_videos = len(playlist_info['entries'])
                    print(f"Número de videos en la lista de reproducción: {num_videos}")


                ydl.download([url])

            end_time = time.time()
            duration = end_time - start_time

            # Datos para mostrar
            download_speed = 0  # La velocidad promedio requiere cálculo adicional
            print(f"\nDetalles de la descarga:")
            print(f"Cantidad de videos descargados: {num_videos}")
            print(f"Ruta de descarga: {os.path.abspath('downloads')}")
            print(f"Hora de inicio: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
            print(f"Hora de finalización: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time))}")
            print(f"Duración total: {duration:.2f} segundos")


            await message.edit(f"{download_type.capitalize()} downloaded for URL: {url}")
        except Exception as e:
            print(f"download_youtube_content Exception: {message}: {e}")
            await message.edit(f"{download_type.capitalize()} downloaded for URL: {url}\n{e}")

    async def handle_callback_query(self, client: Client, callback_query: CallbackQuery):
        data = callback_query.data
        _, download_type, message_id = data.split('_', 2)
        
        url = self.youtubeLinks[int(message_id)]
        removed_value = self.youtubeLinks.pop(int(message_id))

        print(f"callback_query url: [{url}]")
        print(f"callback_query removed_value: [{removed_value}]")
        print(f"callback_query.message.id: [{callback_query.message.id}]")
        print(f"callback_query.message.id pending_callbacks: [{self.pending_callbacks}]")

        if callback_query.message.id in self.pending_callbacks:
            print(f"default download delete [{callback_query.message.id}]")

            del self.pending_callbacks[callback_query.message.id]

        await self.download_youtube_content(client, callback_query.message, url, download_type)
        #await callback_query.message.edit_text(f"{download_type.capitalize()} downloaded for URL: {url}")



