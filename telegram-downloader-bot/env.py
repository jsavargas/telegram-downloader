import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env si existe
load_dotenv()

class Env:
    def __init__(self):

        self.API_ID = int(os.getenv('API_ID', 'DEFAULT_API_ID'))
        self.API_HASH = os.getenv('API_HASH', 'DEFAULT_API_HASH')
        self.BOT_TOKEN = os.getenv('BOT_TOKEN', 'DEFAULT_BOT_TOKEN')
        self.AUTHORIZED_USER_ID = int(os.getenv('AUTHORIZED_USER_ID', '0'))
        self.PUID = int(os.getenv('PUID', '1001'))
        self.PGID = int(os.getenv('PGID', '1001'))
        self.MAX_CONCURRENT_TRANSMISSIONS = int(os.getenv('MAX_CONCURRENT_TRANSMISSIONS', '2'))

        self.IS_DELETE = os.getenv('IS_DELETE', False)
        self.IS_DELETE = bool(self.IS_DELETE) if isinstance(self.IS_DELETE, str) and self.IS_DELETE.lower() in ["true", "1"] else self.IS_DELETE

        self.DOWNLOAD_PATH = os.environ.get("DOWNLOAD_PATH", "/download")
        self.DOWNLOAD_COMPLETED_PATH = os.path.join(self.DOWNLOAD_PATH, "completed")
        self.DOWNLOAD_INCOMPLETED_PATH = os.path.join(self.DOWNLOAD_PATH, "incompleted")
        self.DOWNLOAD_PATH_TORRENTS = os.environ.get("DOWNLOAD_PATH_TORRENTS", "/watch")  # fmt: skip


        self.WELCOME="WELCOME"



    