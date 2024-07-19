# variable_printer.py
from env import Env

class PartialPrinter:
    def __init__(self, constants=[]):
        self.env = Env()

    def print_variable(self, variable_name, variable_value):
        """Prints the variable name and its value in the desired format."""
        print(f"{variable_name:<30}: {variable_value}")

    def print_partial_value(self, variable_name, variable_value):
        """Prints the variable name and half of its value, padded with asterisks."""
        if isinstance(variable_value, str):
            half_len = len(variable_value) // 2
            masked_value = variable_value[:half_len] + "*" * (len(variable_value) - half_len)
        elif isinstance(variable_value, (int, float)):
            masked_value = str(variable_value)[:int(len(str(variable_value)) / 2)] + "*" * (
                len(str(variable_value)) - int(len(str(variable_value)) / 2)
            )
        else:
            raise TypeError(f"Unsupported type for variable_value: {type(variable_value)}")
        print(f"{variable_name:<30}: {masked_value}")

    def print_variables(self):
        self.print_partial_value("API_ID", self.env.API_ID)
        self.print_partial_value("API_HASH", self.env.API_HASH)
        self.print_partial_value("BOT_TOKEN", self.env.BOT_TOKEN)
        self.print_partial_value("AUTHORIZED_USER_ID", self.env.AUTHORIZED_USER_ID)
        self.print_variable("DOWNLOAD_DIR", self.env.DOWNLOAD_PATH)
        self.print_variable("DOWNLOAD_COMPLETED_PATH", self.env.DOWNLOAD_COMPLETED_PATH)
        self.print_variable("DOWNLOAD_INCOMPLETED_PATH", self.env.DOWNLOAD_INCOMPLETED_PATH)
        self.print_variable("DOWNLOAD_PATH_TORRENTS", self.env.DOWNLOAD_PATH_TORRENTS)
