import os
import re
import time
import sqlite3
import asyncio
import shutil

import controllers.telegram
from controllers.database import Database

DOWNLOAD_COMPLETED = os.getenv('DOWNLOAD_COMPLETED') or '/download/completed'
DOWNLOAD_INCOMPLETED = os.getenv('DOWNLOAD_INCOMPLETED') or '/download/incompleted'

PUID = os.environ['PUID']
PUID = os.environ['PUID']
PGID = os.environ['PGID']


def regexDownload(group, file_name,caption=None,regex_download='',regex_rename=''):
    download = True
    
    try:
        #print(f" regexDownload:: [{group}], [{file_name}], [{caption}] [{regex_download}] [{regex_rename}]")

        if re.match(regex_download, file_name, flags=re.I):
            download = True
        elif re.match(regex_download, caption, flags=re.I):
            download = True
        else:
            download = False

        return download

    except Exception as e:
        print(f" regexDownload Exception:: {e}")
        return False

def regexRename(group, file_name,caption=None,regex_download='',regex_rename='',force=False):
    rename = ''

    try:
        #print(f" regexRename:: [{group}], [{file_name}], [{caption}] [{regex_download}] [{regex_rename}]")

        if re.match(regex_download, file_name, flags=re.I):
            mrr = re.match('/(.*)/(.*)/', regex_rename, flags=re.I)
            if mrr:
                rename = re.sub(mrr.group(1), mrr.group(2), file_name, flags=re.I)
            else:
                rename = file_name
        elif re.match(regex_download, caption, flags=re.I):
            mrr = re.match('/(.*)/(.*)/', regex_rename)
            if mrr:
                rename = re.sub(mrr.group(1), mrr.group(2), caption.replace("\n", ""), flags=re.I)
            else:
                rename = caption

        elif force and file_name: 
            rename = file_name
        elif force and caption: 
            rename = caption
        else:
            rename = ''

        return rename

    except Exception as e:
        print(f"[!] >>>>>>> except regexRename [{e}]" ,flush=True)

def ifDownloaded(group, message_id):

    try:
        newDatabase = Database()

        status = newDatabase.ifDownloaded(group, message_id)
        #print(f" [*] successfully ifDownloaded: [{group}][{message_id}] [{status}]", flush=True)

        return status
    except Exception as e:
        print(f"[!] >>>>>>> except ifDownloaded [{e}]" ,flush=True)
        return False


async def downloadFile(group,message_id,regex_download,regex_rename,folder_download):
    try:
        status, message_bot,group,download_path,file_name,caption = await controllers.telegram.downloadFile(group,message_id)
        print(f"[!] >>>>>>> downloadFile [{status}],[{message_bot}],[{group}],[{download_path}],[{file_name}],[{caption}]" ,flush=True)
    
        new_name = regexRename(group,file_name,caption,regex_download,regex_rename,True)
        print(f"[!] >>>>>>> downloadFile regex_download [{regex_download}]" ,flush=True)
        print(f"[!] >>>>>>> downloadFile regex_rename [{regex_rename}]" ,flush=True)
        print(f"[!] >>>>>>> downloadFile folder_download [{folder_download}]" ,flush=True)
        print(f"[!] >>>>>>> downloadFile new_name [{new_name}]" ,flush=True)


        status, download_final_path = await moveFile(new_name, download_path, folder_download)

        if status:
            print(f"[!] >>>>>>> downloadFile download_final_path [{download_final_path}]" ,flush=True)

            newDatabase = Database()

            rest = newDatabase.saveData(group, message_id, new_name, file_name, caption, regex_download, regex_rename, folder_download, download_final_path, status)
            print(f" [*] successfully update status download file: [{group}][{message_id}] [{rest}]", flush=True)

        return status


    except Exception as e:
        print(f"[!] >>>>>>> except downloadFile [{e}]" ,flush=True)
        return False


async def moveFile(filename, temp_file_path, folder_download):
    
    if not folder_download: folder_download = DOWNLOAD_COMPLETED

    print(f"[!] >>>>>>> moveFile filename [{filename}]" ,flush=True)
    print(f"[!] >>>>>>> moveFile temp_file_path [{temp_file_path}]" ,flush=True)
    print(f"[!] >>>>>>> moveFile folder_download [{folder_download}]" ,flush=True)


    try:
        os.makedirs(folder_download, exist_ok=True)
        final_file_path = os.path.join(folder_download,filename)

        if not os.path.exists(final_file_path):
            shutil.move(temp_file_path, final_file_path)

        os.chown(final_file_path, int(PUID), int(PGID))
        os.chmod(final_file_path, 0o666)

        return True, final_file_path
    except Exception as e:
        print(f" [!!!] Exception telegram moveFile_temp [{e}]", flush=True)    # the exception instance
        return False, temp_file_path
