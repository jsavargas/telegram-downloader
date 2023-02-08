import os
import time
import shutil
import asyncio
import json
import pdb
import re
from tqdm import tqdm

from pyrogram import Client
from pyrogram.raw import functions
from pyrogram.raw.functions.messages.get_all_chats import GetAllChats

#import utils.config
#from utils.database import Database, Data, Object
#from utils.utils import UTILS

OWNER = os.environ['OWNER']
APP_ID = int(os.environ['APP_ID'])
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']

PUID = os.environ['PUID']
PGID = os.environ['PGID']

DOWNLOAD_INCOMPLETED = os.getenv('DOWNLOAD_INCOMPLETED') or '/download/incompleted'

def ifDIgit(channel):
    channel = str(channel)

    if channel.isnumeric():
        channel = f"-100{channel}"
    else:
        channel = channel.lower()


    return int(channel) if any(map(str.isdigit,channel)) else channel


async def getAllChats():
    try:
        async with Client("/config/my_account", api_id=APP_ID, api_hash=API_HASH) as app:
            temp_chat = []
            #print(f"[!] >>>>>>> GetAllChats []" ,flush=True)
            AllChats = await app.invoke(GetAllChats(except_ids=[]))
            #print(f"[!] >>>>>>> chat.title [{AllChats}]" ,flush=True)
            #print(f"[!] >>>>>>> chat.title [{AllChats.chats[0]}]" ,flush=True)

            for chat in AllChats.chats:
                print(f"[!] >>>>>>> chat.title [{chat.title}]" ,flush=True)
                temp = {}
                temp['id'] = chat.id
                temp['title'] = chat.title
                temp['username'] = chat.username if not getattr(chat, 'username',None) == None else chat.id
                temp_chat.append(temp)
    
            return temp_chat

    except Exception as e:
        print(f"[!] >>>>>>> except GetAllChats [{e}]" ,flush=True)




async def get_chat_history(group='me',limit=100, init=None):
    data = []

    try:
        print(f"[!] >>>>>>> get_chat_history [{group}]" ,flush=True)

        async with Client("/config/my_account", api_id=APP_ID, api_hash=API_HASH) as app:

            print(f"[!] >>>>>>> app.get_chat " ,flush=True)
            
            chat = await app.get_chat(ifDIgit(group))

            print(f"[!] >>>>>>> chat.title [{chat.title}]" ,flush=True)
            #print(f"[!] >>>>>>> lastID [{lastID}]" ,flush=True)
            if not init:
                async for message in app.get_chat_history(ifDIgit(group),limit=limit):

                    #if not lastID == None and message.id <= lastID: break
                    if str(message.media) == "MessageMediaType.VIDEO":
                        dtemp = {}
                        dtemp['id']         = message.id
                        dtemp['file_name']  = message.video.file_name
                        dtemp['file_size']  = message.video.file_size
                        dtemp['width']      = message.video.width
                        dtemp['height']     = message.video.height
                        dtemp['caption']    = message.caption
                        dtemp['date']       = message.date
                        dtemp['message']    = message
                        data.append(dtemp)
                    if str(message.media) == "MessageMediaType.DOCUMENT":
                        dtemp = {}
                        dtemp['id']         = message.id
                        dtemp['file_name']  = message.document.file_name
                        dtemp['file_size']  = message.document.file_size
                        dtemp['width']      = ""
                        dtemp['height']     = "69412"
                        dtemp['caption']    = message.caption
                        dtemp['date']       = message.date
                        dtemp['message']    = message
                        data.append(dtemp)
            else:

                list = intToArray(init,limit)

                messages = await app.get_messages(ifDIgit(group),list)
                for message in messages:
                    if str(message.media) == "MessageMediaType.VIDEO":
                        dtemp = {}
                        dtemp['id']         = message.id
                        dtemp['file_name']  = message.video.file_name
                        dtemp['file_size']  = message.video.file_size
                        dtemp['width']      = message.video.width
                        dtemp['caption']    = message.caption
                        dtemp['date']       = message.date
                        dtemp['message']    = message
                        data.append(dtemp)
                    if str(message.media) == "MessageMediaType.DOCUMENT":
                        dtemp = {}
                        dtemp['id']         = message.id
                        dtemp['file_name']  = message.document.file_name
                        dtemp['file_size']  = message.document.file_size
                        dtemp['width']      = ""
                        dtemp['height']     = "69412"
                        dtemp['caption']    = message.caption
                        dtemp['date']       = message.date
                        dtemp['message']    = message
                        data.append(dtemp)
                id=None
    except Exception as e:
        print(f"[!] >>>>>>> except get_chat_history [{e}]" ,flush=True)

        return data

    return data


async def downloadFile(group,message_id):

    # /download

    try:
        async with Client("/config/my_account", api_id=APP_ID, api_hash=API_HASH) as app:

            f = await app.get_messages(group,[int(message_id)])
            for message in f:
                print(f"[!] >>>>>>> downloadFile message [{message}]" ,flush=True)

                if str(message.media) == "MessageMediaType.VIDEO":
                    if message.video.file_name:
                        file_name = message.video.file_name
                        temp_file_path = message.video.file_name
                    else:
                        temp_file_path = f"{group}-{message.id}"
                    text = f"downloadind file in: {temp_file_path}, {sizeof_fmt(message.video.file_size)}"
                if str(message.media) == "MessageMediaType.DOCUMENT":
                    if message.document.file_name:
                        file_name = message.document.file_name
                        temp_file_path = message.document.file_name
                    else:
                        temp_file_path = f"{group}-{message.id}"
                    text = f"downloadind file in: {temp_file_path}, {sizeof_fmt(message.document.file_size)}"

                message_bot = None
                download_path = os.path.join(DOWNLOAD_INCOMPLETED,temp_file_path)

                if not os.path.exists(download_path):
                    await app.download_media(message, file_name=download_path, progress=progress, progress_args=[message_bot,text,group,message_id])
                
                return True, message_bot, group, download_path, file_name, message.caption

    except Exception as e:
        print(f"[!] >>>>>>> except downloadFile [{e}]" ,flush=True)
        return False, message_bot, group, download_path, file_name, message.caption



# Keep track of the progress while downloading
async def progress(current, total, *args):
    try:
        print(f" progress {current}, {total}",  flush=True)
    except Exception as e:
        print(f"[!] >>>>>>> except progress [{e}]" ,flush=True)

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.2f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

