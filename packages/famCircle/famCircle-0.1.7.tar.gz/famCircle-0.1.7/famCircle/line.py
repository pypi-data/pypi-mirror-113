# python
# -*- encoding: utf-8 -*-
'''
@File        :iclmap.py
@Time        :2021/07/11 12:44:00
@Author        :charles kiko
@Version        :1.0
@Contact        :charles_kiko@163.com
@Desc        :None
'''

import csv
import sys
import re
from math import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import *
from matplotlib.patches import Circle, Ellipse, Arc
from pylab import *
from famCircle.bez import *

class line():
    def __init__(self, options):
        self.makers = 200
        # self.chrolist = "mes,ssu"
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def readname(self, name):
        if ('^' in name):
            return name
        elif ('g' in name):
            if 'g' not in self.chrolist:
                name = name.replace('g', '^')
            else :
                lt = name.split('g')
                name = ''
                for i in range(len(lt)):
                    if i < len(lt) - 2:
                        name = name + str(lt[i]) + 'g'
                    elif i == len(lt) - 2:
                        name = name + str(lt[-2])
                    else:
                        name = name + "^" + str(lt[-1])
            return name

    def read_csv(self):
        self.chrolist = [self.chr1_name,self.chr2_name]
        matrix_chr1 = pd.read_csv(self.lens1, sep='\t', header=None, index_col=0)
        # print(matrix_chr1)
        # print(matrix_chr1.loc[self.chr1_name,2])
        length1 = matrix_chr1.loc[self.chr1_name,2]
        matrix_chr2 = pd.read_csv(self.lens2, sep='\t', header=None, index_col=0)
        # print(matrix_chr2)
        # print(matrix_chr2.loc[self.chr2_name,2])
        length2 = matrix_chr2.loc[self.chr2_name,2]
        if length1 >= length2:
            x1 = 0.8
            x2 = length2*(0.8/length1)
            maker_str = True
        else :
            x1 = 0.8
            x2 = length1*(0.8/length2)
            maker_str = False
        # x1 = max(length2,length1)
        # x2 = min(length2,length1)*(0.8/x1)
        # x1 = 0.8
        maker1 ,maker2 = int(max(length2,length1)/self.makers), int(min(length2,length1)/self.makers)
        chro1 = self.chr1_name
        chro2 = self.chr2_name
        matrix_gff1 = pd.read_csv(self.gff1, sep='\t', header=None, index_col=1)
        # for index, row in matrix_gff1.iterrows():
        #     print(index)
        matrix_gff2 = pd.read_csv(self.gff2, sep='\t', header=None, index_col=1)
        # for index, row in matrix_gff2.iterrows():
        #     print(index)
        # print(matrix_gff1)
        matrix_gff1.groupby(by=0)
        matrix_gff2.groupby(by=0)
        # print(matrix_gff1)
        return x1,x2,maker1,maker2,matrix_gff1,matrix_gff2,chro1,chro2,maker_str,length1,length2

    def read_colinearscan(self,file):
        pair = []
        pair_list = []
        with open(file) as f:
            for line in f.readlines():
                line = line.strip()
                # print(line)
                if line[0] == "#":
                    if len(pair_list) != 0:
                        # print(pair_list)#输出
                        pair.append(pair_list)
                    pair_list = []
                    block_dict = {}
                    lt = line.split()
                    block_number = str(lt[2])[:-1]
                    # print(lt)
                    for i in lt:
                        if "=" in i:
                            lt0 = i.split('=')
                            block_dict[str(lt0[0])] = str(lt0[1])
                else:
                    lt = line.split()
                    name1 = self.readname(str(lt[0]))
                    name2 = self.readname(str(lt[2]))
                    lt0 = [name1,name2]
                    # print(lt0)
                    pair_list.append(lt0)
            if len(pair_list) != 0:
                # print(pair_list)#输出
                pair.append(pair_list)
            # print(pair)
            return pair

    def plot_bez_inner(self, ex1x, ex1y, ex2x, ex2y):
        x = [ex1x, ex1x+((ex2x - ex1x)/3+0.1), ex2x-((ex2x - ex1x)/3+0.1), ex2x]
        y = [ex1y, ex1y+((ex2y - ex1y)/3), ex2y-((ex2y - ex1y)/3), ex2y]
        # ratiox = 0.5
        # ratioy = 1
        # x = [ex1x, ex1x*ratiox, ex2x*ratiox, ex2x]
        # y = [ex1y, ex1y*ratioy, ex2y*ratioy, ex2y]
        # x = [ex1x, ex1x+((ex2x - ex1x)/3), ex2x-((ex2x - ex1x)/3), ex2x]
        # y = [ex1y, ex1y+((ex2y - ex1y)/3), ex2y-((ex2y - ex1y)/3), ex2y]
        step = .01
        t = arange(0, 1+step, step)
        xt = self.Bezier(x, t)# 贝塞尔曲线
        yt = self.Bezier(y, t)
        plot(xt, yt, '-', color='r', lw=.3, alpha=0.3)#alpha 透明度

    def calculate_coef(self,p0, p1, p2, p3):
        c = 3*(p1 - p0)
        b = 3*(p2 - p1) -c
        a = p3 - p0 - c - b
        return c, b, a
    def Bezier(self,plist, t):
        # p0 : origin, p1, p2 :control, p3: destination
        p0, p1, p2, p3 = plist
        # calculates the coefficient values
        c, b, a = self.calculate_coef(p0, p1, p2, p3)
        tsquared = t**2
        tcubic = tsquared*t
        return a*tcubic + b*tsquared + c*t + p0

    def make_plot(self,maker1,maker2,matrix_gff1,matrix_gff2,pair,chro1,chro2,x1,x2,maker_str,length1,length2):
        fig1 = plt.figure(num=1, figsize=(10, 10))  # 确保正方形在屏幕上显示一致，固定figure的长宽相等
        axes1 = fig1.add_subplot(1, 1, 1)
        plt.xlim((0, 1))
        plt.ylim((0, 1))
        self.map1(axes1,maker1,0.1,0.3,x1,'k')# 长染色体0.8
        self.map1(axes1,maker2,0.1+((0.8-x2)/2),0.65,x2,'k')# 短染色体
        if maker_str:
            plt.text(0.45, 0.28, chro1)
            plt.text(0.45, 0.67, chro2)
        else:
            plt.text(0.45, 0.28, chro2)
            plt.text(0.45, 0.67, chro1)
        plt.axis('off')
        self.pair_index(axes1,matrix_gff1,matrix_gff2,pair,chro1,chro2,x1,x2,maker_str,length1,length2)
        plt.savefig(self.savefile,dpi=1000)

    def map1(self,axes1,maker,x,y,x1,color):
        # makers = 15 #标尺
        # x = 0.1 #起始坐标x
        # y = 0.1 #起始坐标y
        # x1 = 0.8#染色体长度
        # color='k'
        lw = 1  #比例线宽
        y1 = 0.001
        w = 0.01
        alpha = 1
        # print(y+w+y1, x, x+x1,y, x, x+x1, lw)
        plt.axhline(y=y, xmin=x, xmax=x+x1, lw=lw, c=color, alpha=alpha)
        plt.axhline(y=y+w+y1, xmin=x, xmax=x+x1, lw=lw, c=color, alpha=alpha)
        for i in range(maker):
            mx = x + ((x1/maker)*i)
            plt.axvline(x=mx, ymin=y, ymax=y+(w/2.5), lw=lw, c=color, alpha=alpha)
        base1 = Arc(xy=(x, y+((w+y1)/2)),    # 椭圆中心，（圆弧是椭圆的一部分而已）
                width=w+y1,    # 长半轴
                height=w+y1,    # 短半轴
                angle=90,    # 椭圆旋转角度（逆时针） 
                theta1=0,    # 圆弧的起点处角度
                theta2=180,    # 圆度的终点处角度
                color=color,
                alpha=alpha,
                linewidth=lw
                )
        base2 = Arc(xy=(x1+x, y+((w+y1)/2)),    # 椭圆中心，（圆弧是椭圆的一部分而已）
                width=w+y1,    # 长半轴
                height=w+y1,    # 短半轴
                angle=-90,    # 椭圆旋转角度（逆时针） 
                theta1=0,    # 圆弧的起点处角度
                theta2=180,    # 圆度的终点处角度
                color=color,
                alpha=alpha,
                linewidth=lw   #线宽像素
                )
        axes1.add_patch(base1)
        axes1.add_patch(base2)
        
    def pair_index(self,axes1,matrix_gff1,matrix_gff2,pair,chro1,chro2,x1,x2,maker_str,length1,length2):
        pairs = []
        for i in pair:
            for j in i:
                if str(str(j[0]).split('^')[0]) == self.chr1_name and str(str(j[1]).split('^')[0]) == self.chr2_name:
                    name11 = str(j[0]).replace("^", "g")
                    name22 = str(j[1]).replace("^", "g")
                    index1 = matrix_gff1.loc[name11,5]
                    index2 = matrix_gff2.loc[name22,5]
                    # print(index1,index2,'index')
                    if maker_str:
                        prop1 = x1/length1
                        prop2 = x2/length2
                        # print(length1,length2)
                        # pair_lt = [[0.1+index1*prop1,0.3],[0.1+((0.8-x2)/2)+index2*prop2,0.65]]
                        # pairs.append(pair_lt)
                        self.plot_bez_inner(0.1+((0.8-x2)/2)+index2*prop2,0.65-0.004,0.1+index1*prop1,0.3+0.01+0.004)
                        # plt.plot([0.1+((0.8-x2)/2)+index2*prop2,0.1+index1*prop1],[0.65-0.004,0.3+0.01+0.004],c='g')
                    else:
                        prop1 = x2/length1
                        prop2 = x1/length2
                        # pair_lt = [[0.1+index2*prop2,0.3],[0.1+((0.8-x2)/2)+index1*prop1,0.65]]
                        # pairs.append(pair_lt)
                        self.plot_bez_inner(0.1+((0.8-x2)/2)+index1*prop1,0.65-0.004,0.1+index2*prop2,0.3+0.01+0.004)
                        # plt.plot([0.1+((0.8-x2)/2)+index1*prop1,0.1+index2*prop2],[0.65-0.004,0.3+0.01+0.004],c='r')
    def run(self):
        x1,x2,maker1,maker2,matrix_gff1,matrix_gff2,chro1,chro2,maker_str,length1,length2 = self.read_csv()
        pair = self.read_colinearscan(self.pairs_file)
        self.make_plot(maker1,maker2,matrix_gff1,matrix_gff2,pair,chro1,chro2,x1,x2,maker_str,length1,length2)
# iclmap0 = iclmap()
# x1,x2,maker1,maker2,matrix_gff1,matrix_gff2,chro1,chro2,maker_str,length1,length2 = iclmap0.read_csv()
# pair = iclmap0.read_colinearscan('ssu_mes.collinearity')
# iclmap0.make_plot(maker1,maker2,matrix_gff1,matrix_gff2,pair,chro1,chro2,x1,x2,maker_str,length1,length2)
