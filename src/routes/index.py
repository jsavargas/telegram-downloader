from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    Response,
    flash,
    jsonify,
    session,
    send_file
)

from controllers.telegram_api import telegram_api


import json
import random
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import pickle

import os


from controllers.database import Database, Object
import controllers.telegram
import controllers.download
from controllers.jsonDB import  jsonDB

index = Blueprint("index", __name__)


newDatabase = Database()
executor = ThreadPoolExecutor(max_workers=1)

@index.route("/favicon.ico")
def favicon():
    print(f" [!] favicon.ico", flush=True)

    return redirect(url_for('static', filename='favicon.ico'), code=302)


telegram = telegram_api()

@index.route("/")
async def home():
    global chats

    print(f" [!] home", flush=True)

    chats = telegram.getChatDictionary()
    if not chats:
        chats = await telegram.getAllChats()
        check = telegram.setChatDictionary(chats)

    history = newDatabase.getHistory()

    return render_template('index.html',
        countAll=len(history),
        chats=chats
    )


@index.route("/getdb")
async def getDB(group=None):
    json_db = jsonDB()
    return json_db.getDownloaderDB()


@index.route("/<group>")
async def group(group=None):
    global chats
    print(f" [!] /<group>", flush=True)

    chats = []
    data = []

    try:

        limit = request.args.get('limit', default = 100, type = int)
        init = request.args.get('init', default = None, type = str)

        print(f" [!] GET >>> index.route group [{group}] limit:[{limit}]", flush=True)
        
        chats = await telegram.getAllChats()
        data = await telegram.get_chat_history(group,limit=limit,init=init)

        configGroups = newDatabase.getConfigGroup(group)    
        if configGroups:
            regex_download  = configGroups[0]['regex_download']
            regex_rename    = configGroups[0]['regex_rename']
        else:
            regex_download      = ''
            regex_rename        = ''


    except Exception as e:
        print(f" [!] Exception index.route group[{e}]", flush=True)


    return render_template('data.html',
        chats=chats, 
        group=group, 
        data=data,
        regex_download=regex_download,
        regex_rename=regex_rename,
    )


@index.route('/edit/<group>',methods=['GET','POST'])
async def edit(group=None):
    global data
    global chats

    downloaded = []

    try:

        limit = request.args.get('limit', default = 100, type = int)
        init = request.args.get('init', default = None, type = str)

        print(f" [!] GET >>> index.route group [{group}] limit:[{limit}]", flush=True)

        chats = await telegram.getAllChats()
        data = await telegram.get_chat_history(group,limit=limit,init=init)

        print(f" [!] /edit/<group> >>> chats [{len(chats)}]", flush=True)
        print(f" [!] /edit/<group> >>> data [{len(data)}]", flush=True)
        configGroups = newDatabase.getConfigGroup(group)    
        if configGroups:
            regex_download  = configGroups[0]['regex_download']
            regex_rename    = configGroups[0]['regex_rename']
        else:
            regex_download      = ''
            regex_rename        = ''

    except Exception as e:
        print(f" >>>>>>> Exception /edit/<group> [{e}]" ,flush=True)


    return render_template('config_edit.html',
        group=group, 
        chats=chats, 
        data=data,
        regex_download=regex_download,
        regex_rename=regex_rename,
        configGroups=configGroups
    )

@index.route('/regex/get/<group>',methods=['GET','POST'])
async def getRegex(group):
    global data


    channels = []
    regex = {}
    rename = {}
    downloaded = []
    #data = []

    regex_download = ''
    _regex_download = ''
    _regex_rename = ''
    _folder_download = ''
    _group = ''

    try:

        #channels = utils.config.getChannels()
        #_regex_download = utils.config.getRegex_download(group)
        #_folder_download = utils.config.getDownloadPath(group)
        #_regex_rename = utils.config.getRegex_rename(group)

        newDatabase = Database()

        #data = newDatabase.getHistory(group)
        #groups = newDatabase.getGroups()

        if request.method == 'POST':

            _regex_download = request.form.get('regex_download').replace('/','')
            _regex_rename = request.form.get('regex_rename')
            _folder_download = request.form.get('folder_download').replace('/','')
            _group = request.form.get('group').replace('/','')

            print(f" [!] POST >>> _regex_download [{_regex_download}]", flush=True)
            print(f" [!] POST >>> _regex_rename [{_regex_rename}]", flush=True)
            print(f" [!] POST >>> _folder_download [{_folder_download}]", flush=True)
    

        downloaded = []

    except Exception as e:
        print(f" >>>>>>> Exception [{e}]" ,flush=True)


    return render_template(
        'data_telegram.html', 
        group=group, 
        data=data, 
        regex=regex, 
        rename=rename, 
        regex_download=_regex_download, 
        regex_rename=_regex_rename, 
        folder_download=_folder_download, 
        downloaded=downloaded
    )

@index.route('/regex/set/<group>',methods=['POST'])
async def setRegex(group):
    _regex_download = request.form.get('regex_download').replace('/','')
    _regex_rename = request.form.get('regex_rename')
    _folder_download = request.form.get('folder_download')
    _group = request.form.get('group')

    print(f" [!] POST >>> _regex_download [{_regex_download}]", flush=True)
    print(f" [!] POST >>> _regex_rename [{_regex_rename}]", flush=True)
    print(f" [!] POST >>> _folder_download [{_folder_download}]", flush=True)

    data = Object()

    data.group = group
    data.regex_download = _regex_download
    data.regex_rename = _regex_rename
    data.folder_download = _folder_download
    data.status = 1

    configGroups = newDatabase.saveConfigGroup(data)
    

    return f"[{configGroups}]"

# You would use weather_detail here
async def processDownload(_group,_message_id,regex_download,regex_rename,folder_download):
    data = ""
    # jasv
    #TODO
    data = await controllers.download.downloadFile(_group,_message_id,regex_download,regex_rename,folder_download)


    #for num in range(1, 10):
    #    print(f" _message_id:: [{_message_id}] - {num}", flush=True )
    #    time.sleep(.5)

    return data

def wrapper(coro):
    return asyncio.run(coro)

@index.route('/regex/downloadFile',methods=['POST'])
async def downloadFile():
    try:

        _group = request.form.get('group')
        _message_id = request.form.get('message_id')

        configGroups = newDatabase.getConfigGroup(_group)    
        regex_download  = configGroups[0]['regex_download'] if configGroups else ''
        regex_rename    = configGroups[0]['regex_rename'] if configGroups else ''
        folder_download    = configGroups[0]['folder_download'] if configGroups else '/download/completed'


        #telegram
        #controllers.jsonDB.addDownloader(_group, _message_id)
        #return False
        downloaded = telegram.downloadFile(_group, _message_id, force=True)

        print(f"downloadFile::::: [{downloaded}]",flush=True)
    
        if downloaded == 'continue': 
            return {'status': 'continue'}
        elif downloaded:
            return {'status': True}
        else: 
            return {'status': False}
    
    except Exception as e:
        print(f" >>>>>>> Exception [{e}]" ,flush=True)
        return 'False'







@index.context_processor
def utility_processor():
    def human_readable_size(size, decimal_places=2):
        size = int(size)
        for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
            if size < 1024.0 or unit == "PiB":
                break
            size /= 1024.0
        return f"{size:.{decimal_places}f} {unit}"

    return dict(human_readable_size=human_readable_size)

@index.context_processor
def utility_processor():
    def regexDownload(group, file_name, caption=None,regex_download=None,regex_rename=None):
        download = controllers.download.regexDownload(group, file_name, caption,regex_download,regex_rename)
        return download
    return dict(regexDownload=regexDownload)

@index.context_processor
def utility_processor():
    def regexRename(group, file_name, caption=None,regex_download=None,regex_rename=None):
        rename = controllers.download.regexRename(group, file_name, caption,regex_download,regex_rename)
        return rename
    return dict(regexRename=regexRename)

@index.context_processor
def utility_processor():
    def ifDownloaded(group, message_id):
        reifDownloaded = controllers.download.ifDownloaded(group, message_id)
        return reifDownloaded
    return dict(ifDownloaded=ifDownloaded)
