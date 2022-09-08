import configparser
import os
import re



CONFIG_PATH = '/config'
DOWNLOAD_PATH = '/download'

CONFIG = f'{CONFIG_PATH}/config.ini'
CLIENT_NAME = f'{CONFIG_PATH}/my_account'
DICCIONARY_PATH = f'{CONFIG_PATH}/dictionary'

_INIT = None
_LIMIT = 30

config = configparser.ConfigParser(allow_no_value=True)

def read_config_file():

    if not os.path.exists(CONFIG):
        print(f'CREATE DEFAULT CONFIG FILE : {CONFIG}')

        config.read(CONFIG)

        config['DEFAULT_PATH'] = {}
        config['DEFAULT_PATH']['grupo_name_1'] = '/download'

        config['CHANNELS'] = {}
        config['CHANNELS']['grupo_name_1'] = None

        config['REGEX_RENAME'] = {}
        config['REGEX_RENAME']['grupo_name_1'] = '/grupo_name.+?(\d{1}).+?(\w{3}$)/0\\1.\\2/'

        config['REGEX_DOWNLOAD'] = {}
        config['REGEX_DOWNLOAD']['grupo_name_1'] = 'grupo_name _ Capítulo'

        with open(CONFIG, 'w') as configfile:    # save
            config.write(configfile)
        return config

    else:
        config.read(CONFIG)
        return config

def getChannels():
    config = read_config_file()

    CHANNELS = config['CHANNELS']

    return CHANNELS


def getDownloadPath(channel):

    try:
        config = read_config_file()
        folderFlag=False

        DEFAULT_PATH = config['DEFAULT_PATH']
        for ID in DEFAULT_PATH:
            if str(ID).lower() == str(channel).lower():
                _DOWNLOAD_PATH = DEFAULT_PATH[ID]
                folderFlag=True
                break
        
        if folderFlag: return _DOWNLOAD_PATH
        else: return DOWNLOAD_PATH
    except Exception as e:
        print(f" >>>>>>> Exception getDownloadPath [{e}]" ,flush=True)
        return DOWNLOAD_PATH

def getRegex_download(channel):
    _regex = ''

    try:
        #print(f"getRegex_download >> [{channel}]",flush=True)
        config = read_config_file()

        REGEX_DOWNLOAD = config['REGEX_DOWNLOAD']
        for REGEX in REGEX_DOWNLOAD:
            #print(f"getRegex_download || [{REGEX}]", flush=True)
            if str(channel).lower() == str(REGEX).lower():
                _regex = REGEX_DOWNLOAD[REGEX]
                break

        return _regex
    except Exception as e:
        print(f" >>>>>>> Exception getRegex_download [{e}]" ,flush=True)
        return _regex


def getRegex_rename(channel):
    _regex = ''

    try:
        #print(f"getRegex_download >> [{channel}]",flush=True)
        config = read_config_file()

        REGEX_RENAME = config['REGEX_RENAME']
        for REGEX in REGEX_RENAME:
            #print(f"REGEX_RENAME || [{REGEX}]", flush=True)
            if str(channel).lower() == str(REGEX).lower():
                _regex = REGEX_RENAME[REGEX]
                break

        return _regex
    except Exception as e:
        print(f" >>>>>>> Exception getRegex_rename [{e}]" ,flush=True)
        return _regex

def getFileRename(data,_regex_download,_regex_rename):

    regex = {}
    rename = {}

    try:
        for d in data:
            if d.video.file_name == None: 
                filename = d.caption
            else:
                filename = d.video.file_name

            if re.match(_regex_download, filename,re.I):
                regex[d.id] = True
                mrr = re.match('/(.*)/(.*)/', _regex_rename)
                if mrr: 
                    filename_rename = re.sub(mrr.group(1), mrr.group(2), filename, flags=re.I)
                    #print(f"filename_rename [{filename_rename}]", flush=True)
                    rename[d.id] = filename_rename
                else: rename[d.id] = filename
            else:
                regex[d.id] = False

        return regex,rename
    except Exception as e:
        print(f" >>>>>>> Exception getFileRename [{e}]" ,flush=True)
        return regex, rename

def getFileRename2(data,_regex_download,_regex_rename):

    regex = {}
    rename = {}

    try:
        for d in data:

            if d.file_name == None: 
                filename = d.caption
            else:
                filename = d.file_name

            if re.match(_regex_download, filename,re.I):
                regex[d.id] = True
                mrr = re.match('/(.*)/(.*)/', _regex_rename)
                if mrr: 
                    filename_rename = re.sub(mrr.group(1), mrr.group(2), filename, flags=re.I)
                    #print(f"filename_rename [{filename_rename}]", flush=True)
                    rename[d.id] = filename_rename
                else: rename[d.id] = filename
            else:
                regex[d.id] = False

        return regex,rename
    except Exception as e:
        print(f" >>>>>>> Exception getFileRename [{e}]" ,flush=True)
        return regex, rename

def setDownloadPath(channel, value):
    config = read_config_file()

    print(f"setDownloadPath >> [{channel}][{value}]",flush=True)

    if not os.path.abspath(value) == os.path.abspath(DOWNLOAD_PATH) :
        if value == '': value = DOWNLOAD_PATH
        #print(f"IIFFFF setDownloadPath >> [{channel}][{os.path.abspath(value)}]",flush=True)

        #config.add_section('DEFAULT_PATH')
        
        config['DEFAULT_PATH'][channel] = os.path.abspath(value)

        with open(CONFIG, 'w') as configfile:
            config.write(configfile)


    return value

def setRegex_download(channel, value):
    print(f"setRegex_download >> [{channel}][{value}]",flush=True)

    if not value == '':
        config = read_config_file()

        config['REGEX_DOWNLOAD'][channel] = value

        with open(CONFIG, 'w') as configfile:
            config.write(configfile)


    return value

def setRegex_rename(channel, value):
    print(f"setRegex_rename >> [{channel}][{value}]",flush=True)

    if not value == '':
        config = read_config_file()

        config['REGEX_RENAME'][channel] = value

        with open(CONFIG, 'w') as configfile:
            config.write(configfile)


    return value



def getRegexFilename(group,file_name):

    try:

        _regex_rename = getRegex_rename(group)
        mrr = re.match('/(.*)/(.*)/', _regex_rename)
        if mrr:
            filename_rename = re.sub(mrr.group(1), mrr.group(2), file_name, flags=re.I)
            return filename_rename
        else: return file_name

      


    except Exception as inst:
        print("Exception config getRegexFilename ", flush=True)    # the exception instance
        print(type(inst) , flush=True)    # the exception instance
        print(inst.args , flush=True)     # arguments stored in .args
        print(inst , flush=True)          # __str__ allows args to be printed directly,




    return file_name