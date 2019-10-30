import sys
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout



class Graph(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setParent(parent)
        self.p = parent
        # self.resize(1000, 600)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        # pg.setConfigOption('leftButtonPan', False)
        self.pw = pg.PlotWidget(self)
        self.pw.setMouseEnabled(False, False)
        self.pw.showGrid(x=True, y=True)
        self.pw.setRange(xRange=[0, 1024], yRange=[0, 250000], padding=0)
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.pw)
        self.setLayout(self.v_layout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.pw.setSizePolicy(sizePolicy)

    def init_items(self, x, y):
        """初始化部件"""
        self.plot_data = self.pw.plot(x, y, symbolSize=5, symbolPen='w', pen="b")
        self.delay = 0
        self.qtime = QtCore.QTimer()
        self.qtime.timeout.connect(self.update_textBrowser)
        color = pg.mkColor(255, 0, 0, 150)
        pen = pg.mkPen(color)
        color2 = pg.mkColor(255, 150, 150, 150)
        pen2 = pg.mkPen(color2)
        pg.plot()

    def smooth(self, x, y):
        self.plot_data2 = self.pw.plot(x, y, symbolSize=5, symbolPen='r', symbolBrush='r', pen="r")


    def run(self):
        """鼠标事件控制游标"""
        self.set_cursor()
        self.region.sigRegionChanged.connect(self.update)
        self.p.parent().parent().graph_widget2.pw.sigRangeChanged.connect(self.updateRegion)
        self.region.setRegion([200, 800])
        # self.region2.setRegion([-250, 250])
        self.proxy = pg.SignalProxy(self.pw.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        self.vb = pg.ViewBox()
        self.pw.addItem(self.vb)
        # self.pw.addItem(self.label)
        self.qtime.start(100)
        self.vb = pg.ViewBox()
        self.pw.addItem(self.vb)
        # pg.plot().

    def run2(self):
        """鼠标事件控制游标"""
        self.pw.addItem(self.hLine2, ignoreBounds=True)

    def set_threshold(self, evt):
        """设置阈值光标"""
        self.p.parent().parent().doubleSpinBox.setValue(self.hLine.value())  # 改变阈值框值
        self.p.parent().parent().label_21.setText("%dmV" % self.hLine.value())

    def set_baseline(self, evt):
        """设置基准线光标"""
        self.p.parent().parent().label_23.setText("%dmV" % self.hLine2.value())
        self.p.parent().parent().set_basic_line(self.hLine2.value())

    def stop(self):
        """停止run方法"""
        self.pw.removeItem(self.region)
        self.pw.removeItem(self.region2)
        self.pw.removeItem(self.vb)
        # self.pw.removeItem(self.hLine)
        # self.pw.removeItem(self.hLine2)
        self.qtime.stop()

    def stop2(self):
        self.pw.removeItem(self.hLine2)

    def update(self):
        # _translate = QtCore.QCoreApplication.translate
        self.region.setZValue(10)
        self.minX, self.maxX = self.region.getRegion()
        self.p.parent().parent().graph_widget2.pw.setXRange(self.minX, self.maxX, padding=0)

    def update_textBrowser(self):
        _translate = QtCore.QCoreApplication.translate
        # self.p.parent().parent().label_19.setText("%.2f%s" % ((self.maxX-self.minX), self.p.parent().parent().doubleSpinBox_2.suffix()))
        minX, maxX = self.region2.getRegion()
        # self.p.parent().parent().label_20.setText("%.2fmV" % (maxX - minX))

    def updateRegion(self, window, viewRange):
        rgn = viewRange[0]
        self.region.setRegion(rgn)

    def set_cursor(self):
        """设置游标"""
        self.region = pg.LinearRegionItem()
        self.region.setZValue(100)
        self.region2 = pg.LinearRegionItem(brush=None, orientation=pg.LinearRegionItem.Horizontal)
        self.region2.setZValue(10)
        # self.pw.addItem(self.region2, ignoreBounds=True)
        self.pw.addItem(self.region, ignoreBounds=True)

    def mouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.pw.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            index = int(mousePoint.x()*50)
            # if index < self.p.parent().parent().sampling_numble/2 and index > -1*self.p.parent().parent().sampling_numble/2:
            #     x = mousePoint.x() * 50
            #     y = mousePoint.y()*-50

    def update_graph(self, list):
        """刷新图像"""
        self.plot_data.setData(x, y)


class Graph2(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setParent(parent)
        self.p = parent
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        self.pw = pg.PlotWidget(self)
        self.pw.setMouseEnabled(False, False)
        self.pw.showGrid(x=True, y=True)
        self.pw.setRange(xRange=[0, 1024], yRange=[0, 250000], padding=0)
        # self.resize(1000, 600)
        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.pw)
        self.setLayout(self.v_layout)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.pw.setSizePolicy(sizePolicy)

    def init_items(self, x, y):
        """初始化部件"""
        self.plot_data = self.pw.plot(x, y, symbolSize=5, symbolPen='w', pen="b")

    def smooth(self, x, y):
        self.plot_data2 = self.pw.plot(x, y, symbolPen='r', symbolSize=5, symbolBrush='r', pen="r")

    def run(self):
        """鼠标事件控制游标"""
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen="c")
        # self.hLine = pg.InfiniteLine(angle=0, movable=False, pen="b")
        self.pw.addItem(self.vLine, ignoreBounds=True)
        # self.pw.addItem(self.hLine, ignoreBounds=True)
        self.proxy = pg.SignalProxy(self.pw.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        self.vb = pg.ViewBox()
        self.pw.addItem(self.vb)

    def stop(self):
        """停止run方法"""
        self.pw.removeItem(self.vLine)
        self.pw.removeItem(self.vb)

    def mouseMoved(self, evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.pw.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            try:
                self.p.parent().parent().label.setText("道:%d计数:%d" % (int(mousePoint.x()*50), self.p.parent().parent().y[int(mousePoint.x()*50)]))
            except Exception as result:
                pass
            self.vLine.setPos(mousePoint.x()*50)

    def update_graph(self, list):
        """刷新图像"""
        try:
            x = [(i[0]+1-self.p.parent().parent().sampling_numble/2)/self.p.parent().parent().sampling_race * 1000/self.p.parent().parent().ratio for i in list[len(list)-1]]
            k1 = float(self.p.parent().parent().K1)
            k2 = float(self.p.parent().parent().K2)
            k3 = float(self.p.parent().parent().K3)
            k4 = float(self.p.parent().parent().K4)
            bac = float(self.p.parent().parent().bac)
            y = [i[1]*k1+k2*bac+k3+k4 for i in list[len(list)-1]]
            self.plot_data.setData(x, y, pen="m")
        except:
            pass
        if self.p.parent().parent().is_history:
            try:
                x1 = [(i[0]+1-self.p.parent().parent().sampling_numble/2)/self.p.parent().parent().sampling_race * 1000/self.p.parent().parent().ratio for i in list[0]]
                y1 = [i[1]*k1+k2*bac+k3+k4 for i in list[0]]
                self.plot_data1.setData(x1, y1, pen="m")
                x2 = [(i[0]+1-self.p.parent().parent().sampling_numble/2)/self.p.parent().parent().sampling_race * 1000/self.p.parent().parent().ratio for i in list[1]]
                y2 = [i[1]*k1+k2*bac+k3+k4 for i in list[1]]
                self.plot_data2.setData(x2, y2, pen="m")
                x3 = [(i[0]+1-self.p.parent().parent().sampling_numble/2)/self.p.parent().parent().sampling_race * 1000/self.p.parent().parent().ratio for i in list[2]]
                y3 = [i[1]*k1+k2*bac+k3+k4 for i in list[2]]
                self.plot_data3.setData(x3, y3, pen="m")
            except:
                pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Graph()
    demo.show()
    sys.exit(app.exec_())
