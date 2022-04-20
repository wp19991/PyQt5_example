from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QMainWindow, QDialogButtonBox, QApplication
from loguru import logger

from ui.close_dialog import Ui_Dialog as c_dialog


class close_dialog(QDialog, c_dialog):
    def __init__(self, parent: QMainWindow = None):
        super(close_dialog, self).__init__()
        self.setupUi(self)
        self.root = parent

        # 隐藏原始的框,关闭缩小按钮事件绑定
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.close_pushButton.clicked.connect(self.close_event)
        self.min_pushButton.clicked.connect(self.showMinimized)

        # ok 按钮事件绑定
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.ok_event)

    # 关闭的逻辑
    def close_event(self):
        logger.info("关闭dialog窗口")
        # 直接关闭的话主界面就显示出来
        self.close()
        self.root.show()

    # ok 按钮的逻辑
    def ok_event(self):
        logger.info("点击ok按钮")
        # 选择按钮之后，这个 dialog 窗口就关闭了
        if not self.is_min_status_checkBox.isChecked():
            logger.info("没有选择缩小")
            # 退出应用程序
            QApplication.instance().quit()
        else:
            logger.info("选择缩小")
            self.root.hide()
