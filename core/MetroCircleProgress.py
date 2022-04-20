from PyQt5.QtCore import QSequentialAnimationGroup, QPauseAnimation, QPropertyAnimation, \
    QParallelAnimationGroup, QObject, QSize, Qt, QRectF, pyqtSignal, pyqtProperty
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget


class CircleItem(QObject):
    X = 0  # x坐标
    Opacity = 1  # 透明度0~1
    valueChanged = pyqtSignal()

    @pyqtProperty(float)
    def x(self) -> float:
        return self.X

    @x.setter
    def x(self, x: float):
        self.X = x
        self.valueChanged.emit()

    @pyqtProperty(float)
    def opacity(self) -> float:
        return self.Opacity

    @opacity.setter
    def opacity(self, opacity: float):
        self.Opacity = opacity


def qBound(miv, cv, mxv):
    return max(min(cv, mxv), miv)


class MetroCircleProgress(QWidget):
    Radius = 5  # 半径
    Color = QColor(24, 189, 155)  # 圆圈颜色
    BackgroundColor = QColor(Qt.transparent)  # 背景颜色

    def __init__(self, *args, radius=5, color=QColor(24, 189, 155),
                 backgroundColor=QColor(Qt.transparent), **kwargs):
        super(MetroCircleProgress, self).__init__(*args, **kwargs)

        self.setMinimumSize(20,50)
        self.Radius = radius
        self.Color = color
        self.BackgroundColor = backgroundColor
        self._items = []
        self._initAnimations()

    @pyqtProperty(int)
    def radius(self) -> int:
        return self.Radius

    @radius.setter
    def radius(self, radius: int):
        if self.Radius != radius:
            self.Radius = radius
            self.update()

    @pyqtProperty(QColor)
    def color(self) -> QColor:
        return self.Color

    @color.setter
    def color(self, color: QColor):
        if self.Color != color:
            self.Color = color
            self.update()

    @pyqtProperty(QColor)
    def backgroundColor(self) -> QColor:
        return self.BackgroundColor

    @backgroundColor.setter
    def backgroundColor(self, backgroundColor: QColor):
        if self.BackgroundColor != backgroundColor:
            self.BackgroundColor = backgroundColor
            self.update()

    def paintEvent(self, event):
        super(MetroCircleProgress, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), self.BackgroundColor)
        painter.setPen(Qt.NoPen)

        for item, _ in self._items:
            painter.save()
            color = self.Color.toRgb()
            color.setAlphaF(item.opacity)
            painter.setBrush(color)
            # 5<= radius <=10
            radius = qBound(self.Radius, self.Radius / 200 *
                            self.height(), 2 * self.Radius)
            diameter = 2 * radius
            painter.drawRoundedRect(
                QRectF(
                    item.x / 100 * self.width() - diameter,
                    (self.height() - radius) / 2,
                    diameter, diameter
                ), radius, radius)
            painter.restore()

    def _initAnimations(self):
        for index in range(5):  # 5个小圆
            item = CircleItem(self)
            item.valueChanged.connect(self.update)
            # 串行动画组
            seqAnimation = QSequentialAnimationGroup(self)
            seqAnimation.setLoopCount(-1)
            self._items.append((item, seqAnimation))

            # 暂停延迟动画
            seqAnimation.addAnimation(QPauseAnimation(150 * index, self))

            # 加速,并行动画组1
            parAnimation1 = QParallelAnimationGroup(self)
            # 透明度
            parAnimation1.addAnimation(
                QPropertyAnimation(item, b'opacity', self, duration=400, startValue=0, endValue=1.0))
            # x坐标
            parAnimation1.addAnimation(QPropertyAnimation(item, b'x', self, duration=400, startValue=0, endValue=25.0))
            seqAnimation.addAnimation(parAnimation1)
            ##

            # 匀速
            seqAnimation.addAnimation(
                QPropertyAnimation(item, b'x', self, duration=2000, startValue=25.0, endValue=75.0))

            # 加速,并行动画组2
            parAnimation2 = QParallelAnimationGroup(self)
            # 透明度
            parAnimation2.addAnimation(
                QPropertyAnimation(item, b'opacity', self, duration=400, startValue=1.0, endValue=0))
            # x坐标
            parAnimation2.addAnimation(
                QPropertyAnimation(item, b'x', self, duration=400, startValue=75.0, endValue=100.0))
            seqAnimation.addAnimation(parAnimation2)
            ##

            # 暂停延迟动画
            seqAnimation.addAnimation(
                QPauseAnimation((5 - index - 1) * 150, self))

        for _, animation in self._items:
            animation.start()

    def sizeHint(self):
        return QSize(100, self.Radius * 2)
