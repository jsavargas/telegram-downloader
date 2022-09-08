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
        async with Client("/config/my_account", api_id=APP_ID, api_hash=API_HASH) as app:

            for num in range(1490, 1600):
                print(num)
                try:
                    await app.forward_messages("jsavargas_bot", args.group, num)
                    time.sleep(.7)
                except Exception as e:
                    print('__name__',e,flush=True)
                    continue



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


