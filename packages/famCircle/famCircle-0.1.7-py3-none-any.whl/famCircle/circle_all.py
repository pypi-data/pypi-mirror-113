# -*- coding: UTF-8 -*-
import re
import sys
from math import *
import gc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import *
from matplotlib.patches import Circle, Ellipse
from pylab import *
from collections import Counter
from famCircle.bez import *


class circle_all():
    def __init__(self, options):
    ##### circle parameters
        self.GAP_RATIO = 5 #gaps between chromosome circle, chr:gap = 4: 1
        self.radius = 0.33
        self.block=0.01 #block scize
        self.blockthick = 0.004 #0.006
        self.shiftratio = -2.1 # define the distance between overlapping glocks
        self.specieslist = []
        self.iscompletegenome = {}
        self.gene2pos={}
        self.gene2chain = {}
        self.chro2len = {}
        self.otherchrolist = []
        self.labels = []
        self.genes = []
        self.genepair2Ks = {}
        self.genepair2Ka = {}
        self.block = '0'
        self.class1 = True
        self.start_list = []
        self.colornum = 1
        self.color = [ '#a0d8ef', '#c7b370', '#eb6ea5', '#0094c8', '#b8d200', '#00a497'
                      , '#d9333f', '#3e62ad', '#aacf53', '#f6ad49', '#e9e4d4', '#f39800'
                      , '#98d98e', '#ffd900', '#68be8d', '#745399', '#028760', '#c0a2c7']
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def readname(self, name):
        if ('^' in name):
            return name
        elif ('g' in name):
            if 'g' not in self.species_list:
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

    def ksrun(self):
        fpchrolen = open(self.lens,'r', encoding='utf-8')
        fpgff = open(self.gff,'r', encoding='utf-8')
        #### gene block parameters
        figure(1, (8, 8))  ### define the a square, or other rectangle of the figure, if to produce an oval here
        root =axes([0, 0, 1, 1])
        lengthset = set()
        for i in self.species_list.strip('\n').split('_'):
            lengthset.add(len(i))
        chrolist = []
        for row in fpchrolen:
            chro = row.split('\t')[0]
            for i in lengthset:
                if (chro[:i] in self.species_list.strip('\n').split('_')):
                    chrolist.append(chro)
                else:
                    pass
        fpchrolen.close()
        for i in range(len(chrolist)):
            string = chrolist[i]
        #   print string[0:2]
            isnew = 1
            for sp in self.specieslist:
                if sp == string[0:2]:
                    isnew = 0
                    break
            if isnew==1:
                self.specieslist.append(string[0:2])
                if string == string[0:2]:
                    self.iscompletegenome[string[0:2]] = 1
                else:
                    self.iscompletegenome[string[0:2]] = 0
        ### input chromosome length
        fpchrolen = open(self.lens,'r', encoding='utf-8')
        for row in fpchrolen:
            if row[0] == '#' or row == '\n':
                continue
            chro,length = row.split('\t')[0],row.split('\t')[1]
            # chro = chro.upper()
            if len(chro) > 10 :
                continue
            sp = chro[:2]
            if self.iscompletegenome[sp] == 1 :
                self.chro2len[chro] = int(length)
                self.otherchrolist.append(chro)
            else:
                if chro in chrolist :
                    self.chro2len[chro] = int(length)
                    self.otherchrolist.append(chro)
        fpchrolen.close()
        ### full chro list
        for i in self.otherchrolist:
            self.labels.append(i)
        for row in fpgff:
            ch, gene, start, end = row.split()[0],row.split()[1],row.split()[2],row.split()[3]
            gene = self.readname(gene)
            start = int(start)
            end = int(end)
            self.gene2pos[gene] = int(start)
            # print(start)
            self.gene2chain[gene] = int((end-start)/abs(end -start))
        fpgff.close()
        return root

    def rad_to_coord(self, angle, radius):
        return radius*cos(angle), radius*sin(angle)

    def to_radian(self, bp, total):
        # from basepair return as radian
        return radians(bp*360./total)

    def plot_arc(self, start, stop, radius):
        # start, stop measured in radian
        t = arange(start, stop, pi/720.)
        x, y = radius*cos(t), radius*sin(t)
        plot(x, y, "k-", alpha=.5)# 染色体圆弧

    def plot_cap(self, angle, clockwise):
        radius=self.sm_radius
        # angle measured in radian, clockwise is boolean
        if clockwise: 
            t = arange(angle, angle+pi, pi/30.)
        else: 
            t = arange(angle, angle-pi, -pi/30.)
        x, y = radius*cos(t), radius*sin(t)
        middle_r = (self.radius_a+self.radius_b)/2
        x, y = x + middle_r*cos(angle), y + middle_r*sin(angle)
        plot(x, y, "k-", alpha=.5)# 边缘

    def zj(self):
        fullchrolen = int(pd.DataFrame(self.chro2len.values()).sum())
        chr_number = len(self.labels) # total number of chromosomes
        GAP = fullchrolen/self.GAP_RATIO/chr_number # gap size in base pair
        total_size = fullchrolen + chr_number * GAP # base pairs
        for i in range(chr_number):
            self.start_list.append(0)
        for i in range(1, chr_number):
            self.start_list[i] = self.start_list[i-1] + self.chro2len[self.labels[i-1]] + GAP
        stop_list = [(self.start_list[i] + self.chro2len[self.labels[i]]) for i in range(chr_number)]
        return stop_list, total_size, chr_number

    def transform_pt(self, ch, pos, r, total_size):
        rad = self.to_radian(pos + self.start_list[ch], total_size)
        return r*cos(rad), r*sin(rad)

    def readblast(self):
        one_gene = []
        alphagenepairs = open(self.blockfile, 'r', encoding='utf-8')
        chrnum = []
        for row in alphagenepairs:
            if (row[0] == '\n'):
                continue
            else:
                lt = row.strip('\n').split()
                id1, id2 = str(lt[0]),str(lt[2])
                id1 = self.readname(id1)
                id2 = self.readname(id2)
                if (id1 not in self.gene2pos.keys() or id2 not in self.gene2pos.keys()):
                    continue
                chro1 = id1.split("^")[0]
                chro2 = id2.split("^")[0]
                if (chro1 not in self.labels or chro2 not in self.labels):
                    continue
                one_gene.append([id1,id2])
                chr0 = str(id1.split('^')[0])
                if chr0 not in chrnum:
                    chrnum.append(chr0)
                else:
                    pass
        self.colornum = len(chrnum)
        alphagenepairs.close()
        blastlist = sorted(one_gene,key=(lambda x:x[0]))
        return blastlist

    def plot_bez_inner(self, p1, p2, cl, total_size,alp):
    #    print "inner"
        a, b, c = p1
        ex1x, ex1y = self.transform_pt(a, b, c, total_size)
        a, b, c = p2
        ex2x, ex2y = self.transform_pt(a, b, c, total_size)
        # Bezier ratio, controls curve, lower ratio => closer to center
        ratio = .5
        x = [ex1x, ex1x*ratio, ex2x*ratio, ex2x]
        y = [ex1y, ex1y*ratio, ex2y*ratio, ex2y]
        step = .01
        t = arange(0, 1+step, step)
        xt = Bezier(x, t)
        yt = Bezier(y, t)
        plot(xt, yt, '-', color=cl, lw=0.8, alpha = alp)#alpha 

    def run(self):
        self.radius_a = float(self.radius)
        self.radius_b = self.radius_a + 0.005
        self.sm_radius=(self.radius_b-self.radius_a)/2 #telomere capping
        root = self.ksrun()
        stop_list, total_size, chr_number = self.zj()
        ## sort gene according to lacation on circle
        blastlist = self.readblast()
        rowno = 0
        chrlist = []
        # for i in range(3):
        for lt in blastlist:
            id1, id2 = str(lt[0]),str(lt[1])
            pos1 = self.gene2pos[id1]
            pos2 = self.gene2pos[id2]
            chro1 = id1.split("^")[0]
            chro2 = id2.split("^")[0]
            sp1 = chro1[0:2]
            sp2 = chro2[0:2]
            if chro1 in chrlist:
                col = self.color[chrlist.index(chro1)]
            else:
                chrlist.append(chro1)
                col = self.color[len(chrlist) - 1]
            order1 = self.labels.index(chro1)
            order2 = self.labels.index(chro2)
            alp = 0.3
            if id1.split('^')[0] == id2.split('^')[0]:
                # self.plot_bez_inner((order1, pos1, self.radius_a), (order2, pos2, self.radius_a), 'y', total_size,alp)
                pass
            else:
                self.plot_bez_inner((order1, pos1, self.radius_a), (order2, pos2, self.radius_a), col, total_size,alp)
                # pass
            rowno = rowno + 1
        # the chromosome layout
        j = 0
        for start, stop in zip(self.start_list, stop_list):
            start, stop = self.to_radian(start, total_size), self.to_radian(stop, total_size)
            # shaft
            self.plot_arc(start, stop, self.radius_a)
            self.plot_arc(start, stop, self.radius_b)
            # telemere capping
            clockwise=False
            self.plot_cap(start, clockwise)
            clockwise=True
            self.plot_cap(stop, clockwise)
            # chromosome self.labels
            label_x, label_y = self.rad_to_coord((start+stop)/2, self.radius_b*1.1)# text
            #print label_x, label_y
            text(label_x, label_y, self.labels[j], horizontalalignment="center", verticalalignment="center", fontsize = 7, color = 'black')
            j+=1
        ########
        root.set_xlim(-.8, .8)#-.5, .5
        root.set_ylim(-.8, .8)
        root.set_axis_off()
        savefig(self.savefile, dpi=1000)
        sys.exit(0)
