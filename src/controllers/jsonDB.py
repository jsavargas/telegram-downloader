
import os

from pysondb import getDb



class jsonDB:
    def __init__(self):
        self.config_dir = "/config"
        self.db_path = os.path.join(self.config_dir,'dbDownload.json')
        self.todo_db = getDb(self.db_path)

    def getDownloaderDB(self):
        try:
            return self.todo_db.getAll()
            #return self.todo_db.get()
        
        except Exception as e:
            print(f"[!] >>>>>>> except getDownloaderDB [{e}]" ,flush=True)
            return False

    def checkDownloader(self, group, message_id):
        try:

            q = {"group": group, "message_id": message_id}
            dbDatas = self.todo_db.getByQuery(query=q)

            if dbDatas:
                print(f"[!] True checkDownloader [{dbDatas}]" ,flush=True)
                return True
            else:
                return False
                print(f"[!] False checkDownloader [{dbDatas}]" ,flush=True)

        except Exception as e:
            print(f"[!] >>>>>>> except getDownloaderDB [{e}]" ,flush=True)
            return False

    def addDownloader(self, group, message_id):
        try:
            if not self.checkDownloader(group, message_id):
                self.todo_db.add({"group": group, "message_id": message_id})
        
        except Exception as e:
            print(f"[!] >>>>>>> except addDownloader [{e}]" ,flush=True)
            return False

    def deletedDownloader(self, group, message_id):
        try:

            q = {"group": group, "message_id": message_id}
            dbDatas = self.todo_db.getByQuery(query=q)
            
            for dbData in dbDatas:
                is_deleted = self.todo_db.deleteById(pk=dbData['id'])
                print(dbData, is_deleted, flush=True)
        
        except Exception as e:
            print(f"[!] >>>>>>> except deletedDownloader [{e}]" ,flush=True)
            return False
