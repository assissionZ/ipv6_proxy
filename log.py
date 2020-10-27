# coding:utf8
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warn': logging.WARNING,
          'error': logging.ERROR,
          'fatal': logging.CRITICAL}


def Singleton(cls):
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@Singleton
class MyLogger:
    __logger = None

    def __init__(self, level="info"):
        # 写死了日志路径
        logfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log/server.log")
        root_path, file_name = os.path.split(logfile)
        if not os.path.exists(root_path):
            os.makedirs(root_path)
        MyLogger.__logger = logging.getLogger(logfile)
        setval = LEVELS.get(level.lower(), logging.WARNING)
        MyLogger.__logger.setLevel(setval)

        # 这里设置一天一个日志，最多保留30天
        ch = TimedRotatingFileHandler(logfile, when='MIDNIGHT', interval=1, backupCount=30)
        format = '%(asctime)s | %(levelname)s | %(message)s'
        fmt = logging.Formatter(format)
        ch.setFormatter(fmt)
        MyLogger.__logger.addHandler(ch)

    def details(self, msg, depth=1):
        file = os.path.basename(sys._getframe(depth).f_back.f_code.co_filename)
        co_name = sys._getframe(depth).f_back.f_code.co_name
        line_num = sys._getframe(depth).f_back.f_lineno
        info = "%s - %s line:%s" % (file, co_name, line_num)
        return "%s | %s" % (info, msg)

    def debug(self, *msg):
        msg_ = self.deal_msg(*msg)
        MyLogger.__logger.debug(self.details(msg_))

    def info(self, *msg):
        msg_ = self.deal_msg(*msg)
        MyLogger.__logger.info(self.details(msg_))

    def warn(self, *msg):
        msg_ = self.deal_msg(*msg)
        MyLogger.__logger.warn(self.details(msg_))

    def error(self, *msg):
        msg_ = self.deal_msg(*msg)
        MyLogger.__logger.error(self.details(msg_))

    def fatal(self, *msg):
        msg_ = self.deal_msg(*msg)
        MyLogger.__logger.critical(self.details(msg_))

    def deal_msg(self, *msg):
        para = []
        for i in msg:
            para.append(str(i))
        msg_ = " ".join(para)
        return msg_
