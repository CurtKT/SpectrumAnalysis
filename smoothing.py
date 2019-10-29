import numpy as np


class Smooth:
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
        """重心法"""
        smooth_y = np.arange(1024)
        if main_window.pram_n == 2:  # 二次函数
            pass

