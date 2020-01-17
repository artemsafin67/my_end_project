"""Решает проблему при сборке единой программы"""

import os
import sys
import logging


def _append_run_path():
    if getattr(sys, 'frozen', False):
        pathlist = []

        pathlist.append(sys._MEIPASS)

        _main_app_path = os.path.dirname(sys.executable)
        pathlist.append(_main_app_path)

        os.environ["PATH"] += os.pathsep + os.pathsep.join(pathlist)

    logging.error("current PATH: %s", os.environ['PATH'])


_append_run_path()
