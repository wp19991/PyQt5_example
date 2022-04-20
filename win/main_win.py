from PyQt5 import QtWidgets, QtCore
from PyQt5.QtChart import QChart, QLineSeries, QChartView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QMainWindow, QSystemTrayIcon, QFileSystemModel, QTreeView
from loguru import logger

from config.core import Config
from core.CpuLineChart import CpuLineChart
from core.DynamicSpline import DynamicSpline
from core.FileIconProvider import FileIconProvider
from core.ImageView import ImageView
from core.MetroCircleProgress import MetroCircleProgress
from core.MySystemTrayIcon import MySystemTrayIcon
from ui.main_window import Ui_MainWindow as main_window
from utils.CommonHelper import CommonHelper
from win.close_dialog import close_dialog
from utils import global_var as gl


class main_win(QMainWindow, main_window):
    def __init__(self):
        super(main_win, self).__init__()
        self.setupUi(self)

        # 登录界面
        # self.login = login_form(self)
        # self.login.show()

        self.config = Config.current()  # 读取配置文件
        self.setStyleSheet(CommonHelper.read_qss_file(self.config.getSec("general")["skin"]))

        self.config.getSec("advance")["autoexportqss"] = "1seees"
        self.config.saveDefault()  # 保持配置文件

        # 程序托盘图标
        self.show_tray_icon = close_dialog(parent=self)
        self.tray_icon = MySystemTrayIcon()
        self.tray_icon.init(self)  # 将自己传进去
        self.tray_icon.show()

        # 添加用户名的label
        self.user_name_label = QtWidgets.QLabel()
        self.user_name_label.setObjectName("user_name_label")
        self.user_name_label.setText("还没有设置登录界面，请在app.py中打开注释")
        self.verticalLayout.addWidget(self.user_name_label)

        # verticalLayout 添加 cpu动态折线图
        self.add_cpu_chart()

        # 添加无状态的动态进度条
        self.verticalLayout.addWidget(MetroCircleProgress(self, styleSheet="""qproperty-color: #ff0000;"""))

        # verticalLayout 添加 折线图
        # self.add_chart()

        # verticalLayout 添加 动态曲线图
        # self.add_dynamic_chart()

        # 添加图片查看器控件
        # self.image_view = ImageView(image='res/American_Robin.jpg', background=Qt.black)
        # self.image_view.setPixmap("res/fish.png")
        # self.verticalLayout.addWidget(self.image_view)

        # 添加文件路径控件
        # self.add_file_system()

    def add_file_system(self):
        self.model = QFileSystemModel()
        self.model.setIconProvider(FileIconProvider())  # 设置为自定义的图标提供类
        self.model.setRootPath("")
        self.tree = QTreeView()
        self.tree.setModel(self.model)

        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)

        self.tree.setWindowTitle("Dir View")
        self.tree.resize(640, 480)
        self.verticalLayout.addWidget(self.tree)
        self.tree.show()

    def add_cpu_chart(self):
        self.cpu_chart = CpuLineChart()
        self.cpu_chart.setTitle('cpu')
        self.cpu_chart.setAnimationOptions(QChart.SeriesAnimations)

        self.zxt_QChartView = QChartView()
        self.zxt_QChartView.setObjectName("zxt_QChartView")
        self.verticalLayout.addWidget(self.zxt_QChartView)
        self.zxt_QChartView.setChart(self.cpu_chart)
        self.zxt_QChartView.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.zxt_QChartView.resize(800, 600)
        self.zxt_QChartView.show()

    def add_dynamic_chart(self):
        self.dynamic_chart = DynamicSpline()
        self.dynamic_chart.setTitle("Dynamic spline chart")
        self.dynamic_chart.legend().hide()
        self.dynamic_chart.setAnimationOptions(QChart.AllAnimations)

        self.zxt_QChartView = QChartView()
        self.zxt_QChartView.setObjectName("zxt_QChartView")
        self.verticalLayout.addWidget(self.zxt_QChartView)
        self.zxt_QChartView.setChart(self.dynamic_chart)
        self.zxt_QChartView.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.zxt_QChartView.resize(800, 600)
        self.zxt_QChartView.show()

    def add_chart(self):
        self.chart = QChart()
        self.chart.setTitle('Line Chart 1')
        self.series = QLineSeries(self.chart)
        self.series.append(0, 6)
        self.series.append(2, 4)
        self.series.append(3, 14)
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()  # 创建默认轴

        self.zxt_QChartView = QChartView()
        self.zxt_QChartView.setObjectName("zxt_QChartView")
        self.verticalLayout.addWidget(self.zxt_QChartView)
        self.zxt_QChartView.setChart(self.chart)
        self.zxt_QChartView.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.zxt_QChartView.resize(800, 600)
        self.zxt_QChartView.show()

    # 重写关闭的逻辑
    def closeEvent(self, event):
        logger.info("是否关闭主窗口")
        event.ignore()
        self.show_tray_icon.show()
