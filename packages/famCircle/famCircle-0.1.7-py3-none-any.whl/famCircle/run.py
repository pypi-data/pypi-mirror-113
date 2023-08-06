# -*- coding: UTF-8 -*-
import argparse
import os
import sys
import configparser
import pandas as pd
import famCircle
import famCircle.bez as bez
from famCircle.hmmer import hmmer
from famCircle.screen import screen
from famCircle.Ks_allocation import Ks_allocation
from famCircle.Ks import Ks
from famCircle.Ks_block import Ks_block
from famCircle.circle import circle
from famCircle.line import line
from famCircle.circle_all import circle_all
from famCircle.outer import outer
from famCircle.inner import inner
from famCircle.typing import typing
from famCircle.part import part

parser = argparse.ArgumentParser(
    prog = 'famCircle', usage = '%(prog)s [options]', epilog = "", formatter_class = argparse.RawDescriptionHelpFormatter,)
parser.description = '''\
圈图构建
    -------------------------------------- '''
parser.add_argument("-v", "--version", action = 'version', version='0.1.7')
parser.add_argument("-hmm", dest = "hmmer",
                    help = "Gene family identification;基因家族鉴定")
parser.add_argument("-s", dest = "screen",
                    help = "Number and distribution of domains;结构域数量与分布")
parser.add_argument("-ks", dest = "Ks",
                    help = "blast Ks;计算blast")
parser.add_argument("-ka", dest = "Ks_allocation",
                    help = "Genome-wide KS visualization;全基因组Ks可视化")
parser.add_argument("-kb", dest = "Ks_block",
                    help = "block KS visualization;block Ks可视化")
parser.add_argument("-t", dest = "typing",
                    help = "Domain data normalization;结构域数据标准化")
parser.add_argument("-c", dest = "circle",
                    help = "Collinear visualization;共线性可视化")
parser.add_argument("-l", dest = "line",
                    help = "Collinear visualization;共线性可视化")
parser.add_argument("-ca", dest = "circle_all",
                    help = "Collinear visualization;共线性可视化")
parser.add_argument("-o", dest = "outer",
                    help = "Radiating gene families and collinearity visualization;放射状基因家族及共线性可视化")
parser.add_argument("-i", dest = "inner",
                    help = "Gene family circle map;基因家族圈图")
parser.add_argument("-p", dest = "part",
                    help = "Partial repeat gene;局部重复基因")

args = parser.parse_args()

def run_hmmer():
    options = bez.load_conf(args.hmmer, 'hmmer')
    hmmer1 = hmmer(options)
    hmmer1.run()

def run_screen():
    options = bez.load_conf(args.screen, 'screen')
    screen1 = screen(options)
    screen1.run()

def run_Ks_allocation():
    options = bez.load_conf(args.Ks_allocation, 'Ks_allocation')
    lookKs1 = Ks_allocation(options)
    lookKs1.run()

def run_Ks():
    options = bez.load_conf(args.Ks, 'Ks')
    lookKs0 = Ks(options)
    lookKs0.run()

def run_Ks_block():
    options = bez.load_conf(args.Ks_block, 'Ks_block')
    lookKs0 = Ks_block(options)
    lookKs0.run()

def run_typing():
    options = bez.load_conf(args.typing, 'typing')
    typing1 = typing(options)
    typing1.run()

def run_circle():
    options = bez.load_conf(args.circle, 'circle')
    circle1 = circle(options)
    circle1.run()

def run_line():
    options = bez.load_conf(args.line, 'line')
    circle1 = line(options)
    circle1.run()

def run_circle_all():
    options = bez.load_conf(args.circle_all, 'circle_all')
    circle0 = circle_all(options)
    circle0.run()

def run_outer():
    options = bez.load_conf(args.outer, 'outer')
    outer1 = outer(options)
    outer1.run()

def run_inner():
    options = bez.load_conf(args.inner, 'inner')
    inner1 = inner(options)
    inner1.run()

def run_part():
    options = bez.load_conf(args.part, 'part')
    inner1 = part(options)
    inner1.run()

def module_to_run(argument):
    switcher = {
        'hmmer': run_hmmer,
        'screen': run_screen,
        'Ks_allocation': run_Ks_allocation,
        'Ks': run_Ks,
        'Ks_block': run_Ks_block,
        'typing': run_typing,
        'circle': run_circle,
        'line': run_line,
        'circle_all': run_circle_all,
        'outer': run_outer,
        'inner': run_inner,
        'part': run_part,
    }
    return switcher.get(argument)()

def main():
    path = famCircle.__path__[0]
    options = {
               'hmmer': 'hmmer.conf',
               'screen': 'screen.conf',
               'Ks_allocation': 'Ks_allocation.conf',
               'Ks': 'Ks.conf',
               'Ks_block': 'Ks_block.conf',
               'typing': 'typing.conf',
               'circle': 'circle.conf',
               'line': 'line.conf',
               'circle_all': 'circle_all.conf',
               'outer': 'outer.conf',
               'inner': 'inner.conf',
               'part': 'part.conf',
               }
    for arg in vars(args):
        value = getattr(args, arg)
        # print(value)
        if value is not None:
            if value in ['?', 'help', 'example']:
                f = open(os.path.join(path, 'example', options[arg]))
                print(f.read())
            elif value == 'e':
                out = '''\
        File example
        [fpchrolen]
        chromosomes number_of_bases
        *   *
        *   *
        *   *
        [fpgff]
        chromosomes gene    start   end
        *   *   *   *
        *   *   *   *
        *   *   *   *
        [fpgenefamilyinf]
        gene1   gene2   Ka  Ks
        *   *   *   *
        *   *   *   *
        *   *   *   *
        [alphagenepairs]
        gene1   gene2
        *   *   *
        *   *   *
        *   *   *

        The file columns are separated by Tab
        -----------------------------------------------------------    '''
                print(out)
            elif not os.path.exists(value):
                print(value+' not exits')
                sys.exit(0)
            else:
                module_to_run(arg)

