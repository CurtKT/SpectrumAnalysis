import sys
from untitled import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication, QAbstractItemView, QFileDialog
from graph import Graph, Graph2
from PyQt5 import QtCore, QtWidgets
import numpy as np
import smoothing
import untitled_sub
import untitled_sub2
import untitled_sub3


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        """UI初始化"""
        super().__init__()
        self.setupUi(self)
        self.init_flag()
        self.init_special_ui()
        self.init_signal()

    def init_flag(self):
        """标识位初始化"""
        self.yrange = 250000  # y轴量程
        self.smooth_type = "滑动平均"  # 平滑方法
        self.peak_serach_type = "简单比较"  # 寻峰方法
        self.search_region = "全部峰"  # 寻峰范围
        self.cal_area_type = "线性本地法"  # 面积计算方法
        self.pram_m = 3  # 参数m
        self.pram_m2 = 5
        self.pram_n = 2  # 参数n
        self.pram_k = 3
        self.is_smooth = False  # 默认不开起谱光滑
        self.is_serach_peak = False  # 默认不开起寻峰

    def init_special_ui(self):
        """特殊控件初始化"""
        vbox = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.graph_widget = Graph(self.groupBox_2)  # 图像控件1
        vbox.addWidget(self.graph_widget)
        vbox = QtWidgets.QVBoxLayout(self.groupBox)
        self.graph_widget2 = Graph2(self.groupBox)  # 图像控件2
        vbox.addWidget(self.graph_widget2)
        self.make_mython = smoothing.Method  # 平滑处理方法对象
        self.sub_window2()

    def init_signal(self):
        """建立信号与槽链接"""
        self.action.triggered.connect(self.file_read)
        self.action_3.triggered.connect(self.sub_window)
        self.action_4.triggered.connect(self.sub_window2_show)
        self.pushButton_2.clicked.connect(self.set_is_smooth)
        self.pushButton_4.clicked.connect(self.set_search_peak)

    def set_is_smooth(self):
        """点击谱光滑"""
        self.is_smooth = True if self.is_smooth is False else False
        if self.is_smooth:
            self.set_smooth(self.y)
        else:
            self.graph_widget.plot_data2.setData([0], [0])
            self.graph_widget2.plot_data2.setData([0], [0])

    def set_smooth(self, y):
        """进行谱光滑处理"""
        self.smooth_y = y
        if self.smooth_type == "滑动平均":
            self.smooth_y = self.make_mython.mean_shift(self, y)
        elif self.smooth_type == "重心法":
            self.smooth_y = self.make_mython.focus(self, y)
        elif self.smooth_type == "最小二乘法":
            self.smooth_y = self.make_mython.least_sqa(self, y)
        try:
            print(self.graph_widget.plot_data2)  # 增加异常判断
            self.graph_widget.plot_data2.setData(self.x, self.smooth_y)
            self.graph_widget2.plot_data2.setData(self.x, self.smooth_y)
        except:
            self.graph_widget.smooth(self.x, self.smooth_y)
            self.graph_widget2.smooth(self.x, self.smooth_y)

    def set_search_peak(self):
        """点击寻峰"""
        self.is_serach_peak = True if self.is_serach_peak is False else False
        if self.is_serach_peak:
            if self.ui2.checkBox.isChecked():  # 如果勾选谱光滑用光滑后的数据寻峰
                if self.is_serach_peak:
                    self.set_smooth(self.y)
                    if self.peak_serach_type == "简单比较":
                        peak_list, range_left_list, range_right_list = self.make_mython.simple_cmp(self, self.smooth_y)
                        self.make_mython.linear_cal(self, self.smooth_y, peak_list, range_left_list, range_right_list)
                    elif self.peak_serach_type == "一阶导数法":
                        peak_list, range_left_list, range_right_list = self.smooth_y = self.make_mython.first_der(self, self.smooth_y)
                        self.make_mython.linear_cal(self, self.smooth_y, peak_list, range_left_list, range_right_list)
                else:
                    pass
                pass
            else:  # 如果未勾选谱光滑，用原始数据寻峰
                if self.is_serach_peak:
                    if self.peak_serach_type == "简单比较":
                        peak_list, range_left_list, range_right_list = self.make_mython.simple_cmp(self, self.y)
                        self.make_mython.linear_cal(self, self.y, peak_list, range_left_list, range_right_list)
                    elif self.peak_serach_type == "一阶导数法":
                        peak_list, range_left_list, range_right_list = self.make_mython.first_der(self, self.y)
                        self.make_mython.linear_cal(self, self.y, peak_list, range_left_list, range_right_list)
                else:
                    pass
        else:
           for i in self.line_obj_list:
                i.setData([0], [0])

    def sub_window(self):
        """建立子窗口1"""
        Dialog = QtWidgets.QDialog(self)
        self.ui = untitled_sub.Ui_Dialog()
        self.ui.setupUi(Dialog)
        Dialog.show()
        self.ui.comboBox.currentTextChanged.connect(self.sub_window_pram_choose)
        self.ui.comboBox.setCurrentText(self.smooth_type)
        self.ui.comboBox_2.setCurrentText(str(self.pram_m))
        self.ui.buttonBox.accepted.connect(self.sub_window_trans)

    def sub_window2(self):
        """建立子窗口2"""
        self.Dialog = QtWidgets.QDialog(self)
        self.ui2 = untitled_sub2.Ui_Dialog()
        self.ui2.setupUi(self.Dialog)
        self.ui2.comboBox.setCurrentText(self.peak_serach_type)
        self.ui2.comboBox_2.setCurrentText(str(self.pram_m2))
        self.ui2.doubleSpinBox.setValue(self.pram_k)
        self.ui2.buttonBox.accepted.connect(self.sub_window2_trans)

    def sub_window3(self):
        """建立子窗口3"""
        self.Dialog3 = QtWidgets.QDialog(self)
        self.ui3 = untitled_sub2.Ui_Dialog()
        self.ui3.setupUi(self.Dialog3)
        self.Dialog3.show()
        self.ui3.comboBox.setCurrentText(self.cal_area_type)
        self.ui3.buttonBox.accepted.connect(self.sub_window2_trans)

    def sub_window2_show(self):
        """窗口显示"""
        self.Dialog.show()

    def sub_window_trans(self):
        """子窗口传参"""
        self.smooth_type = self.ui.comboBox.currentText()
        self.pram_m = int(self.ui.comboBox_2.currentText())
        self.pram_n = int(self.ui.comboBox_3.currentText())

    def sub_window2_trans(self):
        """子窗口2传参"""
        self.peak_serach_type = self.ui2.comboBox.currentText()
        self.pram_m2 = int(self.ui2.comboBox_2.currentText())
        self.pram_k = self.ui2.doubleSpinBox.value()
        self.search_region = self.ui2.comboBox_3.currentText()

    def sub_window3_trans(self):
        """子窗口3传参"""
        self.cal_area_type = self.ui2.comboBox.currentText()

    def sub_window_pram_choose(self):
        """子窗口参数选择选项"""
        if self.ui.comboBox.currentText() == "滑动平均":
            self.ui.groupBox_3.setEnabled(False)
        if self.ui.comboBox.currentText() == "重心法":
            self.ui.groupBox_3.setEnabled(False)
        if self.ui.comboBox.currentText() == "最小二乘法":
            self.ui.groupBox_3.setEnabled(True)
            self.ui.comboBox_2.setCurrentText("5")

    def keyPressEvent(self, event):
        """设立快捷键"""
        if (event.key() == 16777235):
            self.yrange = self.yrange*1.3
            self.graph_widget.pw.setYRange(0, self.yrange, 0)
            self.graph_widget2.pw.setYRange(0, self.yrange, 0)
        elif (event.key() == 16777237):
            self.yrange = self.yrange/1.3
            self.graph_widget.pw.setYRange(0, self.yrange, 0)
            self.graph_widget2.pw.setYRange(0, self.yrange, 0)

    def file_read(self):
        """文件读取"""
        f_name = QFileDialog.getOpenFileName(self, "打开数据文件", "./data/", "*.txt")  # 读取文件对话
        if f_name[0]:
            with open(f_name[0], "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
                text_list = text.split()
                for i in range(len(text_list)):
                    text_list[i] = int(text_list[i])
                self.x = np.array(text_list[0::3])
                self.y = np.array(text_list[1::3])
                # self.y[950:] = self.y[950:]+50
            self.graph_widget.init_items(self.x, self.y)
            self.graph_widget2.init_items(self.x, self.y)
            self.graph_widget.run()
            self.graph_widget2.run()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = MainWindow()
    my_show.setWindowTitle("EnergyScope")
    # 主窗口退出机制
    my_show.show()
    sys.exit(app.exec_())
