import asyncio
import os
import pickle
import re
import time
import json
import pdb

import utils.telegram
import utils.config
import utils.db

from flask import Flask, request, session, render_template


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

data = None

DICCIONARY_PATH = utils.config.DICCIONARY_PATH



@app.route('/')
async def home():

    global data
    rename = {}
    data = {}

    #data = await utils.telegram.get_chat_history()

   
    regex = {}
    for d in data:
        regex[d.id] = d.id


    channels = utils.config.getChannels()

    return render_template(
        "index.html", data=data, regex=regex, channels=channels, rename=rename
    )



@app.route('/group/<group>',methods=['GET','POST'])
async def groupData(group):
    global data

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

        channels = utils.config.getChannels()
        _regex_download = utils.config.getRegex_download(group)
        _folder_download = utils.config.getDownloadPath(group)
        _regex_rename = utils.config.getRegex_rename(group)
        
        os.makedirs(DICCIONARY_PATH, exist_ok=True)
        file_dict = f"{DICCIONARY_PATH}/dictionary.{group}.dict"

        if request.method == 'POST':
            if os.path.exists(file_dict):
                with open(file_dict, 'rb') as config_dictionary_file:    
                    data = pickle.load(config_dictionary_file)
                    #print(data)
            else:
                data = await utils.telegram.get_chat_history(group)
                with open(file_dict, 'wb') as config_dictionary_file:
                    pickle.dump(data, config_dictionary_file)
        else:
            data = await utils.telegram.get_chat_history(group,limit=limit, init=init)
            with open(file_dict, 'wb') as config_dictionary_file:
                pickle.dump(data, config_dictionary_file)

        if request.method == 'POST':
            _regex_download = request.form.get('regex_download').replace('/','')
            _regex_rename = request.form.get('regex_rename')
            _folder_download = request.form.get('folder_download').replace('/','')
            _group = request.form.get('group').replace('/','')

            print(f" [!] POST >>> _regex_download [{_regex_download}]", flush=True)
            print(f" [!] POST >>> _regex_rename [{_regex_rename}]", flush=True)
            print(f" [!] POST >>> _folder_download [{_folder_download}]", flush=True)
    

        regex, rename = utils.config.getFileRename(data,_regex_download,_regex_rename)
        downloaded = utils.db.getDownloaded(group)

    except Exception as e:
        print(f" >>>>>>> Exception [{e}]" ,flush=True)

    if request.method == 'POST':
        page = "telegram_table.html"
    else:
        page = "index.html"

    return render_template(
        page, group=group, data=data, regex=regex, channels=channels, regex_download=_regex_download, folder_download=_folder_download, regex_rename=_regex_rename, rename=rename, downloaded=downloaded
    )


@app.route('/cron')
async def cron():

    global data
    rename = {}
    data = {}

    #data = await utils.telegram.get_chat_history()

   
    regex = {}
    for d in data:
        regex[d.id] = d.id


    channels = utils.config.getChannels()

    return render_template(
        "cron.html", data=data, regex=regex, channels=channels, rename=rename
    )





@app.route('/save/<group>',methods=['POST'])
async def save(group):
    _regex_download = request.form.get('regex_download').replace('/','')
    _regex_rename = request.form.get('regex_rename')
    _folder_download = request.form.get('folder_download')
    _group = request.form.get('group')

    print(f" [!] POST >>> _regex_download [{_regex_download}]", flush=True)
    print(f" [!] POST >>> _regex_rename [{_regex_rename}]", flush=True)
    print(f" [!] POST >>> _folder_download [{_folder_download}]", flush=True)


    _folder_download = utils.config.setDownloadPath(group,_folder_download)
    _regex_download = utils.config.setRegex_download(group,_regex_download)
    _regex_rename = utils.config.setRegex_rename(group,_regex_rename)

    return f"[{group}]"



@app.route('/pyrogram/downloadFile',methods=['POST'])
async def downloadFile():


    try:
        downloaded = False


        _group = request.form.get('group')
        _message_id = request.form.get('message_id')

        print(_group,flush=True)
        print(_message_id,flush=True)


        data = await utils.telegram.downloadFile(_group,_message_id)

        if data: downloaded = utils.db.setDownloaded(_group,_message_id)

        return 'True'
    except Exception as e:
        print(f" >>>>>>> Exception [{e}]" ,flush=True)
        return 'False'











@app.context_processor
def utility_processor():
    def human_readable_size(size, decimal_places=2):
        size = int(size)
        for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
            if size < 1024.0 or unit == "PiB":
                break
            size /= 1024.0
        return f"{size:.{decimal_places}f} {unit}"

    return dict(human_readable_size=human_readable_size)





if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
