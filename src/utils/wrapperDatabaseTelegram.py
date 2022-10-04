from utils.database import Database, Data, Object
from utils.utils import UTILS
import utils.telegramDownload as tgd


class WrapperDatabaseTelegram:

    def __init__(self):

        self.DATABASE = '/config/database.db'
        self.limit = 30
        self.init = None


    async def getHistory(self, group=None, update=False):

        print(f" [*] getHistory group => [{group}]",flush=True)
        print(f" [*] getHistory update => [{update}]",flush=True)

        try:
            newDatabase = Database()
            utils = UTILS()
            if update: 
                await self.updateDatabase(group)
            data = newDatabase.getHistory(group)
            configGroups = newDatabase.getConfigGroup(group)
            
            print(f" [*] getHistory d.file_size => [--]",flush=True)
            newdata = []
            for d in data:

                print(f" [*] getHistory d.id => [{d.id}]",flush=True)
                print(f" [*] getHistory d.group => [{d.group}]",flush=True)
                print(f" [*] getHistory d.file_name => [{d.file_name}]",flush=True)
                print(f" [*] getHistory d.date => [{d.date}]",flush=True)
                print(f" [*] getHistory d.id => [{d.id}]",flush=True)
                print(f" [*] getHistory d.id => [{d.id}]",flush=True)
                print(f" [*] getHistory a d.id => [{d.id}]",flush=True)
                print(f" [*] getHistory d.file_size => [{d.file_size}]",flush=True)
                print(f" [*] getHistory f d.id => [{d.id}]",flush=True)

                newObject = {}
                newObject['id']          = d.id 
                newObject['group']       = d.group
                newObject['regex']       = utils.isDownloader(group,d.file_name,d.caption) if utils.isDownloader(group,d.file_name,d.caption) else ''
                newObject['save_name']   = d.regex_name 
                newObject['regex_name']  = utils.getFileRename(group,d.file_name,d.caption)[0] if utils.isDownloader(group,d.file_name,d.caption) else ''
                newObject['date']        = d.date
                newObject['file_name']   = d.file_name
                newObject['caption']     = d.caption
                newObject['width']       = d.width
                newObject['file_size']   = utils.human_readable_size(d.file_size)
                newObject['status']      = True if d.status else ''

                newObject['regex_download']     = True
                newObject['regex_rename']       = utils.getFileRename(group,d.file_name,d.caption)[0] if utils.isDownloader(group,d.file_name,d.caption) else ''

                newdata.append(newObject)

            return newdata
        except Exception as e:
            print('[!] WRAPPER Exception getHistory',e,flush=True)

    async def updateDatabase(self, group, limit=50, init=None):

        try:
            
            _limit = limit if limit else self.limit
            _init = init if init else self.init

            data = await tgd.get_chat_history(group,limit=limit, init=init)
            self.telegramtoData(data,group)

            return True
        except Exception as e:
            print('[!] Exception updateDatabase',e,flush=True)
            return False

    def telegramtoData(self, data, group):
        newDatabase = Database()
        
        newdata = []
        for d in data:
            try:
                #print(f' [*] telegramtoData  => [{d}]',flush=True)
                filename = ""
                file_size = ""

                if str(d.media) == "MessageMediaType.VIDEO":
                    filename = d.video.file_name
                    file_size = d.video.file_size
                if str(d.media) == "MessageMediaType.DOCUMENT":
                    filename = d.document.file_name
                    file_size = d.document.file_size

                print(f' [*] telegramtoData media => [{filename}]',flush=True)
                print(f' [*] telegramtoData document.file_size => [{file_size}]',flush=True)

                newObject = Object()
                newObject.group = group
                newObject.regex = ""
                newObject.regex_name = ""
                newObject.id = d.id
                newObject.date = d.date
                newObject.file_name = filename
                newObject.caption = d.caption
                newObject.width = f"{d.video.width}x{d.video.height}" if str(d.media)=="MessageMediaType.VIDEO" else ""
                newObject.file_size = file_size
                newObject.status = ""

                print(f' [*] telegramtoData newObject.file_name  => [{newObject.file_name}]',flush=True)

                #TODO:  AGREGAR 
                '''
                        print(f" >>>>>>> [{message.id}]" ,flush=True)
                        print(f" >>>>>>> [{message.media}]" ,flush=True)
                        print(f" >>>>>>> [{message.document.file_name}]" ,flush=True)
                        print(f" >>>>>>> [{message.document.mime_type}]" ,flush=True)
                        print(f" >>>>>>> [{message.document.file_size}]" ,flush=True)
                        print(f" >>>>>>> [{message.document.date}]" ,flush=True)
                        print(f" >>>>>>> [{message.date}]" ,flush=True)

                '''

                newdata.append(newObject)

                newDatabase.saveData(newObject)

                print(f" >>>>>>> telegramtoData file_size [{newObject.file_size}]", flush=True)
            except Exception as e:
                print(
                    f" >>>>>>> telegramtoData error in insert operation [{e}]", flush=True)

        return newdata
