# utils.py
import os
import re
import time
import shutil
from env import Env

class Utils:
    def __init__(self):

        self.env = Env()
        self.permissions_folder = 0o777
        self.permissions_file = 0o755
        self.PUID = self.env.PUID 
        self.PGID = self.env.PGID
        self.change_permissions()


    @staticmethod
    def format_file_size(self, file_size: int) -> str:
        if file_size < 1024:
            return f"{file_size} bytes"
        elif file_size < 1024 * 1024:
            return f"{file_size / 1024:.2f} KB"
        else:
            return f"{file_size / (1024 * 1024):.2f} MB"


    @staticmethod
    def format_duration(seconds):
        """Format duration to human-readable format."""
        duration = timedelta(seconds=seconds)
        days = duration.days
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if days > 0:
            return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
        elif hours > 0:
            return f"{hours} hours, {minutes} minutes, {seconds} seconds"
        elif minutes > 0:
            return f"{minutes} minutes, {seconds} seconds"
        else:
            return f"{seconds} seconds"

    def create_download_summary(self, download_info):
        """
        Creates a download summary message based on the download information.

        Args:
        - download_info (dict): Dictionary with the following structure:
            {
                'file_name': str,
                'size_str': str,
                'start_hour': str,
                'end_hour': str,
                'elapsed_time': float,
                'download_speed': float,
                'origin_group': str or None (optional)
            }
        
        Returns:
        - str: Formatted download summary message.
        """
        file_name = download_info['file_name']
        download_folder = download_info['download_folder']
        size_str = download_info['size_str']
        start_hour = download_info['start_hour']
        end_hour = download_info['end_hour']
        elapsed_time = download_info['elapsed_time']
        download_speed = download_info['download_speed']
        origin_group = download_info.get('origin_group', None)
        retries = download_info.get('retries', None)
        media_group_id = download_info['message'].media_group_id if download_info['message'].media_group_id else None

        summary = (
            f"**Download completed**\n\n"
            f"**File Name:** {file_name}\n"
            f"**Download Folder:** {download_folder}\n"
            f"**File Size:** {size_str}\n"
            f"**Start Time:** {start_hour}\n"
            f"**End Time:** {end_hour}\n"
            f"**Download Time:** {elapsed_time:.2f} seconds\n"
            f"**Download Speed:** {download_speed:.2f} KB/s"
        )

        if origin_group:
            summary += f"\n**Origin Group:** {origin_group}"
        if retries:
            summary += f"\n**Retries:** {retries}"
        #if media_group_id:
        #    summary += f"\n**media group id:** {media_group_id}"

        return summary

    def removeFiles(self):
        if os.path.exists("telegramBot.session"): 
            os.remove("telegramBot.session")

    def change_permissions(self):
        os.chown(self.env.DOWNLOAD_PATH, self.PUID, self.PGID)

    def change_permissions_owner(self, file_name):
        """Changes the permissions and owner of the specified file."""
        try:
            if os.path.isfile(file_name): os.chmod(file_name, self.permissions_file)
            elif os.path.isdir(file_name): os.chmod(file_name, self.permissions_folder)
            else: os.chmod(file_name, self.permissions_file)
            os.chown(file_name, self.PUID, self.PGID)
            print(f"Successfully changed permissions and owner of {file_name}")
        except Exception as e:
            print(f"Failed to change permissions and owner: {e}")

    def getDownloadFolder(self, file_name):

        download_folder = self.env.DOWNLOAD_COMPLETED_PATH
        final_path = os.path.join(self.env.DOWNLOAD_COMPLETED_PATH, file_name)

        try:
            if file_name.endswith(".torrent"):
                download_folder = self.env.DOWNLOAD_PATH_TORRENTS
    
            # Create the download folder if needed
            self.create_folders(download_folder)

            # Construct the final path
            final_path = os.path.join(download_folder, file_name)

            print(f"getDownloadFolder: download_folder: {download_folder}, final_path: {final_path}")  # Enhanced logging

            return download_folder, final_path

        except Exception as e:
            print(f"getDownloadFolder Failed: {e}")
            return download_folder, final_path

    def getDownloadFolderTemp(self, file_name):
        final_path = os.path.join(self.env.DOWNLOAD_INCOMPLETED_PATH, file_name)
        try:
            self.create_folders(final_path)
            return final_path
        except Exception as e:
            print(f"getDownloadFolderTemp Failed: {e}")
            return final_path

    def create_folders(self, folder_name):
        try:
            print(f"create_folders folder_name: {folder_name}")
            # Verificar si la folder_name es un archivo
            if os.path.isfile(folder_name):
                print(f"create_folders isfile: {folder_name}")
                base_directory = os.path.dirname(folder_name)
                os.makedirs(base_directory, exist_ok=True) 
                self.change_permissions_owner(base_directory)
            elif os.path.isdir(folder_name):
                print(f"create_folders isdir: {folder_name}")
                os.makedirs(folder_name, exist_ok=True) 
                self.change_permissions_owner(folder_name)
            else:
                print(f"create_folders else: {folder_name}")
                dirname = os.path.dirname(folder_name)
                base_directory = os.path.basename(folder_name)
                if "." not in base_directory:
                    print(f"create_folders else: {folder_name}")
                    os.makedirs(folder_name, exist_ok=True) 
                else:
                    print(f"create_folders else: {dirname}")
                    os.makedirs(dirname, exist_ok=True) 
        except FileExistsError as e:
            print(f"The folder {folder_name} already exists: {e}")
        except Exception as e:
            print(f"create_folders Exception: {folder_name}: {e}")

    def startTime(self):
        start_time = time.time()
        start_hour = time.strftime("%H:%M:%S", time.localtime(start_time))

        return start_time, start_hour

    def endTime(self):
        end_time = time.time()
        end_hour = time.strftime("%H:%M:%S", time.localtime(end_time))

        return end_time, end_hour

    def elapsedTime(self, start_time, end_time):
        elapsed_time = end_time - start_time
        
        return elapsed_time
        
    def getSize(self, file_path):
        size_str = ""
        try:
            file_size = os.path.getsize(file_path)

            if file_size < 1024:
                size_str = f"{file_size} bytes"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.2f} KB"
            else:
                size_str = f"{file_size / (1024 * 1024):.2f} MB"

        except Exception as e:
            print(f"getSize Exception: {file_path}: {e}")
            file_size = 0
        return file_size, size_str

    def moveFile(self, old_filename, new_filename):

        ## TODO
        ## leer el archivo config.ini por si ya existe la regla para este group_id
        ## 

        try:
            if os.path.exists(old_filename): 
                self.create_folders(os.path.dirname(new_filename))
                move = shutil.move(old_filename, new_filename)
                return move
            else:
                return None
        except Exception as e:
            print(f"moveFile Exception: [{old_filename}] [{new_filename}]: {e}")
            return None
    
    def moveFileFolder(self, group_id, file_name_download):

        ## TODO
        ## leer el archivo config.ini por si ya existe la regla para este group_id
        ## 

        try:
            if os.path.exists(file_name_download): 
                _group_id = str(group_id).replace('-','')
                create_folders = os.path.join(self.env.DOWNLOAD_PATH, _group_id)
                self.create_folders(create_folders)
                move = shutil.move(file_name_download, create_folders)
                return move

        except Exception as e:
            print(f"moveFile Exception: [{group_id}] [{file_name_download}]: {e}")
            return None
    
    def createGroupFolder(self, group_id):

        try:
            if group_id.startswith("/"):
                print(f"createGroupFolder startswith: [{group_id}]")
                self.create_folders(group_id)
                return group_id
            else:
                _group_id = str(group_id).replace('-','')
                create_folders = os.path.join(self.env.DOWNLOAD_PATH, _group_id)
                self.create_folders(create_folders)
                return create_folders

            ## TODO
            ## crear el registro en config.ini
            ## 


        except Exception as e:
            print(f"moveFile Exception: [{group_id}]: {e}")
            return None

    def format_size(self, size_in_bytes):
        """Convert size in bytes to a human-readable format."""
        if size_in_bytes < 1024:
            return f"{size_in_bytes} bytes"
        elif size_in_bytes < 1024**2:
            return f"{size_in_bytes / 1024:.2f} KB"
        elif size_in_bytes < 1024**3:
            return f"{size_in_bytes / 1024**2:.2f} MB"
        else:
            return f"{size_in_bytes / 1024**3:.2f} GB"

    def format_duration(self, duration_in_seconds):
        """Convert duration in seconds to a human-readable format including hours, minutes, and seconds."""
        if duration_in_seconds < 60:
            return f"{duration_in_seconds:.2f} seconds"
        elif duration_in_seconds < 3600:
            minutes = int(duration_in_seconds // 60)
            seconds = int(duration_in_seconds % 60)
            return f"{minutes} minute(s) and {seconds} second(s)"
        else:
            hours = int(duration_in_seconds // 3600)
            minutes = int((duration_in_seconds % 3600) // 60)
            seconds = int(duration_in_seconds % 60)
            return f"{hours} hour(s), {minutes} minute(s), and {seconds} second(s)"

    def replace_chars_with_underscore(self, s: str, chars_to_replace: str) -> str:
        pattern = '[' + re.escape(chars_to_replace) + ']'
        return re.sub(pattern, '_', s)


    def combine_paths(self, path1, path2):
        # Eliminar posibles barras diagonales finales de path2
        #path2 = path2.rstrip('/')
        pattern = r'^.*\.[A-Za-z]{2,4}$'

        # Extraer el nombre del archivo y la extensión de path1
        base_name = os.path.basename(path1)
        ext = os.path.splitext(base_name)[1]
        file_name = os.path.splitext(base_name)[0]

        if path2.startswith('/'):
            if not re.match(pattern, path2):
                print("!!!!! ACA")
                return os.path.join(base_name, path2,  file_name + ext)

            # Si path2 empieza con '/', considera path2 como la ruta completa
            if ext:  # Si path2 termina en extensión
                return path2
            else:  # Si path2 es solo una ruta
                return os.path.join(path2, file_name + ext)
        else:
            if path2.endswith('/'):
                return os.path.join(os.path.dirname(path1), path2, base_name)

            elif not re.match(pattern, path2):
                print("!!!!! ACA 2 ")
                return os.path.join(os.path.dirname(path1), path2+ext)



            # Si path2 no empieza con '/', es una ruta relativa o nombre de archivo
            if '.' in path2:
                # path2 es un nombre de archivo con extensión
                return os.path.join(os.path.dirname(path1), path2)
            else:
                # path2 es una ruta relativa sin extensión
                return os.path.join(os.path.dirname(path1), path2, base_name)




if __name__ == '__main__':

    utils = Utils()

    old_filename = '/download/mobi/El golem - Gustav Meyrink.mobi'
    
    
    new_filename = '/lololo/lilili/lala'
    new_filename = 'lala/tototo.txt'
    new_filename = 'lala/tototo'
    new_filename = '/lololo/lilili/lala'
    new_filename = '/lololo/lilili/lala.txt'
    new_filename = 'lololo/lilili/lala'
    new_filename = 'lololo/lilili/lala.txt'
    new_filename = '/lala.txt'
    new_filename = 'lala'
    new_filename = 'lala.txt'
    new_filename = '/lala'
    new_filename = 'Directorio/NuevoNombreDeArchivo.ext'
    new_filename = '/lala/'
    


    newfilename = utils.combine_paths(old_filename, new_filename)
    print(f"newfilename:: {newfilename}")