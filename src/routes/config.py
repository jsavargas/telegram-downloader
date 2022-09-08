from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    Response,
    flash,
)

from utils.database import Database, Data
import utils.config

config = Blueprint("config", __name__)

newDatabase = Database()

@config.route('/config/<group>',methods=['GET','POST'])
@config.route('/config/',methods=['GET','POST'])
def home(group=None):

    downloaded = []

    data = newDatabase.getHistory(group)
    groups = newDatabase.getGroups()

    print(f" >>>>>>> history [{data}]" ,flush=True)

    configGroups = newDatabase.getConfigGroup()
    if configGroups:
        _regex_download     = configGroups[0]['regex_download']
        _regex_rename       = configGroups[0]['regex_rename']
        _folder_download    = configGroups[0]['folder_download']


    #return jsonify(data)

    return render_template(
        'config.html', configGroups=configGroups, group=group, data=data, regex='regex', channels=groups, regex_download='_regex_download', folder_download=_folder_download, regex_rename='_regex_rename', rename='rename', downloaded=downloaded
    )























# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
# -------------------------------------------------------------------------


@config.context_processor
def utility_processor():
    def human_readable_size(size, decimal_places=2):
        size = int(size)
        for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
            if size < 1024.0 or unit == "PiB":
                break
            size /= 1024.0
        return f"{size:.{decimal_places}f} {unit}"

    return dict(human_readable_size=human_readable_size)

