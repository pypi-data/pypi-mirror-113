from .level import *

class Loger:
    def __init__(self):
        self.to_file = False
        self.log_file = "log.txt"
        self.level = WARNING #日志记录级别
        self.format = "{level}: {msg}"
    def __format_msg(self, level, msg):
        """格式化msg"""
        msg = self.format.replace("{msg}", msg)
        if level == DEBUG:
            msg = msg.replace("{level}", "DEBUG")
        elif level == INFO:
            msg = msg.replace("{level}", "INFO")
        elif level == WARNING:
            msg = msg.replace("{level}", "WARNING")
        elif level == ERROR:
            msg = msg.replace("{level}", "ERROR")
        return msg
    def __write_log_file(self, msg):
        """将日志写入文件"""
        with open(self.log_file, "a") as f:
            f.write(msg)
            f.write("\n")
    def debug(self, msg):
        if DEBUG >= self.level:
            msg = self.__format_msg(DEBUG, msg)
            print(msg)
            self.__write_log_file(msg)
    def info(self, msg):
        if INFO >= self.level:
            msg = self.__format_msg(INFO, msg)
            print(msg)
            self.__write_log_file(msg)
    def warning(self, msg):
        if WARNING >= self.level:
            msg = self.__format_msg(WARNING, msg)
            print(msg)
            self.__write_log_file(msg)
    def error(self, msg):
        if ERROR >= self.level:
            msg = self.__format_msg(ERROR, msg)
            print(msg)
            self.__write_log_file(msg)
