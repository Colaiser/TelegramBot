import ctypes
import datetime
import enum
import os
import re
import sys
import threading
from ctypes import ArgumentError
from re import RegexFlag

if sys.platform == "win32":
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

FILE_NAME = 'app.log'
FILE = open(FILE_NAME, 'a', encoding='utf-8')
pid = str(os.getpid()).ljust(5)

RESET_COLOR = '\033[0m'

DEBUG_COLOR = '\033[36m'
INFO_COLOR = '\033[32m'
WARNING_COLOR = '\033[33m'
ERROR_COLOR = '\033[31m'

LOCK = threading.Lock()


class LEVEL(enum.IntEnum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


__console_level__ = LEVEL.INFO
__file_level__ = LEVEL.DEBUG


def prefix(level: str):
    level = level.ljust(7)
    return f"[{datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}] [{__name__} {pid}] [{level}]"


def set_console_level(level: LEVEL):
    if type(level) is LEVEL:
        global __console_level__
        __console_level__ = level
    else:
        raise ArgumentError()


def set_file_level(level: LEVEL):
    if type(level) is LEVEL:
        global __file_level__
        __file_level__ = level
    else:
        raise ArgumentError()


def log(color: str, level: LEVEL, level_str: str, *args, **kwargs):
    if level.value >= __console_level__:
        LOCK.acquire()

        try:
            print(' ' + color + prefix(level_str) + ' ', end='')
            print(*args, **kwargs)
            print(RESET_COLOR, end='')
        except:
            pass

        LOCK.release()

    if level.value >= __file_level__:
        try:
            print(prefix(level_str) + ' ', end='', file=FILE)
            print(*args, **kwargs, file=FILE)
        except:
            print('!!! FAILED TO LOG DATA !!!', file=FILE)

        FILE.flush()


def debug(*args, **kwargs):
    log(DEBUG_COLOR, LEVEL.DEBUG, 'DEBUG', *args, **kwargs)


def info(*args, **kwargs):
    log(INFO_COLOR, LEVEL.INFO, 'INFO', *args, **kwargs)


def warning(*args, **kwargs):
    log(WARNING_COLOR, LEVEL.WARNING,
        'WARNING', *args, **kwargs)


def error(*args, **kwargs):
    log(ERROR_COLOR, LEVEL.ERROR, 'ERROR', *args, **kwargs)


def get_errors():
    reg = r'\[ERROR\s*\]\s*(?P<msg>.+)$'

    file = open(FILE_NAME, 'r')
    text = file.read()

    matches = re.findall(reg, text, RegexFlag.MULTILINE)

    completed = []

    for item in matches:
        completed.append(item)

    return str(completed[len(completed) - 1])