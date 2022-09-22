import os
import pickle
import re
import pdb, asyncio, json
import sys
import argparse
import time


from tabulate import tabulate

from utils.database import Database
from utils.utils import UTILS
import utils.telegramDownload

OWNER = os.environ['OWNER']
APP_ID = int(os.environ['APP_ID'])
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']
PUID = os.environ['PUID']
PGID = os.environ['PGID']


__version__ = "VERSION 0.0.1"
_INIT = utils.config._INIT
_LIMIT = 20


def parse_args():
    parser = argparse.ArgumentParser(description="MKV Tools - Delete Spam.")
    parser.add_argument('-v','--version', action='version', version="%(prog)s " + __version__)

                    
    parser.add_argument('-g', '--group', type=str, required=True, help='group to process')
    parser.add_argument('-i', '--init', type=str, default=_INIT, required=False, help='init')
    parser.add_argument('-l', '--limit', type=int, default=_LIMIT, required=False, help='limit to list')
    parser.add_argument('-u', '--update', action='store_true', help='force update list')
 

    parser.add_argument('--groups', action='store_true', help='get groups on db')
    parser.add_argument('-d', '--download', action='store_true', help='download files')
    
    args = parser.parse_args()
    return args





async def main(args):

    if args.group: 
        return await group(args)
    if args.groups: 
        return await getGroups(args)



async def getGroups(args):
    try:

        newDatabase = Database()
        data = newDatabase.getGroups()

        count = 0

        t_data = []
        for row in data:
            #if count >= args.limit: break
            count +=1
            t_data.append([count, row])
        print(tabulate(t_data, headers=[ 'ID', 'Group' ], tablefmt='pretty',stralign='left'))

        return ""
    except Exception as e:
        print('__name__',e,flush=True)


async def group(args):

    try:
        group = 'traicionada_mega'
        group = 'laleydebaltazar'
        group = None
        group = 'hastaencontrarte'

        newDatabase = Database()
        newUTILS = UTILS()
        data = await newUTILS.getHistory(args.group,args.update)

        count = 0

        configGroups = newDatabase.getConfigGroup(args.group)
        if configGroups:
            _regex_download     = configGroups[0]['regex_download']
            _regex_rename       = configGroups[0]['regex_rename']
            _folder_download    = configGroups[0]['folder_download']

        print(f' [*] folder_download  => [{_folder_download}]',flush=True)
        print(f' [*] regex_download   => [{_regex_download}]',flush=True)
        print(f' [*] regex_rename     => [{_regex_rename}]',flush=True)
        print("")

        t_data = []
        for row in data:
            if count >= args.limit: break
            count +=1
            #print(f" >>>>>>> history [{row['group']}]" ,flush=True)
            t_data.append([row['id'], row['group'], row['status'], row['regex'], row['save_name'], row['regex_rename'], row['file_name'], row['caption'], row['width'], row['file_size']])

        print(tabulate(t_data, headers=[ 'ID', 'Group', 'Finish','Enabled','Save Name', 'Regex Name', 'File Name', 'Caption','width', 'file_size'], tablefmt='pretty',stralign='left'))

        print("")
        print("")

        count = 0
        if args.download:
            
            wait(10)

            for row in data:
                if count >= args.limit: break
                count +=1
                if not row['status'] and row['regex']:
                    print(f" [*] DOWNLOADING [{row['id']}] [{row['status']}] [{row['regex']}]")

                    downloadFile = True
                    downloadFile = await utils.telegramDownload.downloadFile(args.group,row['id'])

                    if downloadFile: print(f" [*] FINISHED [{row['id']}] [{row['status']}] [{row['regex']}]")

    except Exception as e:
        print('__name__',e,flush=True)
        





def wait(seconds: int = 3):
    """ Pause for a set number of seconds """
    for i in range(seconds)[::-1]:
        print("\rWait for %d second(s)..." % (i + 1), end="")
        time.sleep(1)





if __name__ == "__main__":
    try:

        args = parse_args()
        
        if args: print(f"\n\n{args}\n")

        asyncio.run(main(args))
    except KeyboardInterrupt:
        # quit
        print('')
        sys.exit(0)
    except Exception as error:
        print(f"[!] Missing group telegram, example: python {sys.argv[0]} --group 'groupTelegram' ", flush=True)
        print(f"[!] ERROR {error} ", flush=True)


