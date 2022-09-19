import os
import pickle
import re
import pdb, asyncio, json
import sys
import argparse
import time


from pyrogram import Client
from pyrogram.errors import FloodWait
from tabulate import tabulate

import utils.config
import utils.db
import utils.telegram

OWNER = os.environ['OWNER']
APP_ID = int(os.environ['APP_ID'])
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']

PUID = os.environ['PUID']
PGID = os.environ['PGID']


__version__ = "VERSION 0.0.6"
_INIT = utils.config._INIT
_LIMIT = utils.config._LIMIT


def parse_args():
    parser = argparse.ArgumentParser(description="MKV Tools - Delete Spam.")
    parser.add_argument('-v','--version', action='version', version="%(prog)s " + __version__)

                    
    parser.add_argument('-g', '--group', type=str, required=True, help='group to process')
    parser.add_argument('-i', '--init', type=str, default=_INIT, required=False, help='group to process')
    parser.add_argument('-l', '--limit', type=int, default=_LIMIT, required=False, help='group to process')
 
 
    parser.add_argument('-d', '--download', action='store_true', help='download files')
    



    args = parser.parse_args()
    return args


async def main(args):

    try:
        data = []

        _regex_download = utils.config.getRegex_download(args.group)
        _folder_download = utils.config.getDownloadPath(args.group)
        _regex_rename = utils.config.getRegex_rename(args.group)


        DICCIONARY_PATH = utils.config.DICCIONARY_PATH

        file_dict = f"{DICCIONARY_PATH}/dictionary.{args.group}.dict"
        
        #pdb.set_trace()

        if os.path.exists(file_dict) and args.limit == _LIMIT and (time.time() - os.path.getmtime(file_dict) < 10 * 60):
            with open(file_dict, 'rb') as config_dictionary_file:    
                data = pickle.load(config_dictionary_file)
        else:
            data = await utils.telegram.get_chat_history(args.group, init=args.init, limit=args.limit)
            with open(file_dict, 'wb') as config_dictionary_file:
                pickle.dump(data, config_dictionary_file)

        regex, rename = utils.config.getFileRename(data,_regex_download,_regex_rename)
        downloaded = utils.db.getDownloaded(args.group)


        print("*"*90)
        print(f' [*] folder_download  => [{_folder_download}]',flush=True)
        print(f' [*] regex_download   => [{_regex_download}]',flush=True)
        print(f' [*] regex_rename     => [{_regex_rename}]',flush=True)


        print("")

        t_data = []
        for d in data:
            #print(f' file_name [{d.id}]:{d.video.file_name}',flush=True)
            down = True if d.id in downloaded else False
            if regex[d.id]:
                t_data.append([d.id, down, regex[d.id], rename[d.id], d.video.file_name, d.caption])
                #print(f' file_name {down} => [{d.id}]:{regex[d.id]} - [{rename[d.id]}] => [{d.video.file_name}]',flush=True)

        print(tabulate(t_data, headers=[ 'ID', 'Finish','Enabled','New Name', 'File Name', 'Caption'], tablefmt='pretty',stralign='left'))


        print("")
        print("")
        if args.download:
            time.sleep(10) 
            
            for d in data:
                down = True if d.id in downloaded else False
                if regex[d.id] and not down:
                    print(f' [!] Download : [{down}] [{d.video.file_name}] => [{rename[d.id]}]',flush=True)

                    downloading = await utils.telegram.downloadFile(args.group,d.id)

                    if downloading: downloading = utils.db.setDownloaded(args.group,d.id)




    except Exception as e:
        print('__name__',e,flush=True)
        






async def botSend(message,message_bot=None):
    try:
        async with Client("/config/bot", api_id=APP_ID, api_hash=API_HASH,bot_token=BOT_TOKEN) as xbot:
            if message_bot == None: return await xbot.send_message(OWNER, message)
            else: return await xbot.edit_message_text(OWNER, message_id=message_bot.id,text=message)

    except Exception as error:

        print('__name__',error,flush=True)
  




if __name__ == "__main__":
    try:

        args = parse_args()
        
        if args: print(args)

        asyncio.run(main(args))

    except Exception as error:
        print(f"[!] Missing group telegram, example: python {sys.argv[0]} --group 'groupTelegram' ", flush=True)
        print(f"[!] ERROR {error} ", flush=True)


