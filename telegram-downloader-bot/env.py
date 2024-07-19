import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env si existe
load_dotenv()

class Env:
    API_ID = int(os.getenv('API_ID', 'DEFAULT_API_ID'))
    API_HASH = os.getenv('API_HASH', 'DEFAULT_API_HASH')
    BOT_TOKEN = os.getenv('BOT_TOKEN', 'DEFAULT_BOT_TOKEN')
    AUTHORIZED_USER_ID = int(os.getenv('AUTHORIZED_USER_ID', '0'))
    PUID = int(os.getenv('PUID', '1001'))
    PGID = int(os.getenv('PGID', '1001'))
    MAX_CONCURRENT_TRANSMISSIONS = int(os.getenv('MAX_CONCURRENT_TRANSMISSIONS', '2'))

    IS_DELETE = os.getenv('IS_DELETE', False)
    IS_DELETE = bool(IS_DELETE) if isinstance(IS_DELETE, str) and IS_DELETE.lower() in ["true", "1"] else IS_DELETE

    DOWNLOAD_DIR = "/download"
    WELCOME="WELCOME"



    