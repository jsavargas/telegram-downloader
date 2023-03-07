from pyrogram import Client
from pyrogram.raw import functions
from pyrogram.raw.functions.messages.get_all_chats import GetAllChats



import io
import json
import os
import re
import shutil
import time
import pickle


class telegram_api:


    def __init__(self,
                 app_id = '',
                 api_hash = '',
                 bot_token = '',
                 config_dir = "/config",
                 account = "my_account",
                 ):
        self._version = "1.10.0"
        self.app_id = app_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.progress = False
        self.config_dir = config_dir
        self.account = account

    def ifDIgit(self, channel):
        channel = str(channel)
        if channel.isnumeric():
            channel = f"-100{channel}"
        else:
            channel = channel.lower()
        return int(channel) if any(map(str.isdigit,channel)) else channel

    def setChatDictionary(self, dictionary, dictionary_file = 'chats'):
        print(f" [!] setDictionary", flush=True)
        with open(f'{dictionary_file}.dictionary', 'wb') as config_dictionary_file:
            pickle.dump(dictionary, config_dictionary_file)
        return dictionary

    def getChatDictionary(self, dictionary_file = 'chats'):
        print(f" [!] getDictionary", flush=True)
        if os.path.exists(f'{dictionary_file}.dictionary'):
            with open(f'{dictionary_file}.dictionary', 'rb') as config_dictionary_file:
                return pickle.load(config_dictionary_file)

    async def getAllChats(self, account = None):
        basepath = account or self.account
        print(f"[!] >>>> getAllChats [{account}]" ,flush=True)
        try:
            async with Client(os.path.join(self.config_dir,self.account), api_id=self.app_id, api_hash=self.api_hash) as app:
                chats = []
                AllChats = await app.invoke(GetAllChats(except_ids=[]))
                for chat in AllChats.chats:
                    chats.append({
                        "id": chat.id,
                        "title": chat.title,
                        "username": chat.username if getattr(chat, 'username',None) else chat.id,
                    })
                return chats
        except Exception as e:
            print(f"[!] >>>>>>> except GetAllChats [{e}]" ,flush=True)
