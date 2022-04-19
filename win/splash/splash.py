# -*- coding: utf-8 -*-
import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen
from res import app_rc
from win.splash.core import preimport


class SplashScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap(":/img/fish.png")
        super(SplashScreen, self).__init__(pixmap)

        self.labelAlignment = int(Qt.AlignBottom | Qt.AlignHCenter | Qt.AlignAbsolute)
        self.show()
        QApplication.flush()

    def showMessage(self, msg):
        """Show the progress message on the splash image"""
        super(SplashScreen, self).showMessage(msg, self.labelAlignment, Qt.white)
        QApplication.processEvents()

    def clearMessage(self):
        """Clear message on the splash image"""
        super(SplashScreen, self).clearMessage()
        QApplication.processEvents()

    def setProgressText(self, percent, delay=0.1):
        time.sleep(delay)  # 延时，给查看splashscreen更新数值
        self.showMessage("正在加载 ... {0}%".format(percent))

    def loadProgress(self):
        self.setProgressText(0, 0)
        time.sleep(0.1)
        self.setProgressText(5)
        time.sleep(0.1)
        self.setProgressText(10)
        time.sleep(0.1)
        self.setProgressText(15)
        time.sleep(0.1)
        self.setProgressText(20)
        preimport(["torch"])
        self.setProgressText(40)
        time.sleep(0.1)
        self.setProgressText(60)
        time.sleep(0.1)
        self.setProgressText(80)
        time.sleep(0.1)
        self.setProgressText(100)
        self.hide()
