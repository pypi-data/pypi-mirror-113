import time
# from config import logger_path


class Logger(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def _write_log(self, level, msg, console_log=True):
        with open(self.file_name, "a") as log_file:
            log_msg = "{0} ### [{1}] ### {2}\n".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                       level, msg.replace('\n', ' '))
            log_file.write(log_msg)
            log_file.close()
            if console_log:
                print(log_msg)

    def critical(self, msg, console_log=True):
        self._write_log("CRITICAL", msg, console_log=True)

    def error(self, msg, console_log=True):
        self._write_log("ERROR", msg, console_log=True)

    def warn(self, msg, console_log=True):
        self._write_log("WARN", msg, console_log=True)

    def info(self, msg, console_log=True):
        self._write_log("INFO", msg, console_log=True)

    def output(self, msg, console_log=True):
        self._write_log("OUTPUT", msg, console_log=True)


# logger = Logger(logger_path)
