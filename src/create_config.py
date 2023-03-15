import os 

from pyrogram import Client

from controllers.configs import *

print(f" >>>>>>> APP_ID [{APP_ID}]" ,flush=True)
print(f" >>>>>>> API_HASH [{API_HASH}]" ,flush=True)
print(f" >>>>>>> BOT_TOKEN [{BOT_TOKEN}]" ,flush=True)




if __name__ == "__main__":

    try:
        with Client(f"{SESSION}", api_id=APP_ID, api_hash=API_HASH) as app:
            #await xbot.send_message(OWNER, OWNER)

            ssession = f'**String Session**:\n - STRING_SESSION={app.export_session_string()}'
            print(f'Your string session has been stored to your saved message => {ssession}')
            app.send_message('me', ssession)
            print('Your string session has been stored to your saved message')

            #me = app.get_chat('me')
            #print(f"[!] >>>>>>> chat.title [{me}]" ,flush=True)


    except Exception as e:
        print(f" >>>>>>> Exception [{e}]" ,flush=True)

