from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    Response,
    flash,
    jsonify
)

from utils.database import Database, Data, Object
import utils.telegramDownload

index = Blueprint("index", __name__)


newDatabase = Database()

@index.route("/")
def home():

    downloaded = []

    newDatabase = Database()


    data = newDatabase.getHistory()
    groups = newDatabase.getGroups()

    print(f" >>>>>>> history [{data}]" ,flush=True)


    return render_template(
        'index_all.html', data=data, regex='regex', channels=groups, regex_download='_regex_download', folder_download='_folder_download', regex_rename='_regex_rename', rename='rename', downloaded=downloaded
    )





@index.route('/reload/<group>',methods=['GET','POST'])
@index.route('/reload/',methods=['GET','POST'])
async def reload(group=None):

    configGroups = []
    ndata = []
    regex = []
    rename = []


    try:

        #if not data:
        limit = request.args.get('limit', default = 30, type = int)
        init = request.args.get('init', default = None, type = str)


        newDatabase = Database()
        groups = newDatabase.getGroups()


        print(f" [!] GET >>> group IS NONE [{group}]", flush=True)
        if group==None:
            print(f" [!] GET >>> group IS NONE [{group}]", flush=True)

            for g in groups:
                data = await utils.telegramDownload.get_chat_history(g,limit=limit, init=init)
                if data:
                    ndata += newDatabase.telegramtoData(data,g)
        else:
            data = await utils.telegramDownload.get_chat_history(group,limit=limit, init=init)
            if data:
                ndata += newDatabase.telegramtoData(data,group)
            
        print(f" [!] GET >>> ndata [{ndata}]", flush=True)

        if not ndata:
            ndata = newDatabase.getHistory()            
        if group: 
            print(f" [!] GET 3>>> group IS NONE [{group}]", flush=True)

            ndata = newDatabase.getHistory(group)
            configGroups = newDatabase.getConfigGroup(group)
            if configGroups:
                _regex_download     = configGroups[0]['regex_download']
                _regex_rename       = configGroups[0]['regex_rename']
                _folder_download    = configGroups[0]['folder_download']

                regex, rename = utils.config.getFileRename2(ndata,_regex_download,_regex_rename)



        print(f" [!] GET >>> limit [{limit}]", flush=True)
        print(f" [!] GET >>> init [{init}]", flush=True)
        print(f" [!] GET >>> ndata [{ndata}]", flush=True)


    except Exception as e:
        print(f" >>>>>>> Exception [{e}]" ,flush=True)

    if request.method == 'POST':
        page = "index.html"
    else:
        page = "index.html"


    return render_template(
        'telegram_table_all.html', groups=groups, data=ndata, configGroups=configGroups, regex=regex, rename=rename
    )


@index.route('/pyrogram/downloadFile',methods=['POST'])
async def downloadFile():


    try:
        downloaded = False

        _group = request.form.get('group')
        _message_id = request.form.get('message_id')

        print(f" [!] downloadFile >>> _group [{_group}] ", flush=True)
        print(f" [!] downloadFile >>> _message_id [{_message_id}] ", flush=True)

        data = await utils.telegramDownload.downloadFile(_group,_message_id)

        if data:
            return jsonify({'error': 'Admin access is required'}), 200
        else:
            return jsonify({'error': 'Admin access is required'}), 400

    except Exception as e:
        print(f" >>>>>>> Exception [{e}]" ,flush=True)
        return jsonify({'error': 'Admin access is required'}), 400






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

