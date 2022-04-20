from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import QFrame, QMainWindow, QApplication
from loguru import logger

from ui.login_form import Ui_Frame as ui_form
from utils import global_var as gl


class login_form(ui_form, QFrame):
    def __init__(self, parent: QMainWindow = None):
        super(login_form, self).__init__()
        self.setupUi(self)
        self.root = parent
        self.root.tray_icon.hide()  # 先隐藏托盘图标

        # 加载字体
        QtGui.QFontDatabase.addApplicationFont("res/Social Media Circled.otf")

        # 隐藏原始的框
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 按钮事件绑定
        self.close_pushButton.clicked.connect(self.close_event)
        self.min_pushButton.clicked.connect(self.showMinimized)

        self.login_pushButton.clicked.connect(self.login_pushButton_event)
        self.forget_password_pushButton.clicked.connect(self.forget_password_pushButton_event)
        self.register_pushButton.clicked.connect(self.register_pushButton_event)

        # 底部按钮
        self.github_pushButton.clicked.connect(self.github_pushButton_event)
        self.phone_pushButton.clicked.connect(self.phone_pushButton_event)
        self.email_pushButton.clicked.connect(self.email_pushButton_event)

    # 关闭的逻辑
    def close_event(self):
        logger.info("关闭登录窗口")
        # 退出应用程序
        QApplication.instance().quit()

    def login_pushButton_event(self):
        logger.info("用户登录")
        # 登录的逻辑写在这里

        # 登录成功
        gl.set_value("user_name", self.user_name_lineEdit.text())
        self.root.user_name_label.setText("user_name:" + gl.get_value("user_name"))
        self.root.show()  # 显示主窗体
        self.root.tray_icon.show()  # 显示托盘图标
        self.close()

    def forget_password_pushButton_event(self):
        logger.info("忘记密码")
        pass

    def register_pushButton_event(self):
        logger.info("用户注册")
        pass

    def github_pushButton_event(self):
        logger.info("跳转到github网站")
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/wp19991/pyqt5_example"))
        pass

    def phone_pushButton_event(self):
        logger.info("忘记密码")
        pass

    def email_pushButton_event(self):
        logger.info("忘记密码")
        pass
