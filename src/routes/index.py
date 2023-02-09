from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    Response,
    flash,
    jsonify,
    session
)

import json
import random
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor


from controllers.database import Database
import controllers.telegram
import controllers.download

index = Blueprint("index", __name__)


newDatabase = Database()
executor = ThreadPoolExecutor(max_workers=1)

@index.route("/favicon.ico")
def favicon():
    return ""

@index.route("/")
async def home():
    global chats

    history = newDatabase.getHistory()
    chats = await controllers.telegram.getAllChats()


    print(f" [!] getAllChats [{chats}]", flush=True)


    return render_template('index.html',
        countAll=len(history),
        chats=chats
    )


@index.route("/<group>")
async def group(group=None):
    global chats

    data = []
    try:
        group = group.strip().lower()

        #if chats is None: chats = await controllers.telegram.getAllChats()
        chats = await controllers.telegram.getAllChats()

        print(f" [!] GET >>> index.route group [{group}]", flush=True)

        limit = request.args.get('limit', default = 100, type = int)
        init = request.args.get('init', default = None, type = str)

        data = await controllers.telegram.get_chat_history(group,limit=limit,init=init)

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
        data = await controllers.telegram.get_chat_history(group)
        print(f" [!] /edit/<group> >>> data ", flush=True)

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
async def get_random(_group,_message_id,regex_download,regex_rename,folder_download):

    data = await controllers.download.downloadFile(_group,_message_id,regex_download,regex_rename,folder_download)

    await asyncio.sleep(5.0)
    return data
    return random.randint(10, 50)

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


        arglist = ((_group,_message_id,regex_download,regex_rename,folder_download), )
        coros = [get_random(_group,_message_id,regex_download,regex_rename,folder_download) for _group,_message_id,regex_download,regex_rename,folder_download in arglist]
        
        print("Start", time.ctime(), flush=True)
        for r in executor.map(wrapper, coros):
            print(f"{r}, {time.ctime()}", flush=True)        
            return 'True'
        
        return 'False'

        #print("Start", time.ctime(), flush=True)
        #with ThreadPoolExecutor(max_workers=1) as executor:
        #    arglist = ((_group,_message_id,regex_download,regex_rename,folder_download), )
        #    coros = [get_random(_group,_message_id,regex_download,regex_rename,folder_download) for _group,_message_id,regex_download,regex_rename,folder_download in arglist]
        #    for r in executor.map(wrapper, coros):
        #        print(f"{r}, {time.ctime()}", flush=True)

        _group = request.form.get('group')
        _message_id = request.form.get('message_id')

        print(f"_group::{_group}",flush=True)
        print(f"_message_id::{_message_id}",flush=True)

        return _message_id
        
        configGroups = newDatabase.getConfigGroup(_group)    

        regex_download  = configGroups[0]['regex_download'] if configGroups else ''
        regex_rename    = configGroups[0]['regex_rename'] if configGroups else ''
        folder_download    = configGroups[0]['folder_download'] if configGroups else '/download/completed'

        print(f"regex_rename::{configGroups}",flush=True)
        print(f"regex_download::{regex_download}",flush=True)
        print(f"regex_rename::{regex_rename}",flush=True)
        print(f"regex_rename::{configGroups}",flush=True)
        print(f"regex_rename::{configGroups[0]['regex_rename']}",flush=True)

        data = await controllers.download.downloadFile(_group,_message_id,regex_download,regex_rename,folder_download)


        return 'True'
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
