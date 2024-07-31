import logging

# Configurar el logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Obtener el logger principal
logger = logging.getLogger(__name__)

# Obtener el logger de Pyrogram y establecer su nivel de logging a ERROR
pyrogram_logger = logging.getLogger("pyrogram")
pyrogram_logger.setLevel(logging.WARNING)  # Solo advertencias y errores
