import sys
import os
from PyQt5.QtWidgets import QApplication

from config import logs
from win.splash.splash import SplashScreen
from loguru import logger

os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class App(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.windows = {}

    def run(self, pytest=False):
        logger.info("程序启动 ...")

        splash = SplashScreen()  # 启动界面
        splash.loadProgress()  # 启动界面

        from win.main_win import main_win
        self.windows["main"] = main_win()
        # self.windows["main"].show() # 先显示登录界面
        # 默认先显示登录界面

        splash.finish(self.windows["main"])  # 启动界面

        if not pytest:
            sys.exit(self.exec_())


if __name__ == "__main__":
    logs.setting()
    App().run()
