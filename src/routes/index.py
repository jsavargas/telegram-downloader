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

from controllers.database import Database, Data, Object
import controllers.telegram
import controllers.download

index = Blueprint("index", __name__)


newDatabase = Database()

@index.route("/favicon.ico")
def favicon():
    return ""

@index.route("/")
def home():

    downloaded = []

    #flash('You were successfully logged in')

    return render_template('index.html')
    return render_template(
        'index.html', 
        data=data, 
        regex='regex', 
        channels=groups, 
        regex_download='_regex_download', 
        folder_download='_folder_download', 
        regex_rename='_regex_rename', 
        rename='rename', 
        downloaded=downloaded
    )


@index.route("/<group>")
async def group(group=None):
    data = []
    try:
        print(f" [!] GET >>> index.route group [{group}]", flush=True)

        data = await controllers.telegram.get_chat_history(group)

        configGroups = newDatabase.getConfigGroup(group)    
        if configGroups:
            regex_download  = configGroups[0]['regex_download']
            regex_rename    = configGroups[0]['regex_rename']
        else:
            regex_download      = ''
            regex_rename        = ''


    except Exception as e:
        print(f" [!] Exception index.route group[{group}]", flush=True)


    return render_template('index.html',
        group=group, 
        data=data,
        regex_download=regex_download,
        regex_rename=regex_rename,
    )


@index.route('/edit/<group>',methods=['GET','POST'])
async def edit(group=None):
    global data
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


@index.route('/regex/downloadFile',methods=['POST'])
async def downloadFile():
    try:

        _group = request.form.get('group')
        _message_id = request.form.get('message_id')

        print(f"_group::{_group}",flush=True)
        print(f"_message_id::{_message_id}",flush=True)

        
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
