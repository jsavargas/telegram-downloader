from pysondb import getDb


todo_db = getDb('dbDownload.json')


def getDownloaderDB():
    try:

        return todo_db.getAll()
        #return todo_db.get()
    
    except Exception as e:
        print(f"[!] >>>>>>> except getDownloaderDB [{e}]" ,flush=True)
        return False

def checkDownloader(group, message_id):
    try:

        q = {"group": group, "message_id": message_id}
        dbDatas = todo_db.getByQuery(query=q)

        if dbDatas:
            print(f"[!] True dbDatas >>>>>>> except checkDownloader [{dbDatas}]" ,flush=True)
            return True
        else:
            return False
            print(f"[!] False dbDatas >>>>>>> except checkDownloader [{dbDatas}]" ,flush=True)

    except Exception as e:
        print(f"[!] >>>>>>> except getDownloaderDB [{e}]" ,flush=True)
        return False

def addDownloader(group, message_id):
    try:
        if not checkDownloader(group, message_id):
            todo_db.add({"group": group, "message_id": message_id})
    
    except Exception as e:
        print(f"[!] >>>>>>> except addDownloader [{e}]" ,flush=True)
        return False

def deletedDownloader(group, message_id):
    try:

        q = {"group": group, "message_id": message_id}
        dbDatas = todo_db.getByQuery(query=q)
        
        for dbData in dbDatas:
            is_deleted = todo_db.deleteById(pk=dbData['id'])
            print(dbData, is_deleted, flush=True)
    
    except Exception as e:
        print(f"[!] >>>>>>> except deletedDownloader [{e}]" ,flush=True)
        return False
