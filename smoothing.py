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
        main_window.textBrowser.append("普光滑:平均移动法")
        main_window.textBrowser.append("m=%d" % main_window.pram_m)
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
        main_window.textBrowser.append("普光滑:重心法")
        main_window.textBrowser.append("m=%d" % main_window.pram_m)
        return smooth_y

    @staticmethod
    def least_sqa(main_window, y):  # 注经最小二乘法平滑之后的数据点可能为负数
        """最小二乘法"""
        smooth_y = np.arange(1024)
        if main_window.pram_n == 2 or main_window.pram_n == 3:  # 二次函数
            if main_window.pram_m == 5:
                for i in range(len(y)):
                    if (i < (main_window.pram_m - 1) / 2 or i > 1023 - (main_window.pram_m - 1) / 2):
                        smooth_y[i] = y[i]
                    else:
                        smooth_y[i] = int(1/35*(-3*y[i-2]+12*y[i-1]+17*y[i]+12*y[i+1]+-3*y[i+2]))
                        if smooth_y[i] < 0:
                            smooth_y[i] = 0
            else:
                for i in range(len(y)):
                    if (i < (main_window.pram_m - 1) / 2 or i > 1023 - (main_window.pram_m - 1) / 2):
                        smooth_y[i] = y[i]
                    else:
                        smooth_y[i] = int(1/21*(-2*y[i-3]+3*y[i-2]+6*y[i-1]+7*y[i]+6*y[i+1]+3*y[i+2]-2*y[i+3]))
                        if smooth_y[i] < 0:
                            smooth_y[i] = 0
        main_window.textBrowser.append("普光滑:重心法")
        main_window.textBrowser.append("点数=%d,多项式次数=%d" % (main_window.pram_m, main_window.pram_n))
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
        # 判断是否选择最强峰
        stro_peak = [0]
        if main_window.search_region == "最强峰":
            for i in search_list:
                if y[i]>y[stro_peak[0]]:
                    stro_peak[0] = i
            search_list = stro_peak
        for i in search_list:
            l_reg = 0
            r_reg = 0
            # 左边界
            while True:
                if i-l_reg-main_window.pram_m2 <= 0:  # 防止左右边界溢出
                    left_list.append(0)
                    break
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
                    left_list.append(1023)
                    break
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
            main_window.line_obj_list = []  # 线条对象列表
            for i in range(len(search_list)):
                main_window.line1 = main_window.graph_widget.pw.plot([search_list[i], search_list[i]], [y[search_list[i]]-0.15*range_y, y[search_list[i]]+0.15*range_y], pen="r")
                main_window.line2 = main_window.graph_widget2.pw.plot([search_list[i], search_list[i]], [y[search_list[i]]-0.15*range_y, y[search_list[i]]+0.15*range_y], pen="r")
                main_window.line3 = main_window.graph_widget.pw.plot([left_list[i], left_list[i]], [y[left_list[i]]-0.15*range_y, y[left_list[i]]+0.15*range_y], pen="b")
                main_window.line4 = main_window.graph_widget2.pw.plot([left_list[i], left_list[i]], [y[left_list[i]] - 0.15 * range_y, y[left_list[i]] + 0.15 * range_y], pen="b")
                main_window.line5 = main_window.graph_widget.pw.plot([right_list[i], right_list[i]], [y[right_list[i]]-0.15*range_y, y[right_list[i]]+0.15*range_y], pen="b")
                main_window.line6 = main_window.graph_widget2.pw.plot([right_list[i], right_list[i]], [y[right_list[i]] - 0.15 * range_y, y[right_list[i]] + 0.15 * range_y], pen="b")
                main_window.line_obj_list.append(main_window.line1)
                main_window.line_obj_list.append(main_window.line2)
                main_window.line_obj_list.append(main_window.line3)
                main_window.line_obj_list.append(main_window.line4)
                main_window.line_obj_list.append(main_window.line5)
                main_window.line_obj_list.append(main_window.line6)
        main_window.textBrowser.append("普光滑:重心法")
        main_window.textBrowser.append("点数=%d,k=%d" % (main_window.pram_m, main_window.pram_k))
        return search_list, left_list, right_list  # 峰位，左边界，右边界

    @staticmethod
    def first_der(main_window, y):
        """一阶导数"""
        print("*"*50)
        der_list = []  # 一阶导数存值列表
        left, right = main_window.graph_widget.region.getRegion()
        if left < main_window.pram_m2:  # 防止左右边界寻峰时列表索引溢出
            left = main_window.pram_m2
        if right > 1023 - main_window.pram_m2:
            right = 1023 - main_window.pram_m2
        # x_range = int(right+1)-int(left)
        # 一阶导数求峰位
        if main_window.pram_m2 == 5:
            for i in range(int(left), int(right + 1)):
                if (i < (main_window.pram_m2 - 1) / 2 or i > 1023 - (main_window.pram_m2 - 1) / 2):
                    der_list.append(0)  # 边界导数为0
                else:
                    temp = y[i-2]+-8*y[i-1]+8*y[i+1]+-1*y[i+2]
                    der_list.append(temp)
        elif main_window.pram_m2 == 7:
            for i in range(int(left), int(right + 1)):
                if (i < (main_window.pram_m2 - 1) / 2 or i > 1023 - (main_window.pram_m2 - 1) / 2):
                    der_list.append(0)  # 边界导数为0
                else:
                    temp = 22*y[i-3]+-67*y[i-2]+-58*y[i-1]+58*y[i+1]+67*y[i+2]+-22*y[i+3]
                    der_list.append(temp)
        else:
            for i in range(int(left), int(right + 1)):
                if (i < (main_window.pram_m2 - 1) / 2 or i > 1023 - (main_window.pram_m2 - 1) / 2):
                    der_list.append(0)  # 边界导数为0
                else:
                    temp = 86*y[i-4]+-142*y[i-3]+-193*y[i-2]+-126*y[i-1]+126*y[i+1]+193*y[i+2]+142*y[i+3]+-86*y[i+4]
                    der_list.append(temp)
        peak_list = []  # 峰位列表
        range_left_list = []  # 左右边界列表
        range_right_list = []
        for i in range(len(der_list)-1):
            # 寻峰
            if der_list[i]>0 and der_list[i+1]<=0:
                if y[int(left)+i]>y[int(left)+i+1]:
                    peak_list.append(int(left)+i)
                else:
                    peak_list.append(int(left)+i+1)
        # 判断是否选择最强峰
        stro_peak = [0]
        if main_window.search_region == "最强峰":
            for i in peak_list:
                if y[i]>y[stro_peak[0]]:
                    stro_peak[0] = i
            peak_list = stro_peak
        # 寻找左右边界
        for i in peak_list:
            num_l = 1  # 左边界离峰道距离
            num_r = 1  # 右边界离峰道距离
            while True:  # 寻找左边界
                try:
                    if der_list[i-num_l]<=0 and der_list[i-num_l+1]>0:
                        range_left_list.append(i-num_l)
                        break
                except:
                    range_left_list.append(int(left))
                    break
                num_l += 1
            while True:  # 寻找右边界
                try:
                    if der_list[i+num_r]<=0 and der_list[i+num_r+1]>0:
                        range_right_list.append(i+num_r)
                        break
                except:
                    range_right_list.append(int(right))
                    break
                num_r += 1
        # 线条标记
        if len(peak_list) != 0:
            range_y = main_window.graph_widget.pw.visibleRange().height()  # 获取y轴量程
            main_window.line_obj_list = []  # 线条对象列表
            for i in range(len(peak_list)):
                main_window.line1 = main_window.graph_widget.pw.plot([peak_list[i], peak_list[i]], [y[peak_list[i]]-0.15*range_y, y[peak_list[i]]+0.15*range_y], pen="r")
                main_window.line2 = main_window.graph_widget2.pw.plot([peak_list[i], peak_list[i]], [y[peak_list[i]]-0.15*range_y, y[peak_list[i]]+0.15*range_y], pen="r")
                main_window.line3 = main_window.graph_widget.pw.plot([range_left_list[i], range_left_list[i]], [y[range_left_list[i]]-0.15*range_y, y[range_left_list[i]]+0.15*range_y], pen="b")
                main_window.line4 = main_window.graph_widget2.pw.plot([range_left_list[i], range_left_list[i]],[y[range_left_list[i]] - 0.15 * range_y,y[range_left_list[i]] + 0.15 * range_y], pen="b")
                main_window.line5 = main_window.graph_widget.pw.plot([range_right_list[i], range_right_list[i]], [y[range_right_list[i]]-0.15*range_y, y[range_right_list[i]]+0.15*range_y], pen="b")
                main_window.line6 = main_window.graph_widget2.pw.plot([range_right_list[i], range_right_list[i]], [y[range_right_list[i]]-0.15*range_y, y[range_right_list[i]]+0.15*range_y], pen="b")
                main_window.line_obj_list.append(main_window.line1)
                main_window.line_obj_list.append(main_window.line2)
                main_window.line_obj_list.append(main_window.line3)
                main_window.line_obj_list.append(main_window.line4)
                main_window.line_obj_list.append(main_window.line5)
                main_window.line_obj_list.append(main_window.line6)
        return peak_list, range_left_list, range_right_list

    @staticmethod
    def linear_cal(main_window, y, peak_list, range_left_list, range_right_list):
        """线性本底法"""
        gross_area = []  # 总面积
        background_area = []  # 本地面积
        net_area = []  # 净面积
        main_window.textBrowser.append("峰面积计算:线性本底法")
        main_window.textBrowser.append("峰号\t总面积\t净面积\t")
        for i in range(len(peak_list)):  # i为第几个峰
            gross_area.append(sum(y[range_left_list[i]:range_right_list[i]+1]))
            background_area.append(int((y[range_right_list[i]]+y[range_left_list[i]])*(range_right_list[i]-range_left_list[i])/2))
            net_area.append(gross_area[i]-background_area[i])
            main_window.textBrowser.append("%d\t%d\t%d\t" % (i, gross_area[i], net_area[i]))
        main_window.textBrowser.append("\r\n\r\n")









