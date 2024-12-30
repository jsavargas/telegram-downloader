import textwrap

class CommandHelp:
    help_text = (
        "Welcome to the bot!\n\n"
        "Available commands:\n"
        "/id - Shows the user/group ID\n"
        "/rename <new_name> - Rename the file from the replied message.\n"
        "/addpath <extension> <path> - Add a download path for a specific file extension.\n"
        "/addgroup <path> - Add a download path for a specific group. Use by replying to a message in the group.\n"
        "/addkeyword <keyword1> <keyword2> ... <path> - Add download paths for messages containing specific keywords or phrases.\n"
        "/delkeyword <keyword1> <keyword2> ... <path> - Remove download paths for messages containing specific keywords or phrases.\n"
        "/addrenamegroup <group_id> - Adds a group ID to the rename group list\n"
        "/delrenamegroup <group_id> - Remove a group ID to the rename group list\n"
        "/pyrogram - Displays the Telethon version\n"
        "/ytdlp - Displays the ytdlp version\n"
        "/version - Displays the bot version"
    )

    ehelp_text = textwrap.dedent('''
        Welcome to the bot!

        Available commands:

        /id - Displays the user/group ID.
            - Usage: Simply type /id and the bot will respond with the ID of the current chat, whether it is a user or a group.
        

        /addpathextension <extension> <NewDirectory> - Crea una regla de ruta de descargad e archivo segun extension
            - Uso: Responde a un mensaje que contenga un archivo con /addpathextension seguido del nuevo nombre que deseas para la carpeta. Si no agregas una ruta
            - Ejemplo: Si recibes un documento y quieres crear una regla para que esos archivos vayan a una carpeta "MiCarpeta", responde al mensaje con /addpathextension MiCarpeta, luego puedes escribir /move para mover el archivo a la nueva ruta creada con /addpathextension
                - /addpathextension 
                - /addpathextension <REPLY> /NuevoDirectorio
                - /addpathextension <extension> /NuevoDirectorio


        /rename <new_name> - Rename the replied message file.
            - Usage: Reply to a message containing a file with /rename followed by the new name you want for the file.
            - Example: If you receive a document and want to rename it to "MyDocument", reply to the message with /rename MyDocument.
                - /rename 
                - /rename /NewDirectory
                - /rename newFileName
                - /rename NewFileName.ext
                - /rename Directory/NewFileName.ext
            - Note: The new name must not contain special characters that are not allowed in file names. You can also use /rename alone and it will rename according to the config.ini file rules


        /move <new_folder> - Mueve el archivo del mensaje respondido.
            - Uso: Responde a un mensaje que contenga un archivo con /move seguido del nuevo nombre que deseas para la carpeta. Si no agregas una ruta, se movera a la carpeta segun las para el archivo o grupo en el archivo config.ini
            - Ejemplo: Si recibes un documento y quieres moverlo a "MiDocumento", responde al mensaje con /move MiDocumento.
                - /move 
                - /move /NuevoDirectorio

        /addgroup <group_id> <new_folder> - Crea una nueva regla para descargar los archivos de este grupo en una carpeta especifica.
            - Uso: Responde a un mensaje que contenga un archivo con /addgroup seguido del nuevo nombre que deseas para la carpeta.
            - Ejemplo: Si recibes un documento y quieres crear una regla para que esos archivos vayan a una carpeta "MiCarpeta", responde al mensaje con /addgroup MiCarpeta, luego puedes escribir /move para mover el archivo a la nueva ruta creada con /addgroup
                - /addgroup 
                - /addgroup <REPLY> /NuevoDirectorio
                - /addgroup <group_id> /NuevoDirectorio

        /delgroup DEVELOP <new_folder> - Crea una nueva regla para descargar los archivos de este grupo en una carpeta especifica.
            - Uso: Responde a un mensaje que contenga un archivo con /addgroup seguido del nuevo nombre que deseas para la carpeta.
            - Ejemplo: Si recibes un documento y quieres crear una regla para que esos archivos vayan a una carpeta "MiCarpeta", responde al mensaje con /addgroup MiCarpeta, luego puedes escribir /move para mover el archivo a la nueva ruta creada con /addgroup
                - /addgroup 
                - /addgroup /NuevoDirectorio


        /addrenamegroup <group_id> - Crea una regla para renombrar archivos en base al texto del mensaje en el archivo a descargar.
            - Uso: Responde a un mensaje que contenga un archivo con /addrenamegroup para que sea agregada una nueva regla en el archivo config.ini.
            - Ejemplo: Si recibes un documento y quieres que su nombre sea el contenido del mensaje, responde al mensaje con /addrenamegroup. Puede usarse despues /rename para renomrar el archivo descargado segun las regla anteriormente creada.
                /addrenamegroup
                /addrenamegroup <group Id>

        /delrenamegroup <group_id> - Crea una regla para renombrar archivos en base al texto del mensaje en el archivo a descargar.
            - Uso: Responde a un mensaje que contenga un archivo con /delrenamegroup para que sea agregada una nueva regla en el archivo config.ini.
            - Ejemplo: Si recibes un documento y quieres que su nombre sea el contenido del mensaje, responde al mensaje con /delrenamegroup. Puede usarse despues /rename para renomrar el archivo descargado segun las regla anteriormente creada.
                /delrenamegroup
                /delrenamegroup <group Id>

        Pronto se agregarán más comandos. ¡Mantente atento!

        Los comandos pueden usarse tanto en chats privados como en chats grupales.
        Asegúrate de que el bot tenga los permisos necesarios para acceder a mensajes y archivos en los chats grupales.
    
    
    
    ''')

    @classmethod
    def get_help(cls):
        return cls.help_text

    @classmethod
    def get_ehelp(cls):
        return cls.ehelp_text
