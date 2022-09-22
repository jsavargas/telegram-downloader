import os
import time
import shutil
import asyncio
import json
import pdb
import re
from tqdm import tqdm

from pyrogram import Client

import utils.config
from utils.database import Database, Data, Object

OWNER = os.environ['OWNER']
APP_ID = int(os.environ['APP_ID'])
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']

PUID = os.environ['PUID']
PGID = os.environ['PGID']

progress_array = {}


def intToArray(init,limit):
    init = int(init)
    _numbers = []
    for i in range(init, init + limit):
        _numbers.append(i)
    return _numbers

async def get_chat_history(group='me',limit=30, init=None):
    data = []

    try:

        newDatabase = Database()
        lastID = newDatabase.getLastIDHistory(group)

        print(f" [!] get_chat_history lastID [{lastID}]" ,flush=True)

        async with Client("/config/my_account", api_id=APP_ID, api_hash=API_HASH) as app:
            #await xbot.send_message(OWNER, OWNER)

            chat = await app.get_chat(ifDIgit(group))

            print(f"[!] >>>>>>> chat.title [{chat.title}]" ,flush=True)
            print(f"[!] >>>>>>> lastID [{lastID}]" ,flush=True)
            if not init:
                async for message in app.get_chat_history(ifDIgit(group),limit=limit):
                    print(f" >>>>>>> [{message.id}]" ,flush=True)
                    if not lastID == None and message.id <= lastID: break
                    if str(message.media) == "MessageMediaType.VIDEO":
                        data.append(message)
            else:

                list = intToArray(init,limit)

                messages = await app.get_messages(ifDIgit(group),list)
                for message in messages:
                    if str(message.media) == "MessageMediaType.VIDEO":
                        data.append(message) 
                id=None
    except Exception as e:
        print(f"[!] >>>>>>> except get_chat_history [{e}]" ,flush=True)

        return data


    return data

async def downloadFile(group,message_id):

    try:
        #TODO: get filename desde la base de datos
        newDatabase = Database()

        _file_name = 'La ley de Baltazar _ Avance Capítulo 67 _ Mega.mp4'
        file_size = 23000000
        #TODO:

        print(f"\n\n\n [*]  [*]  [*]  [*]  [*]  [*] downloadFile: [{_file_name}], [{sizeof_fmt(file_size)}]", flush=True)
        _file_name, caption, file_size, message_bot = await downloadFile_temp(group,message_id)
        print(f" [*] downloadFile: [{_file_name}], [{sizeof_fmt(file_size)}]", flush=True)

        temp_file_path, final_file_path = getFileRename_temp(group,_file_name,caption)
        print(f" [*] downloadFile getFileRename_temp: [{temp_file_path}][{final_file_path}], [{sizeof_fmt(file_size)}]", flush=True)
        message_bot = await botSend(f"moving: {temp_file_path} to {final_file_path}  => {sizeof_fmt(file_size)}",message_bot)

        rmoveFile_temp = await moveFile_temp(temp_file_path, final_file_path)
        
        if not rmoveFile_temp: return False
        print(f" [*] downloadFile moveFile_temp: [{_file_name}], [{sizeof_fmt(file_size)}]", flush=True)
        message_bot = await botSend(f"Finish: \n{temp_file_path} to:\n {final_file_path}  => {sizeof_fmt(file_size)}",message_bot)

        rest = newDatabase.updateData(group,message_id,final_file_path)
        print(f" [*] downloadFile updateData: [{rest}]", flush=True)
        if not rest: return False

        return True
    except Exception as inst:
        print(f" [!!!] Exception telegram downloadFile [{inst}]", flush=True)    # the exception instance
        message_bot = await botSend(f"Error: \n{group}: {message_id}",message_bot)
        return False


async def downloadFile_temp(group,message_id):
    global pbar

    try:
        message_bot = None
        print(f"downloadind {group}\n message_id:{int(message_id)}", flush=True)    # the exception instance
        async with Client("/config/my_account", api_id=APP_ID, api_hash=API_HASH) as app:
            f = await app.get_messages(group,[int(message_id)])
            for message in f:

                if message.video.file_name == None: 
                    filename = message.caption
                else:
                    filename = message.video.file_name


                temp_file_path = os.path.join(utils.config.DOWNLOAD_PATH,'temp',filename)
                os.makedirs(os.path.join(utils.config.DOWNLOAD_PATH,'temp'), exist_ok=True)

                text = f"downloadind {group}\n file in: {temp_file_path}, {sizeof_fmt(message.video.file_size)}"
                print(text, flush=True)    # the exception instance
                message_bot = await botSend(text)

                
                if os.path.exists(temp_file_path) and (message.video.file_size == os.path.getsize(temp_file_path)):
                    print("d >>>>>>>>> downloadFile_temp exists [{}]".format(os.path.getsize(temp_file_path)), flush=True)    # the exception instance
                    return filename,message.caption,message.video.file_size,message_bot
                
                pbar = tqdm(total=100, desc =f" {message_id}")
                await app.download_media(message, file_name=temp_file_path, progress=progress, progress_args=[message_bot,text,group,message_id])
                pbar.close()

        return filename,message.caption,message.video.file_size,message_bot

    except Exception as inst:
        print(f"Exception telegram downloadFile_temp [{inst}]", flush=True)    # the exception instance
        await botSend(f"Exception telegram downloadFile_temp: {inst}")
        print(type(inst) , flush=True)    # the exception instance
        print(inst.args , flush=True)     # arguments stored in .args
        print(inst , flush=True)          # __str__ allows args to be printed directly,

        return None

def getFileRename_temp(group, file_name,caption=None):

    try:
        newDatabase = Database()
        
        temp_file_path = os.path.join(utils.config.DOWNLOAD_PATH,'temp',file_name)
        final_file_path = os.path.join(utils.config.DOWNLOAD_PATH,file_name)

        configGroups = newDatabase.getConfigGroup(group)
        for configGroup in configGroups:

            _regex_download     = configGroups[0]['regex_download']
            _regex_rename       = configGroups[0]['regex_rename']
            _folder_download    = configGroups[0]['folder_download']

            #_regex_rename = getRegex_rename(group)

            mrr = re.match('/(.*)/(.*)/', configGroup['regex_rename'])
            if mrr:
                if not re.match(mrr.group(1), file_name):
                    file_name = caption
                    #continue
                filename_rename = re.sub(mrr.group(1), mrr.group(2), file_name, flags=re.I)
                final_file_path = os.path.join(utils.config.DOWNLOAD_PATH,filename_rename)
                if configGroup['folder_download']:
                    final_file_path = os.path.join(configGroup['folder_download'],filename_rename)

                
                return temp_file_path, final_file_path
            else: 
                
            
                
                
                
                return temp_file_path, final_file_path
        
        return temp_file_path, final_file_path


    except Exception as e:
        print(f" >>>>>>> Exception getFileRename_temp [{e}]" ,flush=True)
        return temp_file_path, temp_file_path

async def moveFile_temp(temp_file_path, final_file_path):
    print(f" [*] moveFile_temp [{temp_file_path}][{final_file_path}]", flush=True)    # the exception instance

    try:
        dirname = os.path.dirname(final_file_path)
        basename = os.path.basename(final_file_path)
        os.makedirs(dirname, exist_ok=True)

        if os.path.exists(final_file_path):
            shutil.move(final_file_path, os.path.join(dirname,f".{basename}"))
        shutil.move(temp_file_path, final_file_path)
        os.chown(final_file_path, int(PUID), int(PGID))
        os.chmod(final_file_path, 0o666)

        return True
    except Exception as inst:
        print(f" [!!!] Exception telegram moveFile_temp [{inst}]", flush=True)    # the exception instance
        return False



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
        global pbar


        message_id, text, group, id = args[0], args[1], args[2], int(args[3])
        
        int_value = int(float("{:.2f}".format(current * 100 / total)) // 1)
        #print(f"progress progress [{int_value}][{progress_array}]", flush=True)    # the exception instance
        if ( (int_value) % 5 == 0): 
            pbar.n = (int(current * 100 / total))
            pbar.refresh() 

        if id not in progress_array:
            progress_array[id] = int_value   
        
        if progress_array[id] != int_value:
            progress_array[id] = int_value
            if ( (int_value) % 10 == 0): 

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
