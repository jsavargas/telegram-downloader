import os
import re
import time
import sqlite3
import asyncio

import controllers.telegram


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

def regexRename(group, file_name,caption=None,regex_download=None,regex_rename=None):
    rename = file_name

    try:
        #print(f" regexRename:: [{group}], [{file_name}], [{caption}] [{regex_download}] [{regex_rename}]")

        if re.match(regex_download, file_name, flags=re.I):
            mrr = re.match('/(.*)/(.*)/', regex_rename, flags=re.I)
            if mrr:
                rename = re.sub(mrr.group(1), mrr.group(2), file_name, flags=re.I)

        elif re.match(regex_download, caption, flags=re.I):
            mrr = re.match('/(.*)/(.*)/', regex_rename)
            if mrr:
                rename = re.sub(mrr.group(1), mrr.group(2), caption.replace("\n", ""), flags=re.I)

        elif file_name: 
            rename = file_name
        else: 
            rename = caption

        return rename

    except Exception as e:
        print(f" regexRename Exception:: {e}")


async def downloadFile(group,message_id,regex_download,regex_rename,folder_download):
    try:
        status, message_bot,group,download_path,file_name,caption = await controllers.telegram.downloadFile(group,message_id)
        print(f"[!] >>>>>>> downloadFile [{status}],[{message_bot}],[{group}],[{download_path}],[{file_name}],[{caption}]" ,flush=True)
    
        new_name = regexRename(group,file_name,caption,regex_download,regex_rename)
        print(f"[!] >>>>>>> downloadFile regex_download [{regex_download}]" ,flush=True)
        print(f"[!] >>>>>>> downloadFile regex_rename [{regex_rename}]" ,flush=True)
        print(f"[!] >>>>>>> downloadFile folder_download [{folder_download}]" ,flush=True)
        print(f"[!] >>>>>>> downloadFile new_name [{new_name}]" ,flush=True)





    except Exception as e:
        print(f"[!] >>>>>>> except downloadFile [{e}]" ,flush=True)
        return False
