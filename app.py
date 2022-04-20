import sys
import os
from PyQt5.QtWidgets import QApplication
from loguru import logger

from utils import global_var as gl
from config import logs
from win.login_form import login_form
from win.splash.splash import SplashScreen

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
        # 默认先显示登录界面
        # self.windows["main"].show()
        # 如果需要登录界面，就打开下面的注释，把上面self.windows["main"].show()注释掉
        self.windows["login"] = login_form(self.windows["main"])
        self.windows["login"].show()

        splash.finish(self.windows["main"])  # 启动界面

        if not pytest:
            sys.exit(self.exec_())


if __name__ == "__main__":
    logs.setting()  # log 设置
    gl.__init()  # 全局变量
    App().run()
