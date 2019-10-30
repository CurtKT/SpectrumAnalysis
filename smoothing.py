import numpy as np
import math


# class Smooth:
class Method:
    @staticmethod
    def mean_shift(main_window, y):
        """平均移动法"""
        a1 = len(y)
        smooth_y = np.arange(1024)
        for i in range(a1):
            if (i<(main_window.pram_m-1)/2 or i>1023-(main_window.pram_m-1)/2):
                smooth_y[i] = y[i]
            else:
                temp = 0
                for j in range(main_window.pram_m):
                    temp = temp + y[int(i+j-(main_window.pram_m-1)/2)]
                smooth_y[i] = temp/main_window.pram_m
        return smooth_y

    @staticmethod
    def focus(main_window, y):
        """重心法"""
        smooth_y = np.arange(1024)
        if main_window.pram_m == 3:
            for i in range(len(y)):
                if (i < (main_window.pram_m - 1) / 2 or i > 1023 - (main_window.pram_m - 1) / 2):
                    smooth_y[i] = y[i]
                else:
                    smooth_y[i] = int(0.25*(y[i-1]+2*y[i]+y[i+1]))
        if main_window.pram_m == 5:
            for i in range(len(y)):
                if (i < (main_window.pram_m - 1) / 2 or i > 1023 - (main_window.pram_m - 1) / 2):
                    smooth_y[i] = y[i]
                else:
                    smooth_y[i] = int(1/16*(y[i-2]+4*y[i-1]+6*y[i]+4*y[i+1]+y[i+2]))
        if main_window.pram_m == 7:
            for i in range(len(y)):
                if (i < (main_window.pram_m - 1) / 2 or i > 1023 - (main_window.pram_m - 1) / 2):
                    smooth_y[i] = y[i]
                else:
                    smooth_y[i] = int(1/64*(y[i-3]+6*y[i-2]+15*y[i-1]+20*y[i]+15*y[i+1]+6*y[i+2]+y[i+3]))
        return smooth_y

    @staticmethod
    def least_sqa(main_window, y):
        """最小二乘法"""
        smooth_y = np.arange(1024)
        if main_window.pram_n == 2 or main_window.pram_n == 3:  # 二次函数
            if main_window.pram_m == 5:
                for i in range(len(y)):
                    if (i < (main_window.pram_m - 1) / 2 or i > 1023 - (main_window.pram_m - 1) / 2):
                        smooth_y[i] = y[i]
                    else:
                        smooth_y[i] = int(1/35*(-3*y[i-2]+12*y[i-1]+17*y[i]+12*y[i+1]+-3*y[i+2]))
            else:
                for i in range(len(y)):
                    if (i < (main_window.pram_m - 1) / 2 or i > 1023 - (main_window.pram_m - 1) / 2):
                        smooth_y[i] = y[i]
                    else:
                        smooth_y[i] = int(1/21*(-2*y[i-3]+3*y[i-2]+6*y[i-1]+7*y[i]+6*y[i+1]+3*y[i+2]-2*y[i+3]))
        return smooth_y

    @staticmethod
    def simple_cmp(main_window, y):
        """简单比较法"""
        search = 3  # 峰位区间内只出现一个特征点
        search_list = []  # 存储特征点列表
        if main_window.peak_serach_type == "简单比较":
            left, right = main_window.graph_widget.region.getRegion()
            if left<main_window.pram_m2:  # 防止左右边界寻峰时列表索引溢出
                left = main_window.pram_m2
            if right>1023-main_window.pram_m2:
                right = 1023-main_window.pram_m2
            # x_range = int(right+1)-int(left)
            for i in range(int(left), int(right+1)):
                cmp_value = y[i] - main_window.pram_k * math.sqrt(y[i])
                if y[i-main_window.pram_m2] < cmp_value and y[i+main_window.pram_m2] < cmp_value:
                    if search >= 3:
                        search_list.append(i)
                        search = 0
                else:
                    search += 1
        cnt = 0
        # 寻找峰位道值
        for i in search_list:
            for j in range(main_window.pram_m2):
                temp = int(i+j-(main_window.pram_m2-1)/2)  # 以i点为中心，一共寻找m2个点
                if y[search_list[cnt]] < y[temp]:  # 寻找峰位
                    search_list[cnt] = temp
            cnt += 1

        # 寻找左右边界
        left_list = []
        right_list = []
        for i in search_list:
            l_reg = 0
            r_reg = 0
            # 左边界
            while True:
                if i-l_reg-main_window.pram_m2 <= 0:  # 防止左右边界溢出
                    temp = y[0]
                else:
                    temp = y[i-l_reg-main_window.pram_m2]
                if temp >= y[i-l_reg]+main_window.pram_k*math.sqrt(y[i-l_reg]):  # 左边界判断条件
                    left_list.append(i-l_reg)
                    break
                else:
                    l_reg += 1
            # 右边界
            while True:
                if i+r_reg+main_window.pram_m2 >= 1023:  # 防止左右边界溢出
                    temp = y[1023]
                else:
                    temp = y[i+r_reg+main_window.pram_m2]
                if temp >= y[i+r_reg]+main_window.pram_k*math.sqrt(y[i+r_reg]):  # 左边界判断条件
                    right_list.append(i+r_reg)
                    break
                else:
                    r_reg += 1

        # 线条标记
        if len(search_list) != 0:
            range_y = main_window.graph_widget.pw.visibleRange().height()  # 获取y轴量程
            for i in range(len(search_list)):
                main_window.graph_widget.pw.plot([search_list[i], search_list[i]], [y[search_list[i]]-0.15*range_y, y[search_list[i]]+0.15*range_y], pen="r")
                main_window.graph_widget2.pw.plot([search_list[i], search_list[i]], [y[search_list[i]]-0.15*range_y, y[search_list[i]]+0.15*range_y], pen="r")
                main_window.graph_widget.pw.plot([left_list[i], left_list[i]], [y[left_list[i]]-0.15*range_y, y[left_list[i]]+0.15*range_y], pen="b")
                main_window.graph_widget2.pw.plot([left_list[i], left_list[i]], [y[left_list[i]] - 0.15 * range_y, y[left_list[i]] + 0.15 * range_y], pen="b")
                main_window.graph_widget.pw.plot([right_list[i], right_list[i]], [y[right_list[i]]-0.15*range_y, y[right_list[i]]+0.15*range_y], pen="b")
                main_window.graph_widget2.pw.plot([right_list[i], right_list[i]], [y[right_list[i]] - 0.15 * range_y, y[right_list[i]] + 0.15 * range_y], pen="b")

    @staticmethod
    def gauss_product(main_window, y):
        """高斯乘积法"""
        pass





