import os
import time
import logging
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import get_file_type, format_file_size  # Importar las funciones desde utils.py

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

# Cargar variables de entorno desde el archivo .env si existe
load_dotenv()

# Leer variables de entorno o usar valores por defecto
API_ID = int(os.getenv('API_ID', 'DEFAULT_API_ID'))
API_HASH = os.getenv('API_HASH', 'DEFAULT_API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN', 'DEFAULT_BOT_TOKEN')
AUTHORIZED_USER_ID = int(os.getenv('AUTHORIZED_USER_ID', '0'))

# Crear cliente de Pyrogram
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN,workers=2,max_concurrent_transmissions=2)
with app:
    print("my_bot: ")
    app.send_message(AUTHORIZED_USER_ID, "¡El bot se ha iniciado correctamente!")
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

        size_str = format_file_size

        # Crear el mensaje de resumen
        summary = (
            f"**Descarga completada**\n\n"
            f"**Nombre del archivo:** {file_name}\n"
            f"**Tamaño del archivo:** {size_str}\n"
            f"**Hora de inicio:** {start_hour}\n"
            f"**Hora de finalización:** {end_hour}\n"
            f"**Tiempo de descarga:** {elapsed_time:.2f} segundos\n"
            f"**Velocidad de descarga:** {download_speed:.2f} KB/s"
        )
    
        logger.info(f"download_document file_path: [{file_path}]")
        logger.info(f"download_document file_name: [{file_name}]")

        # Actualizar el mensaje de inicio con el resumen
        await start_msg.edit_text(summary)
    except Exception as e:
        await start_msg.edit_text(f"Error al descargar **{file_name}**: {str(e)}")


if __name__ == "__main__":
    print("Bot está corriendo...")
    app.run()
