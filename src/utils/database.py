import sqlite3
import time

class Database:

    def __init__(self):

        self.DATABASE = '/config/database.db'

        conn = sqlite3.connect(self.DATABASE)

        conn.execute("CREATE TABLE IF NOT EXISTS students ('name' TEXT, 'addr' TEXT, 'city' TEXT, 'pin' TEXT)")
        conn.execute("CREATE TABLE IF NOT EXISTS downloader ( 'group' TEXT, 'regex' TEXT, 'regex_name' TEXT, 'id' INTEGER, 'date' TEXT, 'file_name' TEXT, 'caption' TEXT, 'width' TEXT, 'file_size' INTEGER, 'status' TEXT)")
        conn.execute("CREATE TABLE IF NOT EXISTS groups ( ID INTEGER PRIMARY KEY AUTOINCREMENT, 'group' TEXT, 'regex_download' TEXT, 'regex_rename' TEXT, 'folder_download' TEXT, 'status' BOOLEAN )")


        createSecondaryIndex = "CREATE UNIQUE INDEX IF NOT EXISTS index_group_id ON downloader('group','id')"
        conn.execute(createSecondaryIndex)


        conn.close()


    def getHistory(self,group=None):
        conn = sqlite3.connect(self.DATABASE)
        conn.row_factory = sqlite3.Row

        if group==None:
            query = "SELECT * FROM downloader ORDER BY `group`,`id` DESC "
        else:
            query = f"SELECT * FROM downloader where `group` = '{group}' ORDER BY `group`,`id` DESC"

        print(f" >>>>>>> getHistory [{query}]" ,flush=True)

        data = conn.execute(query).fetchall()

        conn.close()

        
        return [studentDef(*row) for row in data]


        return "getHistory"




    def getGroups(self):

        return ["hijosdeldesiertocaps","laleydebaltazarcapitulos",
        "laleydebaltazar","hastaencontrarte","traicionada_mega","laleydebaltazarcl"]

    def getConfigGroup(self,group=None):

        conn = sqlite3.connect(self.DATABASE)
        conn.row_factory = sqlite3.Row

        if group==None:
            query = "SELECT * FROM groups ORDER BY `group`,`id` ASC "
        else:
            query = f"SELECT * FROM groups where `group` = '{group}' ORDER BY `group`,`id` ASC"

        print(f" >>>>>>> getHistory [{query}]" ,flush=True)

        data = conn.execute(query).fetchall()

        conn.close()

        return [row for row in data]
        return [studentDef(*row) for row in data]

    def saveConfigGroup(self,config):

        print(f" >>>>>>> saveConfigGroup [{config}]" ,flush=True)
        print(f" >>>>>>> saveConfigGroup [{config.regex_download}]" ,flush=True)

        try:
            
            sqliteConnection  = sqlite3.connect(self.DATABASE)
            cursor = sqliteConnection.cursor()


            count = cursor.execute("INSERT INTO groups (`group`, 'regex_download', 'regex_rename', 'folder_download', 'status' ) VALUES (?,?,?,?,?)",(config.group, config.regex_download, config.regex_name, config.folder_download, config.status) )
            #count = cursor.execute("INSERT INTO students (name , addr , city , pin  ) VALUES (?,?,?,?)",(str(data.group),data.regex,str(data.regex_name),str(data.id)) )
            #count = cursor.execute("INSERT INTO downloader ('group', 'regex', 'regex_name', 'id'  ) VALUES (?,?,?,?)",(str(data.group),data.regex,str(data.regex_name),str(data.id)) )
                
            sqliteConnection.commit()
            msg = "Record successfully added"
            print(f" >>>>>>> Record successfully added [{count}]" ,flush=True)
            cursor.close()


            time.sleep(3)
        except:
            msg = "error in insert operation"
            print(f" >>>>>>> error in insert operation" ,flush=True)

            sqliteConnection.rollback()
            time.sleep(3)
        
        finally:
            if sqliteConnection:
                sqliteConnection.close()

            time.sleep(3)
            return cursor.rowcount

        return cursor.rowcount


    def saveData(self,data,group):


        try:

            #data.group, data.regex, data.regex_name, data.id, data.date, data.file_name, data.caption, data.width, data.file_size, data.status
            print(f" >>>>>>> saveData [{d.group}]" ,flush=True)
            print(f" >>>>>>> saveData [{d.regex}]" ,flush=True)
            print(f" >>>>>>> saveData [{d.regex_name}]" ,flush=True)
            print(f" >>>>>>> saveData [{d.id}]" ,flush=True)
            print(f" >>>>>>> saveData [{d.date}]" ,flush=True)
            print(f" >>>>>>> saveData [{d.file_name}]" ,flush=True)
            print(f" >>>>>>> saveData [{d.caption}]" ,flush=True)
            print(f" >>>>>>> saveData [{d.width}]" ,flush=True)
            print(f" >>>>>>> saveData [{d.file_size}]" ,flush=True)
            print(f" >>>>>>> saveData [{d.status}]" ,flush=True)

            
            sqliteConnection  = sqlite3.connect(self.DATABASE)
            cursor = sqliteConnection.cursor()


            count = cursor.execute("INSERT INTO downloader ('group', 'regex', 'regex_name', 'id', 'date', 'file_name', 'caption', 'width', 'file_size', 'status') VALUES (?,?,?,?,?,?,?,?,?,?)",(d.group, d.regex, d.regex_name, d.id, d.date, d.file_name, d.caption, d.width, d.file_size, d.status) )
            #count = cursor.execute("INSERT INTO students (name , addr , city , pin  ) VALUES (?,?,?,?)",(str(data.group),data.regex,str(data.regex_name),str(data.id)) )
            #count = cursor.execute("INSERT INTO downloader ('group', 'regex', 'regex_name', 'id'  ) VALUES (?,?,?,?)",(str(data.group),data.regex,str(data.regex_name),str(data.id)) )
                
            sqliteConnection.commit()
            msg = "Record successfully added"
            print(f" >>>>>>> Record successfully added [{count}]" ,flush=True)
            cursor.close()


            time.sleep(3)
        except:
            msg = "error in insert operation"
            print(f" >>>>>>> error in insert operation" ,flush=True)

            sqliteConnection.rollback()
            time.sleep(3)
        
        finally:
            if sqliteConnection:
                sqliteConnection.close()

            time.sleep(3)
            return cursor.rowcount

        return cursor.rowcount



    def telegramtoData(self,data,group):

        newdata = []
        for d in data:
            try:
                print(f" >>>>>>> telegramtoData [{d}]" ,flush=True)

                newObject = Object()
                newObject.group          = group
                newObject.regex          = ""
                newObject.regex_name     = ""
                newObject.id             = d.id
                newObject.date           = d.date
                newObject.file_name      = d.video.file_name
                newObject.caption        = d.caption 
                newObject.width          = f"{d.video.width}x{d.video.height}"
                newObject.file_size      = d.video.file_size
                newObject.status         = ""

                newdata.append(newObject)

                self.saveData(newObject)

            except:
                msg = "error in insert operation"
                print(f" >>>>>>> error in insert operation" ,flush=True)
        return newdata






class Data:

    group         = ''
    regex         = ''
    regex_name    = ''
    id            = ''
    date          = ''
    file_name     = ''
    caption       = ''
    width         = ''
    file_size     = ''
    status        = ''


class studentDef(object):
    def __init__(self, group, regex, regex_name, id, date, file_name, caption, width, file_size , status ):
        self.group        = group       
        self.regex        = regex       
        self.regex_name   = regex_name  
        self.id           = id          
        self.date         = date        
        self.file_name    = file_name   
        self.caption      = caption     
        self.width        = width       
        self.file_size    = int(file_size)   
        self.status       = status      

class dataGroup(object):
    def __init__(self, group, regex_download, regex_name, folder_download, status):
        self.group              = group       
        self.regex_download     = regex_download       
        self.regex_name         = regex_name  
        self.folder_download    = folder_download          
        self.status             = status        

class Object(object):
    pass
