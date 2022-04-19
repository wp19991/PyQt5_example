from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon
from loguru import logger

from config.core import Config
from core.MySystemTrayIcon import MySystemTrayIcon
from ui.main_window import Ui_MainWindow as main_window
from utils.CommonHelper import CommonHelper
from win.login_form import login_form


class main_win(QMainWindow, main_window):
    def __init__(self):
        super(main_win, self).__init__()
        self.setupUi(self)

        self.config = Config.current()  # 读取配置文件
        self.setStyleSheet(CommonHelper.read_qss_file(self.config.getSec("general")["skin"]))

        self.config.getSec("advance")["autoexportqss"] = "1seees"
        self.config.saveDefault()  # 保持配置文件

        # 隐藏原始的框
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 登录界面
        self.login = login_form(self)
        self.login.show()

        # 程序托盘图标
        self.tray_icon = MySystemTrayIcon()
        self.tray_icon.init(self)  # 将自己传进去

    # 重写关闭的逻辑
    def closeEvent(self, event):
        logger.info("关闭主窗口")
        if self.is_min_status_checkBox.isChecked():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Tray Program",
                "Application was minimized to Tray",
                QSystemTrayIcon.Information,
                2000
            )
