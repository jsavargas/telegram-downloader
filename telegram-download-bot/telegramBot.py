import os
import time
import logging
import uvloop
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import get_file_type, format_file_size, create_download_summary  # Importar las funciones desde utils.py
from env import Env  # Importar la clase Config desde Env.py

uvloop.install()

BOT_VERSION = "5.0.0.r5"

# Configurar el logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NoParsingFilter(logging.Filter):
    def filter(self, record):
        return not record.getMessage().startswith('pyrogram.session.session')

logger.addFilter(NoParsingFilter())


# Crear cliente de Pyrogram
#app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN,workers=2,max_concurrent_transmissions=2)
#app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
app = Client("my_bot", api_id=Env.API_ID, api_hash=Env.API_HASH, bot_token=Env.BOT_TOKEN, max_concurrent_transmissions=Env.MAX_CONCURRENT_TRANSMISSIONS)
with app:
    print("my_bot: ")
    app.send_message(Env.AUTHORIZED_USER_ID, "¡El bot se ha iniciado correctamente!")
    logger.info(f"¡El bot se ha iniciado correctamente")

# Crear el directorio de descarga si no existe
DOWNLOAD_DIR = "/download"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

@app.on_message(filters.document | filters.photo | filters.video | filters.audio)
async def download_document(client: Client, message: Message):
    #document = message.document
    #file_name = document.file_name

    logger.info(f"download_document: [{message}]")

    file_name = get_file_type(message)

    # Enviar mensaje de inicio de descarga
    start_msg = await message.reply(f"Iniciando la descarga de **{file_name}**...")

    start_time = time.time()
    start_hour = time.strftime("%H:%M:%S", time.localtime(start_time))

    try:

        # Descarga del archivo
        file_path = await message.download(file_name=os.path.join(DOWNLOAD_DIR, file_name))

        end_time = time.time()
        end_hour = time.strftime("%H:%M:%S", time.localtime(end_time))

        elapsed_time = end_time - start_time
        file_size = os.path.getsize(file_path)
        download_speed = file_size / elapsed_time / 1024  # KB/s

        size_str = format_file_size(file_size)

        # Crear el objeto con la información de la descarga
        download_info = {
            'file_name': file_name,
            'size_str': size_str,
            'start_hour': start_hour,
            'end_hour': end_hour,
            'elapsed_time': elapsed_time,
            'download_speed': download_speed,
            'from': ""
        }

        # Crear el mensaje de resumen utilizando la función de utils
        summary = create_download_summary(download_info)
        logger.info(f"download_document file_path: [{file_path}]")
        logger.info(f"download_document file_name: [{file_name}]")

        # Actualizar el mensaje de inicio con el resumen
        await start_msg.edit_text(summary)
    except Exception as e:
        await start_msg.edit_text(f"Error al descargar **{file_name}**: {str(e)}")


if __name__ == "__main__":
    print("Bot está corriendo...")
    app.run()
