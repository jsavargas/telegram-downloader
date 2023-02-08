import os
import time
import sqlite3

import asyncio

from flask import (
    flash
    )

class Database:

    def __init__(self):

        self.DATABASE = '/config/database.db'

        conn = sqlite3.connect(self.DATABASE)

        conn.execute("CREATE TABLE IF NOT EXISTS students ('name' TEXT, 'addr' TEXT, 'city' TEXT, 'pin' TEXT)")
        conn.execute("CREATE TABLE IF NOT EXISTS downloader ('id' INTEGER, 'group' TEXT, 'message_id' TEXT, 'new_name' TEXT, 'file_name' TEXT, 'caption' TEXT, 'regex_download' TEXT, 'regex_rename' TEXT, 'folder_download' TEXT, 'download_final_path' TEXT, 'width' TEXT, 'file_size' INTEGER, 'status' BOOLEAN)")
        conn.execute("CREATE TABLE IF NOT EXISTS groups ( ID INTEGER PRIMARY KEY AUTOINCREMENT, 'group' TEXT, 'regex_download' TEXT, 'regex_rename' TEXT, 'folder_download' TEXT, 'status' BOOLEAN )")

        createSecondaryIndex = "CREATE UNIQUE INDEX IF NOT EXISTS index_group_id ON downloader('group','id')"
        conn.execute(createSecondaryIndex)

        conn.close()

    def getHistory(self, group=None):
        conn = sqlite3.connect(self.DATABASE)
        conn.row_factory = sqlite3.Row

        if group == None:
            query = "SELECT * FROM downloader ORDER BY `group`,`id` DESC "
        else:
            query = f"SELECT * FROM downloader where `group` = '{group}' ORDER BY `group`,`id` DESC"

        #print(f" >>>>>>> getHistory [{query}]", flush=True)

        data = conn.execute(query).fetchall()
    
        #flash('getHistory')

        conn.close()

        return [downloaderObj(*row) for row in data]


    def getLastIDHistory(self,group=None):
        conn = sqlite3.connect(self.DATABASE)
        cursor=conn.cursor()

        if group:
            query = f"SELECT max(id) FROM downloader where `group` = '{group}'"

            cursor.execute(query)
            lastID = cursor.fetchone()[0]
        else:
            lastID = 0

        conn.close()
        
        print(f" Last ID saved: [{group}] [{lastID}]" ,flush=True)
        
        return lastID

        

    def getGroups(self):

        conn = sqlite3.connect(self.DATABASE)
        conn.row_factory = sqlite3.Row

        query = "SELECT DISTINCT `group` FROM groups ORDER BY `group`,`ID` DESC "

        #print(f" >>>>>>> getGroups [{query}]", flush=True)

        data = conn.execute(query).fetchall()

        conn.close()

        return [row['group'] for row in data]


        return ["hijosdeldesiertocaps", "laleydebaltazarcapitulos",
                "laleydebaltazar", "hastaencontrarte", "traicionada_mega", "laleydebaltazarcl"]

    def getConfigGroup(self, group=None):

        conn = sqlite3.connect(self.DATABASE)
        conn.row_factory = sqlite3.Row

        if group == None:
            query = "SELECT * FROM groups ORDER BY `group`,`id` ASC "
        else:
            query = f"SELECT * FROM groups where `group` = '{group}' ORDER BY `group`,`id` ASC"

        data = conn.execute(query).fetchall()
        conn.close()
        if not data:
            data = []
            data.append({})
            data[0]['group'] = group
            data[0]['regex_download'] = ""
            data[0]['regex_rename'] = ""
            data[0]['folder_download'] = ""
            data[0]['ID'] = ""

        return [row for row in data]

    def saveConfigGroup(self, config):

        print(f" >>>>>>> saveConfigGroup [{config}]", flush=True)
        try:

            sqliteConnection = sqlite3.connect(self.DATABASE)
            cursor = sqliteConnection.cursor()
            sqliteConnection.row_factory = sqlite3.Row

            resp = sqliteConnection.execute(
                f"SELECT * FROM groups WHERE `group` = '{config.group}'").fetchall()

            print(f" >>>>>>> SELECT * FROM groups [{resp}]", flush=True)

            if resp:
                try:

                    print(f" >>>>>>> UPDATE", flush=True)
                    count = cursor.execute("UPDATE groups SET `regex_download`=?,`regex_rename`=?,`folder_download`=?,`status`=? WHERE `group`=?", (
                        config.regex_download, config.regex_rename, config.folder_download, config.status, config.group))
                    sqliteConnection.commit()
                    print(
                        f" >>>>>>> Record successfully UPDATE [{count}]", flush=True)
                    cursor.close()

                    return 10
                except Exception as e:
                    print(
                        f" >>>>>>> Record Exception UPDATE [{e}]", flush=True)

            count = cursor.execute("INSERT INTO groups (`group`, 'regex_download', 'regex_rename', 'folder_download', 'status' ) VALUES (?,?,?,?,?)", (
                config.group, config.regex_download, config.regex_rename, config.folder_download, config.status))
            #count = cursor.execute("INSERT INTO students (name , addr , city , pin  ) VALUES (?,?,?,?)",(str(data.group),data.regex,str(data.regex_name),str(data.id)) )
            #count = cursor.execute("INSERT INTO downloader ('group', 'regex', 'regex_name', 'id'  ) VALUES (?,?,?,?)",(str(data.group),data.regex,str(data.regex_name),str(data.id)) )

            sqliteConnection.commit()
            msg = "Record successfully added"
            #print(f" >>>>>>> Record successfully added [{count}]", flush=True)
            cursor.close()
        except:
            msg = "error in insert operation"
            print(f" >>>>>>> error in insert operation", flush=True)

            sqliteConnection.rollback()

        finally:
            if sqliteConnection:
                sqliteConnection.close()

            return cursor.rowcount

        return cursor.rowcount

    def saveData(self, group, message_id, new_name, file_name, caption, regex_download, regex_rename, folder_download, download_final_path, status, width='', file_size=''):

        try:


            sqliteConnection = sqlite3.connect(self.DATABASE)
            cursor = sqliteConnection.cursor()

            count = cursor.execute("INSERT INTO downloader ('group', 'message_id', 'new_name', 'file_name', 'caption', 'regex_download', 'regex_rename', 'folder_download', 'download_final_path', 'width', 'file_size', 'status') VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (
                group, message_id, new_name, file_name, caption, regex_download, regex_rename, folder_download, download_final_path, width,file_size,status))
            #count = cursor.execute("INSERT INTO students (name , addr , city , pin  ) VALUES (?,?,?,?)",(str(data.group),data.regex,str(data.regex_name),str(data.id)) )
            #count = cursor.execute("INSERT INTO downloader ('group', 'regex', 'regex_name', 'id'  ) VALUES (?,?,?,?)",(str(data.group),data.regex,str(data.regex_name),str(data.id)) )

            sqliteConnection.commit()
            print(f" [*] Record successfully added [{group}] [{message_id}]", flush=True)
            cursor.close()

        except Exception as e:
            print(f" >>>>>>> error in insert operation [{e}]", flush=True)

            sqliteConnection.rollback()

        finally:
            if sqliteConnection:
                sqliteConnection.close()

            return cursor.rowcount

        return cursor.rowcount


    def ifDownloaded(self,group, message_id):

        try:
            #print(f" ifDownloaded IN: [{group}] [{message_id}] " ,flush=True)

            conn = sqlite3.connect(self.DATABASE)
            cursor=conn.cursor()

            if group:
                query = f"SELECT `status` FROM downloader where `group` = '{group}' and `message_id` = '{message_id}' "
                cursor.execute(query)
                
                data = cursor.fetchone()
                
                if data: 
                    status = True
                else:
                    status = False

            else:
                status = False

            conn.close()
            
            #print(f" ifDownloaded: [{group}] [{message_id}] [{status}]" ,flush=True)
            
            return status

        except Exception as e:
            print(f" >>>>>>> error database ifDownloaded [{e}]", flush=True)

            return False





    def updateDataaaaaaaa(self, group, id, _file_name):

        try:

            dirname = os.path.dirname(_file_name)
            basename = os.path.basename(_file_name)

            #data.group, data.regex, data.regex_name, data.id, data.date, data.file_name, data.caption, data.width, data.file_size, data.status

            sqliteConnection = sqlite3.connect(self.DATABASE)
            cursor = sqliteConnection.cursor()

            count = cursor.execute(
                "UPDATE downloader SET `status`=?, regex_name=? WHERE `group`=? AND `id`=?", (1, basename, group, id))
            #count = cursor.execute("INSERT INTO students (name , addr , city , pin  ) VALUES (?,?,?,?)",(str(data.group),data.regex,str(data.regex_name),str(data.id)) )
            #count = cursor.execute("INSERT INTO downloader ('group', 'regex', 'regex_name', 'id'  ) VALUES (?,?,?,?)",(str(data.group),data.regex,str(data.regex_name),str(data.id)) )

            sqliteConnection.commit()
            #print(f" [*] Record successfully added updateData [{group}] [{id}]", flush=True)
            cursor.close()

            return True

        except Exception as e:
            print(f" >>>>>>> error in insert operation [{e}]", flush=True)

            sqliteConnection.rollback()
            return False

        finally:
            if sqliteConnection:
                sqliteConnection.close()

            return True
            return cursor.rowcount

        return True
        return cursor.rowcount

    def telegramtoData(self, data, group):

        newdata = []
        for d in data:
            try:

                newObject = Object()
                newObject.group = group
                newObject.regex = ""
                newObject.regex_name = ""
                newObject.id = d.id
                newObject.date = d.date
                newObject.file_name = d.video.file_name
                newObject.caption = d.caption
                newObject.width = f"{d.video.width}x{d.video.height}"
                newObject.file_size = d.video.file_size
                newObject.status = ""

                newdata.append(newObject)

                self.saveData(newObject)

                print(f" >>>>>>> telegramtoData file_size [{newObject.file_size}]", flush=True)
            except Exception as e:
                print(
                    f" >>>>>>> telegramtoData error in insert operation [{e}]", flush=True)

        return newdata


class Data:

    group = ''
    regex = ''
    regex_name = ''
    id = ''
    date = ''
    file_name = ''
    caption = ''
    width = ''
    file_size = ''
    status = ''


class downloaderObj(object):
    def __init__(self, group, regex, regex_name, id, date, file_name, caption, width, file_size, status):
        try:
            self.group = group
            self.regex = regex
            self.regex_name = regex_name
            self.id = id
            self.date = date
            self.file_name = file_name
            self.caption = caption
            self.width = width
            self.file_size = int(file_size) 
            self.status = status
        except Exception as e:
            pass

class dataGroup(object):
    def __init__(self, group, regex_download, regex_name, folder_download, status):
        self.group = group
        self.regex_download = regex_download
        self.regex_name = regex_name
        self.folder_download = folder_download
        self.status = status


class Object(object):
    pass
