# -*- coding: utf-8 -*-

import sys
from collections.abc import Iterable
from importlib import import_module
from time import time

from loguru import logger


def preimport(*moduleNames):
    for moduleName in moduleNames:
        if isinstance(moduleName, str):
            if moduleName in sys.modules:
                logger.info("[Note]:{} already imported.".format(moduleName))
            else:
                timeStart = time()
                try:
                    import_module(moduleName)
                except ModuleNotFoundError:
                    logger.warning("import {} ... ".format("'" + moduleName + "'") + " ModuleNotFound.")
                except:
                    logger.error("import {} ... ".format("'" + moduleName + "'") + "Unexpected error happened")
                else:
                    logger.info("import {} ... ".format("'" + moduleName + "'") + " successfully in {:.2}s.".format(
                        time() - timeStart))
        elif isinstance(moduleName, Iterable):
            preimport(*moduleName)
        else:
            logger.error("import error, moduleName must be str or Iterable.")
