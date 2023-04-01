import os

VERSION = "1.1.5"

# Bot information
SESSION     = os.environ.get('SESSION', 'pdf2img')
APP_ID      = int(os.environ['APP_ID'])
API_HASH    = os.environ['API_HASH']
BOT_TOKEN   = os.environ['BOT_TOKEN']

ACCOUNT_NAME = "my_account"
DOWNLOAD_NAME = "account_down"


PATH_CONFIG = os.environ.get('PATH_CONFIG', '/config') 
PATH_DOWNLOAD = os.environ.get('PATH_DOWNLOAD', '/download') 
PATH_INCOMPLETED = "incompleted"
PATH_COMPLETED = "completed"

PUID     = os.environ.get('PUID', None)
PGID     = os.environ.get('PGID', None)


DOWNLOAD_INCOMPLETED = os.getenv('DOWNLOAD_INCOMPLETED') or os.path.join(PATH_DOWNLOAD,PATH_INCOMPLETED)
DOWNLOAD_COMPLETED = os.getenv('DOWNLOAD_COMPLETED') or os.path.join(PATH_DOWNLOAD,PATH_COMPLETED)
PATH_DICTIONARY = os.path.join(PATH_CONFIG,'dictionary')


SESSION = os.path.join(PATH_CONFIG,ACCOUNT_NAME)
SESSION_DOWN = os.path.join(PATH_CONFIG,DOWNLOAD_NAME)

LOCKFILE = f"{SESSION}.session-journal"
LOCKFILE_DOWN = f"{SESSION_DOWN}.session-journal"

