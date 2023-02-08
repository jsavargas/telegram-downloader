import os 

from pyrogram import Client

import utils.config

print(f" >>>>>>> APP_ID [{os.environ['APP_ID']}]" ,flush=True)
print(f" >>>>>>> API_HASH [{os.environ['API_HASH']}]" ,flush=True)
print(f" >>>>>>> BOT_TOKEN [{os.environ['BOT_TOKEN']}]" ,flush=True)


APP_ID = int(os.environ['APP_ID'])
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']



if __name__ == "__main__":

    try:
        with Client(f"{utils.config.CLIENT_NAME}", api_id=APP_ID, api_hash=API_HASH) as app:
            #await xbot.send_message(OWNER, OWNER)

            ssession = f'**String Session**:\n - STRING_SESSION={app.export_session_string()}'
            print(f'Your string session has been stored to your saved message => {ssession}')
            app.send_message('me', ssession)
            print('Your string session has been stored to your saved message')

            #me = app.get_chat('me')
            #print(f"[!] >>>>>>> chat.title [{me}]" ,flush=True)


    except Exception as e:
        print(f" >>>>>>> Exception [{e}]" ,flush=True)

