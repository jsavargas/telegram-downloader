'''

encargado de descargar en un solo comando
encargado de buscar y antualizar en un solo comando

wrapper entre  telegram y la base de datos

'''
import os
import re


from utils.database import Database
import utils.telegramDownload as tgd

class UTILS:

    def __init__(self):

        self.DATABASE = '/config/database.db'
        self.CONFIG_PATH = '/config'
        self.DOWNLOAD_PATH = '/download'

        self.limit = 30
        self.init = None

    async def getHistory(self, group=None, update=False):
        try:
            newDatabase = Database()
            if update: 
                await self.updateDatabase(group)
            data = newDatabase.getHistory(group)
            configGroups = newDatabase.getConfigGroup(group)
            
            newdata = []
            for d in data:
                newObject = {}
                newObject['id']          = d.id 
                newObject['group']       = d.group
                newObject['regex']       = self.isDownloader(group,d.file_name,d.caption) if self.isDownloader(group,d.file_name,d.caption) else ''
                newObject['save_name']   = d.regex_name 
                newObject['regex_name']  = self.getFileRename(group,d.file_name,d.caption)[0] if self.isDownloader(group,d.file_name,d.caption) else ''
                newObject['date']        = d.date
                newObject['file_name']   = d.file_name
                newObject['caption']     = d.caption
                newObject['width']       = d.width
                newObject['file_size']   = self.human_readable_size(d.file_size)
                newObject['status']      = True if d.status else ''

                newObject['regex_download']     = True
                newObject['regex_rename']       = self.getFileRename(group,d.file_name,d.caption)[0] if self.isDownloader(group,d.file_name,d.caption) else ''

                newdata.append(newObject)

            return newdata
        except Exception as e:
            print('[!] Exception human_readable_size',e,flush=True)







    def isDownloader(self, group, file_name, caption):

        try:
            newDatabase = Database()
            
            configGroups = newDatabase.getConfigGroup(group)
            filename = file_name if file_name else caption
            for configGroup in configGroups:
                if re.match(configGroup['regex_download'], filename,re.I):
                    return True

            return False

        except Exception as e:
            print(f" >>>>>>> Exception getFileRename_temp [{e}]" ,flush=True)
            return False

    def getFileRename(self, group, file_name, caption):

        try:
            newDatabase = Database()
            
            temp_file_path = os.path.join(self.DOWNLOAD_PATH,'temp',file_name)
            final_file_path = os.path.join(self.DOWNLOAD_PATH,file_name)

            filename_rename = file_name if file_name else caption

            configGroups = newDatabase.getConfigGroup(group)
            for configGroup in configGroups:
                mrr = re.match('/(.*)/(.*)/', configGroup['regex_rename'])
                if mrr:
                    if not re.match(mrr.group(1), file_name):
                        file_name = caption
                        #continue
                    filename_rename = re.sub(mrr.group(1), mrr.group(2), file_name, flags=re.I)
                    final_file_path = os.path.join(self.DOWNLOAD_PATH,filename_rename)
                    if configGroup['folder_download']:
                        final_file_path = os.path.join(configGroup['folder_download'],filename_rename)

                    return filename_rename,temp_file_path, final_file_path
                else:    
                    return filename_rename,temp_file_path, final_file_path
            
            return filename_rename,temp_file_path, final_file_path

        except Exception as e:
            print(f" >>>>>>> Exception getFileRename_temp [{e}]" ,flush=True)
            return temp_file_path, temp_file_path


    async def updateDatabase(self, group, limit=50, init=None):

        try:
            newDatabase = Database()
            
            _limit = limit if limit else self.limit
            _init = init if init else self.init

            data = await tgd.get_chat_history(group,limit=limit, init=init)
            newDatabase.telegramtoData(data,group)

            return True
        except Exception as e:
            print('[!] Exception updateDatabase',e,flush=True)
            return False



    def human_readable_size(self, size, decimal_places=2):
        try:
            size = int(size)
            for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
                if size < 1024.0 or unit == "PiB":
                    break
                size /= 1024.0
            return f"{size:.{decimal_places}f} {unit}"
        except Exception as e:
            print('[!] Exception human_readable_size',e,flush=True)


    def ifDIgit(self, channel):
        channel = str(channel)
        if channel.startswith('-100') or channel.startswith('-'):
            channel = channel.replace("-100", "-")
            channel = channel.replace("-", "-100")

        return int(channel) if any(map(str.isdigit,channel)) else channel


    def getFilename(self, message):
        filename = ""
        file_size = ""
        if str(message.media) == "MessageMediaType.VIDEO":
            filename = message.video.file_name
            file_size = message.video.file_size
        if str(message.media) == "MessageMediaType.DOCUMENT":
            filename = message.document.file_name
            file_size = message.document.file_size
        return filename

    def getFilesize(self, message):
        filename = ""
        file_size = ""
        if str(message.media) == "MessageMediaType.VIDEO":
            filename = message.video.file_name
            file_size = message.video.file_size
        if str(message.media) == "MessageMediaType.DOCUMENT":
            filename = message.document.file_name
            file_size = message.document.file_size
        return file_size

