import aiohttp
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from utils import Utils
import os
import asyncio

class URLDownloader:
    def __init__(self):
        self.default_download_type = os.getenv("DEFAULT_DOWNLOAD_TYPE", "video")
        self.pending_callbacks = {}  # To store pending callback queries

    async def download_from_url(self, client: Client, message: Message, url: str):
        if 'youtube.com' in url or 'youtu.be' in url:
            await self.send_download_options(client, message, url)
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        file_name = url.split("/")[-1]
                        file_path = os.path.join("/download", file_name)
                        with open(file_path, 'wb') as f:
                            f.write(await response.read())
                        await message.reply_text(f"File {file_name} downloaded to {file_path}")

    async def send_download_options(self, client: Client, message: Message, url: str):
        buttons = [
            [InlineKeyboardButton("Download Video", callback_data=f"subject_video_{url}")],
            [InlineKeyboardButton("Download Audio", callback_data=f"subject_audio_{url}")],
            [InlineKeyboardButton("Download Both", callback_data=f"subject_both_{url}")]
        ]
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


    async def download_youtube_content(self, client: Client, message: Message, url: str, download_type: str):
        
        try:
            await message.edit("downloading video")
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': '/download/%(title)s.%(ext)s',
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

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            await message.edit(f"{download_type.capitalize()} downloaded for URL: {url}")
        except Exception as e:
            print(f"download_youtube_content Exception: {message}: {e}")
            await message.edit(f"{download_type.capitalize()} downloaded for URL: {url}\n{e}")

    async def handle_callback_query(self, client: Client, callback_query: CallbackQuery):
        data = callback_query.data
        _, download_type, url = data.split('_', 2)

        print(f"callback_query.message.id: [{callback_query.message.id}]")
        print(f"callback_query.message.id pending_callbacks: [{self.pending_callbacks}]")

        if callback_query.message.id in self.pending_callbacks:
            print(f"default download delete [{callback_query.message.id}]")

            del self.pending_callbacks[callback_query.message.id]

        await self.download_youtube_content(client, callback_query.message, url, download_type)
        #await callback_query.message.edit_text(f"{download_type.capitalize()} downloaded for URL: {url}")



