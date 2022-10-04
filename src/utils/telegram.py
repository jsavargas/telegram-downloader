import os
import time
import shutil
import asyncio
import json
import pdb

from pyrogram import Client

import utils.config
from utils.utils import UTILS

OWNER = os.environ['OWNER']
APP_ID = int(os.environ['APP_ID'])
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']

PUID = os.environ['PUID']
PGID = os.environ['PGID']

progress_array = {}



async def get_chat_history(group='me',limit=30, init=None):

    data = []



    try:

        async with Client("/config/my_account", api_id=APP_ID, api_hash=API_HASH) as app:
            #await xbot.send_message(OWNER, OWNER)

            chat = await app.get_chat(ifDIgit(group))

            print(f"[!] >>>>>>> chat.title [{chat.title}]" ,flush=True)

            if not init:
                async for message in app.get_chat_history(ifDIgit(group),limit=limit):
                    #print(f" >>>>>>> [{message.media}]" ,flush=True)
                    if str(message.media) == "MessageMediaType.VIDEO":
                        data.append(message)


            else:

                list = intToArray(init,limit)

                messages = await app.get_messages(ifDIgit(group),list)
                for message in messages:
                    if str(message.media) == "MessageMediaType.VIDEO":
                        data.append(message) 
                id=None

        #print(f" >>>>>>> SALIENDO [{data}]" ,flush=True)

    except:
        return data


    return data

def intToArray(init,limit):
    init = int(init)
    _numbers = []
    for i in range(init, init + limit):
        _numbers.append(i)
    return _numbers


async def downloadFile(group,message_id):

    try:

        #print(f"telegram downloadFile [{group}] [{message_id}]", flush=True)

        _regex_download = utils.config.getRegex_download(group)
        _folder_download = utils.config.getDownloadPath(group)
        _regex_rename = utils.config.getRegex_rename(group)

        async with Client("/config/my_account", api_id=APP_ID, api_hash=API_HASH) as app:

            f = await app.get_messages(group,[int(message_id)])
            for message in f:

                if message.video.file_name == None: 
                    filename = message.caption
                else:
                    filename = message.video.file_name

                file_name = utils.config.getRegexFilename(group,filename)
                #print(f"telegram downloadFile message [{file_name}]", flush=True)

                temp_file_path = os.path.join(utils.config.DOWNLOAD_PATH,file_name)
                final_file_path = os.path.join(_folder_download,file_name)

                #print(f"telegram downloadFile [{temp_file_path}]", flush=True)
                #print(f"telegram downloadFile [{final_file_path}]", flush=True)

                text = f"downloadind file in: {temp_file_path}, {sizeof_fmt(message.video.file_size)}"

                print(f"downloadind file in: {temp_file_path} , {sizeof_fmt(message.video.file_size)}", flush=True)
                message_bot = await botSend(text)

                await app.download_media(message, file_name=temp_file_path, progress=progress, progress_args=[message_bot,text,group,message_id])

                os.makedirs(_folder_download, exist_ok=True)

                print(f"moving file: {temp_file_path} to {final_file_path}", flush=True)
                message_bot = await botSend(f"moving file: {temp_file_path} to {final_file_path}",message_bot)

                shutil.move(temp_file_path, final_file_path)

                os.chown(final_file_path, int(PUID), int(PGID))
                os.chmod(final_file_path, 0o666)

                print(f"download file: {final_file_path}, {sizeof_fmt(message.video.file_size)}", flush=True)
                message_bot = await botSend(f"download file: {final_file_path}, {sizeof_fmt(message.video.file_size)}",message_bot)

        return True

    except Exception as inst:
        print(f"Exception telegram downloadFile [{inst}]", flush=True)    # the exception instance
        await botSend(f"Exception telegram downloadFile: {inst}")
        print(type(inst) , flush=True)    # the exception instance
        print(inst.args , flush=True)     # arguments stored in .args
        print(inst , flush=True)          # __str__ allows args to be printed directly,

        return False



async def downloadFile2(group,message_id):

    try:
        #TODO: get filename desde la base de datos 

        

        _file_name, file_size = downloadFile_temp(group,message_id)
        print(f"download file: {final_file_path}, {sizeof_fmt(message.video.file_size)}", flush=True)

        _file_name = renameFile_temp(group,_file_name)
        print(f"download file: {final_file_path}, {sizeof_fmt(message.video.file_size)}", flush=True)

        _file_name = moveFile_temp(_file_name)
        print(f"download file: {final_file_path}, {sizeof_fmt(message.video.file_size)}", flush=True)

    except Exception as inst:
        print(f"Exception telegram downloadFile [{inst}]", flush=True)    # the exception instance








async def downloadFile_temp(group,message_id):

    print(f"downloadFile_temp: {group}, {message_id}", flush=True)

    try:
        async with Client("/config/my_account", api_id=APP_ID, api_hash=API_HASH) as app:

            f = await app.get_messages(group,[int(message_id)])
            for message in f:

                newutils = UTILS()

                filename = newutils.getFilename(message)
                file_size = newutils.getFilesize(message)

                if filename == None: 
                    filename = message.caption
                else:
                    filename = filename

                temp_file_path = os.path.join(utils.config.DOWNLOAD_PATH,filename)

                await app.download_media(message, file_name=temp_file_path, progress=progress, progress_args=[message_bot,text,group,message_id])


        return temp_file_path,file_size

    except Exception as inst:
        print(f"Exception telegram downloadFile [{inst}]", flush=True)    # the exception instance
        await botSend(f"Exception telegram downloadFile: {inst}")
        print(type(inst) , flush=True)    # the exception instance
        print(inst.args , flush=True)     # arguments stored in .args
        print(inst , flush=True)          # __str__ allows args to be printed directly,

        return None


async def renameFile_temp(group,filename):
    try:

        newDatabase = Database()
        configGroups = newDatabase.getConfigGroup(group)
        if configGroups:
            _regex_download     = configGroups[0]['regex_download']
            _regex_rename       = configGroups[0]['regex_rename']
            _folder_download    = configGroups[0]['folder_download']
    
        regex, rename = utils.config.getFileRename2(data,_regex_download,_regex_rename)



        return temp_file_path,message.video.file_size

    except Exception as inst:
        print(f"Exception telegram downloadFile [{inst}]", flush=True)    # the exception instance
        await botSend(f"Exception telegram downloadFile: {inst}")
        print(type(inst) , flush=True)    # the exception instance
        print(inst.args , flush=True)     # arguments stored in .args
        print(inst , flush=True)          # __str__ allows args to be printed directly,

        return None




























def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.2f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


# Keep track of the progress while downloading
async def progress(current, total, *args):

    try:
        global progress_array

        message_id, text, group, id = args[0], args[1], args[2], int(args[3])

        int_value = int(float("{:.2f}".format(current * 100 / total)) // 1)
        #print(f"progress progress [{int_value}][{progress_array}]", flush=True)    # the exception instance
        
        if id not in progress_array:
            progress_array[id] = int_value   
        
        if progress_array[id] != int_value:
            progress_array[id] = int_value
            if ( (int_value) % 10 == 0): 
                #print(f"{current * 100 / total}% {args}",  flush=True)
                await botSend(f"{text} {current * 100 / total:.1f}%",message_id)
        if int_value == 100:
            progress_array.pop(id)

    except Exception as e:
        print(f"ERROR progress {e}",  flush=True)


async def botSend(message,message_bot=None):
    try:
        async with Client("/config/bot", api_id=APP_ID, api_hash=API_HASH,bot_token=BOT_TOKEN) as xbot:
            if message_bot == None: return await xbot.send_message(OWNER, message)
            else: return await xbot.edit_message_text(OWNER, message_id=message_bot.id,text=message)

    except Exception as error:
        print('__name__',error,flush=True)
  

def ifDIgit(channel):

    return int(channel) if any(map(str.isdigit,channel)) else channel





if __name__ == "__main__":

    print('__name__')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(botSend("prueba"))
