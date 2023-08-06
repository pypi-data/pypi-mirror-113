import logging
import colorama
colorama.init()


class CustomFormatter(logging.Formatter):
    grey = colorama.Fore.CYAN
    magenta = colorama.Fore.MAGENTA
    yellow = colorama.Fore.YELLOW
    red = colorama.Fore.RED
    reset = colorama.Fore.RESET
    format = "%(levelname)s | %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: magenta + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
