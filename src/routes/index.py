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
import utils.telegram

index = Blueprint("index", __name__)



@index.route("/")
def home():

    downloaded = []
    newDatabase = Database()

    data = newDatabase.getHistory()
    groups = newDatabase.getGroups()

    print(f" >>>>>>> history [{data}]" ,flush=True)


    return render_template(
        'index_all.html', group='group', data=data, regex='regex', channels=groups, regex_download='_regex_download', folder_download='_folder_download', regex_rename='_regex_rename', rename='rename', downloaded=downloaded
    )





@index.route('/reload/<group>',methods=['GET','POST'])
@index.route('/reload/',methods=['GET','POST'])
async def reload(group=None):

    downloaded = []

    group = 'traicionada_mega'
    group = 'hastaencontrarte'
    group = 'laleydebaltazarcl'


    try:

        #if not data:
        limit = request.args.get('limit', default = 50, type = int)
        init = request.args.get('init', default = None, type = str)


        newDatabase = Database()
        groups = newDatabase.getGroups()

        data = await utils.telegram.get_chat_history(group,limit=limit, init=init)
        if data:
            ndata = newDatabase.telegramtoData(data,group)
        else:
            data = newDatabase.getHistory()            
 


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
        'index_all.html', group='group', data=ndata, regex='regex', channels=groups, regex_download='_regex_download', folder_download='_folder_download', regex_rename='_regex_rename', rename='rename', downloaded=downloaded
    )








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

