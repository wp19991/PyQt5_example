import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QFrame, QMessageBox, QTableWidgetItem, QApplication, QHeaderView
from loguru import logger
from playhouse.shortcuts import model_to_dict

from models.user import User
from ui.mysql_form import Ui_Frame as ui_form
from utils.connect_mysql import db


class mysql_form(ui_form, QFrame):
    def __init__(self):
        super(mysql_form, self).__init__()
        self.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon/探测声音.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)

        # 加载字体
        QtGui.QFontDatabase.addApplicationFont("res/Social Media Circled.otf")
        # 隐藏原始的框
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 按钮事件绑定
        self.close_pushButton.clicked.connect(self.close_event)
        self.min_pushButton.clicked.connect(self.showMinimized)

        self.is_admin_login = False

        self.admin_login_pushButton.clicked.connect(self.admin_login_pushButton_event)
        self.fresh_pushButton.clicked.connect(self.fresh_pushButton_event)
        self.delete_user_pushButton.clicked.connect(self.delete_user_pushButton_event)
        self.add_user_pushButton.clicked.connect(self.add_user_pushButton_event)
        self.change_user_pushButton.clicked.connect(self.change_user_pushButton_event)

        # 后期需要删除
        self.admin_login_of_user_name_lineEdit.setText("admin")
        self.admin_login_of_password_lineEdit.setText("123456")

    # 关闭的逻辑
    def close_event(self):
        logger.info("关闭窗口")
        self.close()

    def admin_login_pushButton_event(self):
        logger.info("管理员登录")
        user_name = self.admin_login_of_user_name_lineEdit.text()
        password = self.admin_login_of_password_lineEdit.text()
        if user_name == "" or password == "":
            QMessageBox.information(self, "管理员登录", "请输入用户名密码")
            return
        info = User.select_from_user_name_and_password(user_name, password)

        if info is None:
            QMessageBox.information(self, "管理员登录", "登录错误，请重试")
            return

        if info.type != 2:
            QMessageBox.information(self, "管理员登录", "不是管理员，请重新登录")
            return

        # 登录成功
        QMessageBox.information(self, "登录成功", "欢迎用户管理员")
        self.is_admin_login = True
        self.groupBox_4.hide()
        self.fresh_pushButton_event()  # 刷新数据表

    def fresh_pushButton_event(self):
        logger.info("更新user表内容")
        if not self.is_admin_login:
            QMessageBox.information(self, "权限错误", "管理员未登录")
            return
        self.datas = User.get_user_datas()

        # print("len(self.datas):", len(self.datas))
        self.rowNum = len(self.datas)  # 获取查询到的行数
        self.columnNum = 0  # 获取查询到的列数
        for _ in model_to_dict(self.datas[0]).keys():
            self.columnNum += 1
        # print("self.rowNum", self.rowNum)
        # print("self.columnNum", self.columnNum)

        self.data_name_list = []
        self.data_name_list_zw = ["id", "创建时间", "修改时间", "用户名", "是否注销", "手机号", "邮箱", "密码", "类型", "简要说明"]
        for i in model_to_dict(self.datas[0]).keys():
            self.data_name_list.append(i)
        # print("self.data_name_list", self.data_name_list)

        self.data_list = []
        for i in self.datas:
            temp = []
            for j in model_to_dict(i).values():
                temp.append(j)
            self.data_list.append(temp)
        # print("self.data_list", self.data_list)

        self.tableWidget.setRowCount(self.rowNum)  # 设置表格行数
        self.tableWidget.setColumnCount(self.columnNum)  # 设置表格列数
        self.tableWidget.setHorizontalHeaderLabels(self.data_name_list_zw)  # 设置表头

        for i, da in enumerate(self.data_list):
            for j in range(self.columnNum):
                if j == 8:
                    da_temp = "普通用户" if da[j] == 1 else "管理员"
                    self.itemContent = QTableWidgetItem('%s' % da_temp)
                    self.tableWidget.setItem(i, j, self.itemContent)
                    continue
                da_temp = "无" if da[j] is None else da[j]
                self.itemContent = QTableWidgetItem('%s' % da_temp)
                self.tableWidget.setItem(i, j, self.itemContent)

        for i in range(self.columnNum):
            # 设置列宽
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def delete_user_pushButton_event(self):
        logger.info("删除用户")
        if not self.is_admin_login:
            QMessageBox.information(self, "权限错误", "管理员未登录")
            return
        user_id = self.delete_user_of_id_lineEdit.text()
        # 字段检查
        if user_id == "":
            QMessageBox.information(self, "删除用户", "请输入用户id")
            return
        if user_id == "1":
            QMessageBox.information(self, "删除用户", "你删除的是管理员，操作错误")
            return
        # 进行删除用户
        if User.user_delete(int(user_id)):
            QMessageBox.information(self, "删除用户", "删除用户成功")
            self.delete_user_of_id_lineEdit.setText("")
            self.fresh_pushButton_event()
        else:
            QMessageBox.information(self, "删除用户", "删除用户失败，请检查输入")

    def add_user_pushButton_event(self):
        logger.info("添加用户")
        if not self.is_admin_login:
            QMessageBox.information(self, "权限错误", "管理员未登录")
            return
        user_name = self.add_user_of_user_name_lineEdit.text()
        password = self.add_user_of_password_lineEdit.text()
        # 字段检查
        if user_name == "" or password == "":
            QMessageBox.information(self, "添加用户", "请输入输入用户名和密码")
            return
        # 进行添加用户
        try:
            User.user_create(user_name, password)
            QMessageBox.information(self, "添加用户", "添加用户成功")
            self.add_user_of_user_name_lineEdit.setText("")
            self.add_user_of_password_lineEdit.setText("")
            self.fresh_pushButton_event()
        except:
            QMessageBox.information(self, "添加用户", "用户名重复，请重新输入")

    def change_user_pushButton_event(self):
        logger.info("修改用户")
        if not self.is_admin_login:
            QMessageBox.information(self, "权限错误", "管理员未登录")
            return
        user_id = self.change_user_of_id_lineEdit.text()
        user_name = self.change_user_of_user_name_lineEdit.text()
        phone = self.change_user_of_phone_lineEdit.text()
        email = self.change_user_of_email_lineEdit.text()
        password = self.change_user_of_password_lineEdit.text()
        # 字段检查
        if user_id == "":
            QMessageBox.information(self, "修改用户", "请输入输入需要修改的用户id")
            return
        # 进行修改用户
        res = User.user_update(int(user_id), user_name, phone, email, password)
        if res:
            QMessageBox.information(self, "修改用户", "修改用户成功")
            self.change_user_of_user_name_lineEdit.setText("")
            self.change_user_of_phone_lineEdit.setText("")
            self.change_user_of_email_lineEdit.setText("")
            self.change_user_of_password_lineEdit.setText("")
            self.fresh_pushButton_event()
        else:
            QMessageBox.information(self, "修改用户", "修改失败,请检查输入")

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


if __name__ == "__main__":
    db.connect()
    app = QApplication(sys.argv)
    A1 = mysql_form()
    A1.show()
    sys.exit(app.exec_())
