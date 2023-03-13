
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

    def addDownloader(self, data):
        try:
            if not self.checkDownloader(data['group'], data['message_id']):
                q = {"group": data['group'], "message_id": data['message_id'], 'file_size': None, 'progress':None }
                self.todo_db.add(q)
        
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

    def updated_data(self, group, message_id, current, total):

        q = {"group": group, "message_id": message_id}
        dbDatas = self.todo_db.getByQuery(query=q)
        """
        [!] >>>>>>> updated_data [[{'group': '1238196432', 
        'message_id': '60', 
        'file_size': None, 
        'progress': None, 
        'id': 249434469424494566}, 
        {'group': '1238196432', 'message_id': '60', 'file_size': None, 'progress': None, 'id': 247018462500810205}]]

        """
        if not dbDatas: return False

        updated_data = {"name": "Book", "quantity": 100}
        updated_data = {'progress':current, 'file_size':total}
        self.todo_db.updateById(pk=dbDatas[0]['id'], new_data=updated_data)
