import os
import time
import pdb, asyncio, json

from pyrogram import Client
from pyrogram.errors import FloodWait
from tabulate import tabulate


OWNER = os.environ['OWNER']
APP_ID = int(os.environ['APP_ID'])
API_HASH = os.environ['API_HASH']



async def test(group='me'):

    data = []

    try:


        async with Client("/config/my_account", api_id=APP_ID, api_hash=API_HASH) as app:
            #await xbot.send_message(OWNER, OWNER)
            #group = 'Traicionada_MEGA'

            chat = await app.get_chat(group)

            print(f"[!] >>>>>>> chat.title [{chat.title}]" ,flush=True)

            async for message in app.get_chat_history(group,limit=30):
                #print(f" >>>>>>> [{message.media}]" ,flush=True)
                if str(message.media) == "MessageMediaType.VIDEO":
                    data.append(message) 


        print(f" >>>>>>> SALIENDO [{data}]" ,flush=True)

    except:
        return data


    return data
    


if __name__ == "__main__":

    print('__name__')
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(test())
