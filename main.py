import sys
from untitled import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication, QAbstractItemView, QFileDialog
from graph import Graph, Graph2
from PyQt5 import QtCore, QtWidgets
import numpy as np


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
        print("1f")
        print("2f")
        pass

    def init_special_ui(self):
        """特殊控件初始化"""
        vbox = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.graph_widget = Graph(self.groupBox_2)  # 图像控件1
        vbox.addWidget(self.graph_widget)
        vbox = QtWidgets.QVBoxLayout(self.groupBox)
        self.graph_widget2 = Graph2(self.groupBox)  # 图像控件2
        vbox.addWidget(self.graph_widget2)
        pass

    def init_signal(self):
        """建立信号与槽链接"""
        self.action.triggered.connect(self.file_read)
        pass

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
        self.graph_widget.init_items(self.x, self.y+10)
        self.graph_widget2.init_items(self.x, self.y+10)
        self.graph_widget.run()
        self.graph_widget2.run()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_show = MainWindow()
    my_show.setWindowTitle("EnergyScope")
    # 主窗口退出机制
    my_show.show()
    sys.exit(app.exec_())
