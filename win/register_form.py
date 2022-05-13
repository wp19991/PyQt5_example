from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QFrame, QMessageBox
from loguru import logger

from models.user import User
from ui.register_form import Ui_Frame as ui_form


class register_form(ui_form, QFrame):
    def __init__(self):
        super(register_form, self).__init__()
        self.setupUi(self)

        # 加载字体
        QtGui.QFontDatabase.addApplicationFont("res/otf/Social Media Circled.otf")

        # 隐藏原始的框
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 按钮事件绑定
        self.close_pushButton.clicked.connect(self.close_event)
        self.min_pushButton.clicked.connect(self.showMinimized)

        self.register_pushButton.clicked.connect(self.register_pushButton_event)

        # 底部按钮
        self.github_pushButton.clicked.connect(self.github_pushButton_event)
        self.phone_pushButton.clicked.connect(self.phone_pushButton_event)
        self.email_pushButton.clicked.connect(self.email_pushButton_event)

    # 关闭的逻辑
    def close_event(self):
        logger.info("关闭登录窗口")
        # 退出应用程序
        self.close()

    def register_pushButton_event(self):
        logger.info("用户注册")
        user_name = self.user_name_lineEdit.text()
        password = self.password_lineEdit.text()
        password2 = self.password2_lineEdit.text()
        if password != password2:
            QMessageBox.information(self, "错误提示", "两次密码输入不对，请重新输入")
            return
        try:
            User.user_create(user_name, password)
            QMessageBox.information(self, "注册成功", "注册成功，请登录")
            self.close()
        except:
            QMessageBox.information(self, "错误提示", "用户名重复，请重新注册")

    def github_pushButton_event(self):
        logger.info("跳转到github网站")
        QMessageBox.information(self, "GitHub", "wp19991")
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/wp19991"))

    def phone_pushButton_event(self):
        logger.info("手机号")
        QMessageBox.information(self, "手机号", "手机号\n13170190193")

    def email_pushButton_event(self):
        logger.info("邮箱")
        QMessageBox.information(self, "邮箱", "邮箱\nwpycahrm@outlook.com")

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = True
            self._startPos = QPoint(e.x(), e.y())

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        self._endPos = e.pos() - self._startPos
        self.move(self.pos() + self._endPos)

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._isTracking = False
            self._startPos = None
            self._endPos = None
