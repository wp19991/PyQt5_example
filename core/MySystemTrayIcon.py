from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QSystemTrayIcon, QAction, QApplication, QMenu, QGraphicsDropShadowEffect, QStyle
from loguru import logger


class MySystemTrayIcon(QSystemTrayIcon):
    """
    自定义的系统托盘图标类
    """

    def init(self, parent=None):
        self.root = parent
        self.setupUi()

    def setupUi(self):
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap(":/icon/app.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(self.icon)
        '''
            Define and add steps to work with the system tray icon
            show - show window
            hide - hide window
            exit - exit from application
        '''
        self.show_action = QAction("显示", self)
        self.hide_action = QAction("隐藏", self)
        self.quit_action = QAction("退出", self)
        self.show_action.triggered.connect(self.show_event)
        self.hide_action.triggered.connect(self.hide_event)
        self.quit_action.triggered.connect(QApplication.instance().quit)
        self.tray_menu = QMenu()
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.hide_action)
        self.tray_menu.addAction(self.quit_action)
        self.setContextMenu(self.tray_menu)

        self.tray_menu.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 背景透明
        self.tray_menu.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 去掉黑边
        self.tray_menu.setWindowFlag(QtCore.Qt.NoDropShadowWindowHint)  # 去掉阴影
        self.tray_menu.setAutoFillBackground(True)
        # 增加阴影
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setOffset(0, 0)
        self.shadow.setColor(QtCore.Qt.gray)
        self.shadow.setBlurRadius(9)
        self.tray_menu.setGraphicsEffect(self.shadow)

        self.QMenuStyleSheet = '''
        QMenu {
            color:black;
            background-color:white; 
            border-radius:12px;
            padding:5px;
            margin:6px;
        }
        QMenu::item {
            font-size: 8pt; 
            border: 2px solid #909090; /*item选框*/
            border-radius:12px;
            padding:5px 10px; /*设置菜单项文字上下和左右的内边距，效果就是菜单中的条目左右上下有了间隔*/
            margin:2px 2px; /*设置菜单项的外边距*/
        }
        QMenu::item:selected{ 
            color:#1aa3ff;
            background-color: #e5f5ff;
            border-radius:12px;
        }
        QMenu::separator{
            height:1px;
            background:#bbbbbb;
            margin:5px;
            margin-left:10px;
            margin-right:10px;
        }
        '''
        self.tray_menu.setStyleSheet(self.QMenuStyleSheet)

    def show_event(self):
        logger.info("显示主窗口")
        self.root.show()
        self.setupUi()

    def hide_event(self):
        logger.info("隐藏主窗口")
        self.root.hide()
        self.setupUi()
