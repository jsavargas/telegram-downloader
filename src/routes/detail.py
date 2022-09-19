from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    Response,
    flash,
)

from utils.database import Database, Data, Object
import utils.config

detail = Blueprint("detail", __name__)

newDatabase = Database()


@detail.route('/detail/<group>',methods=['GET','POST'])
@detail.route('/detail/',methods=['GET','POST'])
def home(group=None):

    downloaded = []

    data = newDatabase.getHistory(group)
    groups = newDatabase.getGroups()

    print(f" >>>>>>> history [{data}]" ,flush=True)

    configGroups = newDatabase.getConfigGroup(group)
    if configGroups:
        _regex_download     = configGroups[0]['regex_download']
        _regex_rename       = configGroups[0]['regex_rename']
        _folder_download    = configGroups[0]['folder_download']

    regex, rename = utils.config.getFileRename2(data,_regex_download,_regex_rename)

    return render_template(
        'index_all.html', group=group, data=data, regex=regex, rename=rename, channels=groups
    )


@detail.route('/detail/edit/<group>',methods=['GET','POST'])
@detail.route('/detail/edit/',methods=['GET','POST'])
def edit(group=None):

    downloaded = []
    _regex_download     = ''
    _regex_rename       = ''
    _folder_download    = ''

    data = newDatabase.getHistory(group)
    groups = newDatabase.getGroups()

    #_regex_download = utils.config.getRegex_download(group)
    #_regex_rename= utils.config.getRegex_rename(group)
    #_folder_download= utils.config.getDownloadPath(group)

    regex = {}
    rename = {}

    configGroups = newDatabase.getConfigGroup(group)
    if configGroups:
        _regex_download     = configGroups[0]['regex_download']
        _regex_rename       = configGroups[0]['regex_rename']
        _folder_download    = configGroups[0]['folder_download']


    regex, rename = utils.config.getFileRename2(data,_regex_download,_regex_rename)
    print(f" [!] groupData >>> _regex_download [{_regex_download}] ", flush=True)
    print(f" [!] groupData >>> _regex_rename [{_regex_rename}] ", flush=True)
    print(f" [!] groupData >>> regex [{regex}] ", flush=True)
    print(f" [!] groupData >>> rename [{rename}] ", flush=True)


    return render_template(
        'config_edit.html', groups=groups, data=data, configGroups=configGroups, regex=regex, rename=rename, downloaded=downloaded
    )




@detail.route('/detail/regex/get/<group>',methods=['GET','POST'])
async def groupData(group):

    channels = []
    regex = {}
    rename = {}
    data = []
    downloaded = []

    regex_download = ''
    _regex_download = ''
    _regex_rename = ''
    _folder_download = ''
    _group = ''

    try:
        #if not data:
        limit = request.args.get('limit', default = 30, type = int)
        init = request.args.get('init', default = None, type = str)

        print(f" [!] GET >>> limit [{limit}]", flush=True)
        print(f" [!] GET >>> init [{init}]", flush=True)

        #channels = utils.config.getChannels()
        #_regex_download = utils.config.getRegex_download(group)
        #_folder_download = utils.config.getDownloadPath(group)
        #_regex_rename = utils.config.getRegex_rename(group)

        newDatabase = Database()

        data = newDatabase.getHistory(group)
        groups = newDatabase.getGroups()

        if request.method == 'POST':
            _regex_download = request.form.get('regex_download').replace('/','')
            _regex_rename = request.form.get('regex_rename')
            _folder_download = request.form.get('folder_download').replace('/','')
            _group = request.form.get('group').replace('/','')

            print(f" [!] POST >>> _regex_download [{_regex_download}]", flush=True)
            print(f" [!] POST >>> _regex_rename [{_regex_rename}]", flush=True)
            print(f" [!] POST >>> _folder_download [{_folder_download}]", flush=True)
    

        regex, rename = utils.config.getFileRename2(data,_regex_download,_regex_rename)
        print(f" [!] groupData >>> regex [{regex}] [{rename}]", flush=True)
        downloaded = []

    except Exception as e:
        print(f" >>>>>>> Exception [{e}]" ,flush=True)

    if request.method == 'POST':
        page = "telegram_table_all.html"
    else:
        page = "telegram_table_all.html"

    return render_template(
        page, group=group, data=data, regex=regex, channels=channels, regex_download=_regex_download, folder_download=_folder_download, regex_rename=_regex_rename, rename=rename, downloaded=downloaded
    )


@detail.route('/detail/regex/set/<group>',methods=['POST'])
async def save(group):
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

    #_folder_download = utils.config.setDownloadPath(group,_folder_download)
    #_regex_download = utils.config.setRegex_download(group,_regex_download)
    #_regex_rename = utils.config.setRegex_rename(group,_regex_rename)

    return f"[{data}]"

















@detail.context_processor
def utility_processor():
    def human_readable_size(size, decimal_places=2):
        size = int(size)
        for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
            if size < 1024.0 or unit == "PiB":
                break
            size /= 1024.0
        return f"{size:.{decimal_places}f} {unit}"

    return dict(human_readable_size=human_readable_size)

