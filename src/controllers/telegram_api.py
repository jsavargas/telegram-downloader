from pyrogram import Client,idle,handlers
from pyrogram.handlers.handler import Handler
from pyrogram.raw import functions
from pyrogram.raw.functions.messages.get_all_chats import GetAllChats



import io
import json
import os
import re
import shutil
import time
import pickle
from concurrent.futures import ThreadPoolExecutor
import asyncio

#Client(os.path.join(self.config_dir,"lala"), api_id=self.app_id, api_hash=self.api_hash)
from controllers.configs import *
from controllers.jsonDB import jsonDB
from controllers.database import Database, Object

class telegram_api:

    def __init__(self):
        self._version = "1.10.0"
        self.app_id = API_ID
        self.api_hash = API_HASH
        self.bot_token = API_TOKEN
        self.progress = False
        self.config_dir = "/config"
        self.account = "my_account"
        self.dictionary_dir = os.path.join(self.config_dir,'dictionary')
        self.session = os.path.join(self.config_dir,'my_account')
        self.download = "/download"
        self.incompleted = "incompleted"
        self.completed = "completed"
        self.lockfile = f"{os.path.join(self.config_dir,self.account)}.session-journal"
        self.DOWNLOAD_INCOMPLETED = os.getenv('DOWNLOAD_INCOMPLETED') or os.path.join(self.download,self.incompleted)
        self.DOWNLOAD_COMPLETED = os.getenv('DOWNLOAD_COMPLETED') or os.path.join(self.download,self.completed)
        self.PUID = os.environ.get("PUID") or None
        self.PGID = os.environ.get("PGID") or None 
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.json_db = jsonDB()


    def ifDIgit(self, channel):
        channel = str(channel)
        if channel.isnumeric():
            channel = f"-100{channel}"
        else:
            channel = channel.lower()
        return int(channel) if channel.isnumeric() else channel

    def getChatDictionary(self, dictionary_file = 'chats'):
        os.makedirs(self.dictionary_dir, exist_ok=True)
        dictionary_path = os.path.join(self.dictionary_dir,f'{dictionary_file}.dictionary')
        if os.path.exists(dictionary_path):
            if (time.time() - os.stat(dictionary_path).st_mtime) > 300: return False
            with open(dictionary_path, 'rb') as config_dictionary_file:
                print(f" [!] getDictionary >> [{dictionary_file}] >>> [{config_dictionary_file}]", flush=True)
                return pickle.load(config_dictionary_file)
        print(f" [!] getDictionary >> [False] [{dictionary_file}]", flush=True)
        return False

    def setChatDictionary(self, dictionary, dictionary_file = 'chats'):
        dictionary_path = os.path.join(self.dictionary_dir,f'{dictionary_file}.dictionary')
        print(f" [!] setDictionary >> [{dictionary_file}]", flush=True)
        with open(dictionary_path, 'wb') as config_dictionary_file:
            pickle.dump(dictionary, config_dictionary_file)
        return dictionary

    async def getAllChats(self, account = None):
        basepath = account or self.account
        print(f"[!] >>>> getAllChats [{account}]" ,flush=True)
        try:
            getAllChats = self.getChatDictionary(dictionary_file='getAllChats')
            if getAllChats:
                return getAllChats

            #my_account.session-journal
            while os.path.isfile(self.lockfile):
                print("Otra instancia de Pyrogram ya está activa. Esperando...",flush=True)
                time.sleep(3)
            
            async with Client(os.path.join(self.config_dir,self.account), api_id=self.app_id, api_hash=self.api_hash) as app:
                chats = []
                AllChats = await app.invoke(GetAllChats(except_ids=[]))
                for chat in AllChats.chats:
                    chats.append({
                        "id": chat.id,
                        "title": chat.title,
                        "username": chat.username if getattr(chat, 'username',None) else chat.id,
                    })
                self.setChatDictionary(chats,dictionary_file='getAllChats')
                return chats
        except Exception as e:
            print(f"[!] >>>>>>> except GetAllChats [{e}]" ,flush=True)

    async def get_chat_history(self, group='me',limit=100, init=None):
        data = []

        try:
            print(f"[!] 1 >>>>>>> get_chat_history group:[{group}] limit:[{limit}]" ,flush=True)

            get_chat_history = self.getChatDictionary(dictionary_file=group)
            if not init and get_chat_history:
                return get_chat_history

            while os.path.isfile(self.lockfile):
                print("Otra instancia de Pyrogram ya está activa. Esperando...",flush=True)
                time.sleep(3)

            print(f"[!] 1 >>>>>>> jonas [{get_chat_history}] group:[{group}] limit:[{limit}]" ,flush=True)
            async with Client(os.path.join(self.config_dir,self.account), api_id=self.app_id, api_hash=self.api_hash) as app:


                print(f"[!] 2 >>>>>>> app.get_chat " ,flush=True)
                
                if not init:
                    async for message in app.get_chat_history(self.ifDIgit(group),limit=limit):
                        if str(message.media) == "MessageMediaType.VIDEO":
                            dtemp = {
                                'id': message.id,
                                'file_name' : message.video.file_name,
                                'file_size' : message.video.file_size,
                                'width'     : message.video.width,
                                'height'    : message.video.height,
                                'caption'   : message.caption,
                                'date'      : message.date,
                                'message'   : message,
                            }
                            data.append(dtemp)
                        if str(message.media) == "MessageMediaType.DOCUMENT":
                            dtemp = {
                                'id': message.id,
                                'file_name' : message.document.file_name,
                                'file_size' : message.document.file_size,
                                'width'     : '',
                                'height'    : '',
                                'caption'   : message.caption,
                                'date'      : message.date,
                                'message'   : message,
                            }
                            data.append(dtemp)
                else:
                    #list = intToArray(init,limit)
                    messages = await app.get_messages(self.ifDIgit(group),range(50, 100))
                    for message in messages:
                        if str(message.media) == "MessageMediaType.VIDEO":
                            dtemp = {
                                'id': message.id,
                                'file_name' : message.video.file_name,
                                'file_size' : message.video.file_size,
                                'width'     : message.video.width,
                                'height'    : message.video.height,
                                'caption'   : message.caption,
                                'date'      : message.date,
                                'message'   : message,
                            }
                            data.append(dtemp)
                        if str(message.media) == "MessageMediaType.DOCUMENT":
                            dtemp = {
                                'id': message.id,
                                'file_name' : message.document.file_name,
                                'file_size' : message.document.file_size,
                                'width'     : '',
                                'height'    : '',
                                'caption'   : message.caption,
                                'date'      : message.date,
                                'message'   : message,
                            }
                            data.append(dtemp)
                    id=None
        except Exception as e:
            print(f"[!] >>>>>>> except get_chat_history [{e}]" ,flush=True)

            return data
        self.setChatDictionary(data,dictionary_file=group)
        return data


    def wrapper(self, coro):
        return asyncio.run(coro)

    def downloadFile(self, group, message_id, force=False):
        regex_download  = ""
        regex_rename    = ""
        folder_download = ""

        database = Database()
        config = database.getConfigGroup2(group)  

        print(f"[!][!][!][!] >>>>>>> downloadFile [{group}][{message_id}] [{config}]" ,flush=True)

        if self.json_db.checkDownloader(group, message_id): 
            return 'continue'
        
        q = {"group": group, "message_id": message_id, 'file_size': None, 'progress':None }
        self.json_db.addDownloader(q)

        arglist = ((group,message_id,config,force), )
        down = [self.downloadFileTemp(_group,_message_id,_config,force) for _group,_message_id,_config,force in arglist]
        
        print("Start", time.ctime(), flush=True)
        for r in self.executor.map(self.wrapper, down):
            print(f"{r}, {time.ctime()}", flush=True)
            self.json_db.deletedDownloader(group, message_id)
            return r['status']
        
        self.json_db.deletedDownloader(group, message_id)
        return 'False'

    

    async def downloadFileTemp(self, group, message_id, config={}, force=False):
        # status, message_bot,group,download_path,file_name,caption
        try:
            pass

            print(f"[!][!][!][!] >>>>>>> downloadFileTemp [{group}][{message_id}] [{config}]" ,flush=True)

            while os.path.isfile(self.lockfile):
                print("Otra instancia de Pyrogram ya está activa. Esperando...",flush=True)
                time.sleep(3)

            async with Client(self.session, api_id=self.app_id, api_hash=self.api_hash) as app:
                f = await app.get_messages(self.ifDIgit(group),[int(message_id)])
                for message in f:
                    print(f"[!] >>>>>>> downloadFileTemp file_name [{message.video.file_name}]" ,flush=True)

                    if str(message.media) == "MessageMediaType.VIDEO":
                        if message.video.file_name:
                            file_name = message.video.file_name
                        else:
                            file_name = None
                        if message.caption:
                            caption = message.caption
                        else:
                            caption = None

                        in_message = {'file_name':file_name,'caption':caption}
                        new_rename = self.regexRename(group,in_message,config)

                        
                        folder_download = new_rename['folder_download'] or self.DOWNLOAD_COMPLETED
                        print(f"[!] >>>>>>> downloadFileTemp new_rename [{new_rename}]" ,flush=True)
                        print(f"[!] >>>>>>> downloadFileTemp folder_download [{folder_download}]" ,flush=True)
                        print(f"[!] >>>>>>> downloadFileTemp file_name [{file_name}]" ,flush=True)
                        print(f"[!] >>>>>>> downloadFileTemp caption [{caption}]" ,flush=True)

                        temp_file_path = file_name or caption or f"{group}-{message.id}"
                        print(f"[!] >>>>>>> downloadFileTemp temp_file_path [{temp_file_path}]" ,flush=True)
                        final_path = os.path.join(folder_download,new_rename['rename'])
                        
                        text = f"download file id: {message.id}\n"
                        text += f" => {file_name}\n"
                        text += f" => {caption}\n"
                        text += f" {temp_file_path} to: {final_path}, {self.sizeof_fmt(message.video.file_size)}"

                        download_path = os.path.join(self.DOWNLOAD_INCOMPLETED,temp_file_path)
                        print(f"[!] >>>>>>> downloadFileTemp rename [{text}]" ,flush=True)
                        print(f"[!] >>>>>>> downloadFileTemp download_path [{download_path}]" ,flush=True)
                        print(f"[!] >>>>>>> downloadFileTemp new_rename \n\n\n\n" ,flush=True)


                        #TODO if regexDownload
                        message_bot = None  
                        if True or not os.path.exists(download_path):
                            result = await app.download_media(message, file_name=download_path, progress=self.progress_task, progress_args=[message_bot,text,group,message_id])
                            print(f"[!] >>>>>>> downloadFileTemp download_media [{result}]" ,flush=True)
                            re_move = self.moveFile(result,final_path)
                            if result and re_move:
                                return {
                                    'status'    :True,
                                    'group'     :group,
                                    'message_id':message_id,
                                    'source_path':result,
                                    'dest_path':final_path,
                                    'config'    :config
                                }
            return {
                'status'    :False,
                'group'     :group,
                'message_id':message_id,
                'config'    :config
            }
        except Exception as e:
            print(f"[!] >>>>>>> except downloadFile [{e}]" ,flush=True)
            return {
                'status'        : False,
                'message_bot'   :'message_bot',
                'group'         :group,
                'message_id'    :message_id,
                'config'        :config
            }


        print(f"[!][!][!][!] >>>>>>> downloadFile message [{group}][{message_id}]" ,flush=True)
        try:
            while os.path.isfile(self.lockfile):
                print("Otra instancia de Pyrogram ya está activa. Esperando...",flush=True)
                time.sleep(3)

            async with Client(os.path.join(self.config_dir,self.account), api_id=self.app_id, api_hash=self.api_hash) as app:

                f = await app.get_messages(self.ifDIgit(group),[int(message_id)])
                for message in f:
                    #print(f"[!] >>>>>>> downloadFile message [{message}]" ,flush=True)
                    if str(message.media) == "MessageMediaType.VIDEO":
                        if message.video.file_name:
                            file_name = message.video.file_name
                            temp_file_path = message.video.file_name
                        else:
                            temp_file_path = f"{group}-{message.id}"
                        text = f"downloadind file in: {temp_file_path}, {self.sizeof_fmt(message.video.file_size)}"
                    if str(message.media) == "MessageMediaType.DOCUMENT":
                        if message.document.file_name:
                            file_name = message.document.file_name
                            temp_file_path = message.document.file_name
                        else:
                            temp_file_path = f"{group}-{message.id}"
                        text = f"downloadind file in: {temp_file_path}, {self.sizeof_fmt(message.document.file_size)}"

                    message_bot = None
                    download_path = os.path.join(self.DOWNLOAD_INCOMPLETED,temp_file_path)
                    download_path = os.path.join(self.temp_file_path)

                    if not os.path.exists(download_path):
                        await app.download_media(message, file_name=download_path, progress=self.progress, progress_args=[message_bot,text,group,message_id])
                    
                    return {
                        'status'        : True,
                        'message_bot'   :message_bot,
                        'group'         :group,
                        'download_path' :download_path,
                        'file_name'     :file_name,
                        'caption'       :message.caption,
                    }
                    return True, message_bot, group, download_path, file_name, message.caption

        except Exception as e:
            print(f"[!] >>>>>>> except downloadFile [{e}]" ,flush=True)
            return {
                'status'        : False,
                'message_bot'   :message_bot,
                'group'         :group,
                'download_path' :download_path,
                'file_name'     :file_name,
                'caption'       :message.caption,
            }
            return False, message_bot, group, download_path, file_name, message.caption

    





    #def regexRename(self, group, file_name,caption=None,regex_download='',regex_rename='',force=False):
    def regexRename(self, group, message, config):
        rename = ''
        regex_download = False
        folder_download = None

        try:
            for conf in config:
                #print(f" regexRename:: [{group}], [{file_name}], [{caption}] [{regex_download}] [{regex_rename}]")
                print(f" regexRename:: [{message}], [{conf}]")
                if re.match(conf['regex_download'], message['file_name'], flags=re.I):
                    regex_download = True
                    mrr = re.match('/(.*)/(.*)/', conf['regex_rename'], flags=re.I)
                    if mrr:
                        rename = re.sub(mrr.group(1), mrr.group(2), message['file_name'], flags=re.I)
                    else:
                        rename = message['file_name']
                elif re.match(conf['regex_download'], message['caption'], flags=re.I):
                    regex_download = True
                    mrr = re.match('/(.*)/(.*)/', conf['regex_rename'])
                    if mrr:
                        rename = re.sub(mrr.group(1), mrr.group(2), message['caption'].replace("\n", ""), flags=re.I)
                    else:
                        rename = message['caption']

                if not regex_download and message['file_name']:
                    mrr = re.match('/(.*)/(.*)/', conf['regex_rename'])
                    mr2 = re.match(mrr.group(1), message['file_name'], flags=re.I)
                    if mr2:
                        rename = re.sub(mrr.group(1), mrr.group(2), message['file_name'], flags=re.I)
                if not rename and message['caption']:
                    mrr = re.match('/(.*)/(.*)/', conf['regex_rename'])
                    mr2 = re.match(mrr.group(1), message['caption'], flags=re.I)
                    if mr2: rename = re.sub(mrr.group(1), mrr.group(2), message['caption'].replace("\n", ""), flags=re.I)
                folder_download = conf['folder_download']
                if rename :
                    return {
                        'regex_download'    :regex_download,
                        'rename'            :rename,
                        'folder_download'   :folder_download }
                
            if not rename:
                print(f" regexRename :: not rename [{message}], []")
                rename = message['file_name'] or message['caption'].replace("\n", "")
                print(f" regexRename :: not rename [{rename}], []")

            return {
                'regex_download'    :regex_download,
                'rename'            :rename,
                'folder_download'   :folder_download }
        
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

    def moveFile(self, source_path, dest_path):
        
        parent_folder = os.path.dirname(dest_path)

        print(f"[!] >>>>>>> moveFile source_path [{source_path}]" ,flush=True)
        print(f"[!] >>>>>>> moveFile dest_path [{dest_path}]" ,flush=True)

        try:
            os.makedirs(parent_folder, exist_ok=True)
            if not os.path.exists(dest_path):
                shutil.move(source_path, dest_path.strip())
                self.set_file_permissions(dest_path.strip())
                return {'status': True, 'dest_path': dest_path}
            return {'status': False, 'dest_path': dest_path}
        except Exception as e:
            print(f" [!!!] Exception telegram moveFile_temp [{e}]", flush=True)    # the exception instance
            return {'status': False, 'dest_path': dest_path}

    def set_file_permissions(self, file_path):
        # Obtener los valores de PUID y PGID desde las variables de entorno
        puid = os.environ.get("PUID")
        pgid = os.environ.get("PGID")

        # Verificar si las variables de entorno existen
        if not puid or not pgid:
            raise Exception("Las variables de entorno PUID y PGID no están definidas.")

        # Convertir los valores de PUID y PGID a enteros
        puid = int(puid)
        pgid = int(pgid)

        # Cambiar los permisos del archivo
        os.chown(file_path, puid, pgid)
        os.chmod(file_path, 0o660)  # permisos rw-rw----

        # Cambiar los permisos de la carpeta contenedora
        parent_folder = os.path.dirname(file_path)
        os.chown(parent_folder, puid, pgid)
        os.chmod(parent_folder, 0o770)  # permisos rwxrwx---

        print(f"Los permisos del archivo {file_path} y su carpeta contenedora se han cambiado a {puid}:{pgid} con permisos rw-rw---- (lectura/escritura para usuario y grupo).")



    # Keep track of the progress while downloading
    async def progress_task(self, current, total, *args):
        try:

            value = (current / total) * 100
            format_float = "{:.2f}".format(value)
            int_value = int(float(format_float) // 1)
            if ((int_value != 100 ) and (int_value % 2 == 0)):
                #print(f" progress {current}, {total}",  flush=True)
                current = self.sizeof_fmt(current)
                total = self.sizeof_fmt(total)
                print(f" progress {current}, {total}",  flush=True)
                self.json_db.updated_data(args[2], args[3], current, total)
        except Exception as e:
            print(f"[!] >>>>>>> except progress [{e}]" ,flush=True)

    def sizeof_fmt(self, num, suffix="B"):
        for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
            if abs(num) < 1024.0:
                return f"{num:3.2f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Yi{suffix}"

