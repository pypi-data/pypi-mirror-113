# -*- coding: UTF-8 -*-
import re
import sys
from math import *

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import *
from matplotlib.patches import Circle, Ellipse
from pylab import *

from famCircle.bez import *


class circle():
    def __init__(self, options):
    ##### circle parameters
        self.GAP_RATIO = 4 #gaps between chromosome circle, chr:gap = 4: 1
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
        fpgenefamilyinf = open(self.ks, 'r', encoding='utf-8')
        alphagenepairs = open(self.genepairs, 'r', encoding='utf-8')
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
            # sp = chro[:2].upper()
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
        #    print gene, int(start), self.gene2chain
        fpgff.close()
        ### input gene family gene1 gene2 Ka Ks
        for row in fpgenefamilyinf:
            if (row.split()[0] == 'id1'):
                continue
            if len(row.split('\t')) < 4:
                continue
            gene1, gene2, Ka, Ks = row.split()[0],row.split()[1],row.split()[2],row.split()[3]
            gene1 = self.readname(gene1)
            gene2 = self.readname(gene2)
            if (gene1 not in self.gene2pos.keys() or gene2 not in self.gene2pos.keys()):
                continue
            genepair = ""
            if gene1 < gene2:
               genepair = gene1 + " " + gene2
            else:
               genepair = gene2 + " " + gene1
            if (gene1.split("^")[0] not in self.otherchrolist or gene2.split("^")[0] not in self.otherchrolist):
               continue
            if len(gene1.split("^")[0]) < 10  and len(gene2.split("^")[0]) < 10 :
               self.genepair2Ka[genepair] = float(Ka)
               self.genepair2Ks[genepair] = float(Ks)
            if gene1 not in self.genes:
                if len(gene1.split("^")[0]) < 10:
                         self.genes.append(gene1)
            if gene2 not in self.genes :
                if len(gene2.split("^")[0]) < 10:
                     self.genes.append(gene2)
        fpgenefamilyinf.close()
        return root

    def rad_to_coord(self, angle, radius):
        return radius*cos(angle), radius*sin(angle)

    def to_radian(self, bp, total):
        # from basepair return as radian
        # print ("to_radian", bp, total)
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
        # print(total_size)
        plot(xt, yt, '-', color=cl, lw=0.3, alpha = alp)#alpha 

    def run(self):
        self.radius_a = float(self.radius)
        self.radius_b = self.radius_a + 0.005
        self.sm_radius=(self.radius_b-self.radius_a)/2 #telomere capping
        root = self.ksrun()
        gene_average = gene_length(self.gff)
        stop_list, total_size, chr_number = self.zj()
        alphagenepairs = open(self.genepairs, 'r', encoding='utf-8')
        ## sort gene according to lacation on circle
        genessorted = []
        geneno = 0
        for i in range(len(self.genes)):
        #    print i, genes[i]

            if geneno == 0:
                genessorted.append(self.genes[0])
                geneno = geneno + 1
            else:
                firstgene = genessorted[0]
                lastgene = genessorted[-1]
                chf = firstgene.split("^")[0]
                chl = lastgene.split("^")[0]
                if (chf not in self.otherchrolist or chl not in self.otherchrolist):
                    continue
                #print firstgene, lastgene, chf, chl, self.gene2pos[firstgene]
                posf = self.gene2pos[firstgene] + self.start_list[self.labels.index(chf)]
                posl = self.gene2pos[lastgene] + self.start_list[self.labels.index(chl)]
                chi = self.genes[i].split("^")[0]
                posi = self.gene2pos[self.genes[i]] + self.start_list[self.labels.index(chi)]
        #        print posf, posl, posi
                if posi <= posf:
                    genessorted[0:0] = [self.genes[i]]
                elif posi >= posl:
                    genessorted.append(self.genes[i])
                else:
                    for j in range(len(genessorted)-1):
                        chj = genessorted[j].split("^")[0]
                        posj = self.gene2pos[genessorted[j]] + self.start_list[self.labels.index(chj)]
                        chj1 = genessorted[j+1].split("^")[0]
                        posj1 = self.gene2pos[genessorted[j+1]]+self.start_list[self.labels.index(chj1)]
                        #print posj, posj1, posi
                        if posi > posj and posi < posj1:
                            genessorted[j+1:j+1] = [self.genes[i]]
        ###########
        ###########alpha genepairs
        row = alphagenepairs.readline()#
        rowno = 0
        istoread = 0
        data1 = []
        data2 = []
        data3 = []
        data4 = []
        data5 = []
        for row in alphagenepairs:
            if (row[0] == '\n'):
                continue
            elif (row[0] == '#'):
                lt = row.strip('\n').split(' ')
                block = {}
                for i in lt:
                    if '=' in str(i):
                        lt0 = i.split('=')
                        block[str(lt0[0])] = str(lt0[1])
                N = int(block['N'])
                if N >= int(self.block):
                    self.class1 = True
                else :
                    self.class1 = False
            else:
                if self.class1:
                    seqname = []
                    
                    for i in self.species_list.strip('\n').split('_'):
                        seqname.append(i[:2])
                    lt = row.strip('\n').split()
                    try :
                        if (lt[2][:2] in seqname):
                            id1, id2 = row.split()[0],row.split()[2]
                    except:
                        id1, id2 = row.split()[0],row.split()[1]
                    if (id1[1] == '*'):
                        id1 = id1[2:]
                        col = id1[0]
                    else:
                        col = 'green'
                    id1 = self.readname(id1)
                    id2 = self.readname(id2)
                    if (id1 not in self.gene2pos.keys() or id2 not in self.gene2pos.keys()):
                        continue
                    pos1 = self.gene2pos[id1]
                    pos2 = self.gene2pos[id2]
                    chro1 = id1.split("^")[0]
                    chro2 = id2.split("^")[0]
                    if (chro1 not in self.otherchrolist or chro2 not in self.otherchrolist):
                        continue
                    sp1 = chro1[0:2]
                    sp2 = chro2[0:2]
                    # print(chro1,chro2)
                    if(chro1 not in self.labels or chro2 not in self.labels):
                        continue
                    order1 = self.labels.index(chro1)
                    order2 = self.labels.index(chro2)
                    # print(abs(pos1 - pos2))
                    # print(order1, pos1, self.radius_a, order2, pos2, self.radius_a)
                    if id1.split('^')[0] == id2.split('^')[0] and abs(pos1 - pos2) < (100 * gene_average):
                        data1.append([order1, pos1, self.radius_a, order2, pos2, self.radius_a, 'lime', total_size,0.3])
                        # self.plot_bez_inner((order1, pos1, self.radius_a), (order2, pos2, self.radius_a), 'silver', total_size)
                        # pass
                    elif id1.split('^')[0] == id2.split('^')[0] and abs(pos1 - pos2) < (400 * gene_average):
                        data2.append([order1, pos1, self.radius_a, order2, pos2, self.radius_a, 'cyan', total_size,0.2])
                        # self.plot_bez_inner((order1, pos1, self.radius_a), (order2, pos2, self.radius_a), 'silver', total_size)
                        # pass
                    else:
                        data3.append([order1, pos1, self.radius_a, order2, pos2, self.radius_a, 'silver', total_size,0.1])
                        # self.plot_bez_inner((order1, pos1, self.radius_a), (order2, pos2, self.radius_a), "lime", total_size)
                        # pass
                    rowno = rowno + 1
                else:
                    # pass
                    seqname = []
                    for i in self.species_list.strip('\n').split('_'):
                        seqname.append(i[:2])
                    lt = row.strip('\n').split()
                    try :
                        if (lt[2][:2] in seqname):
                            id1, id2 = row.split()[0],row.split()[2]
                    except:
                        id1, id2 = row.split()[0],row.split()[1]
                    if (id1[1] == '*'):
                        id1 = id1[2:]
                        col = id1[0]
                    else:
                        col = 'green'
                    id1 = self.readname(id1)
                    id2 = self.readname(id2)
                    if (id1 not in self.gene2pos.keys() or id2 not in self.gene2pos.keys()):
                        continue
                    pos1 = self.gene2pos[id1]
                    pos2 = self.gene2pos[id2]
                    chro1 = id1.split("^")[0]
                    chro2 = id2.split("^")[0]
                    if (chro1 not in self.otherchrolist or chro2 not in self.otherchrolist):
                        continue
                    sp1 = chro1[0:2]
                    sp2 = chro2[0:2]
                    if(chro1 not in self.labels or chro2 not in self.labels):
                        continue
                    order1 = self.labels.index(chro1)
                    order2 = self.labels.index(chro2)
                    if id1.split('^')[0] == id2.split('^')[0] and abs(pos1 - pos2) < (100 * gene_average):
                        data4.append([order1, pos1, self.radius_a, order2, pos2, self.radius_a, '#b44c97', total_size,0.2])
                    else:
                        data5.append([order1, pos1, self.radius_a, order2, pos2, self.radius_a, '#ee7800', total_size,0.15])
                    rowno = rowno + 1

        for i in data3:
            self.plot_bez_inner((i[0],i[1],i[2]),(i[3],i[4],i[5]),i[6],i[7],i[8])
        # for i in data5:
        #     self.plot_bez_inner((i[0],i[1],i[2]),(i[3],i[4],i[5]),i[6],i[7],i[8])
        # for i in data2:
        #     self.plot_bez_inner((i[0],i[1],i[2]),(i[3],i[4],i[5]),i[6],i[7],i[8])
        for i in data1:
            self.plot_bez_inner((i[0],i[1],i[2]),(i[3],i[4],i[5]),i[6],i[7],i[8])
        for i in data4:
            self.plot_bez_inner((i[0],i[1],i[2]),(i[3],i[4],i[5]),i[6],i[7],i[8])

        alphagenepairs.close()
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
