# -*- coding: UTF-8 -*-
import configparser
import os
import re
import famCircle
import numpy as np
import pandas as pd
from Bio import Seq, SeqIO, SeqRecord
import codecs
# Bezier functions

def config():
    conf = configparser.ConfigParser()
    conf.read(os.path.join(famCircle.__path__[0], 'conf.ini'))
    return conf.items('ini')

def load_conf(file, section):
    conf = configparser.ConfigParser()
    conf.read(file)
    return conf.items(section)

def calculate_coef(p0, p1, p2, p3):
    c = 3*(p1 - p0)
    b = 3*(p2 - p1) -c
    a = p3 - p0 - c - b
    return c, b, a

def Bezier(plist, t):
    # p0 : origin, p1, p2 :control, p3: destination
    p0, p1, p2, p3 = plist
    # calculates the coefficient values
    c, b, a = calculate_coef(p0, p1, p2, p3)
    tsquared = t**2
    tcubic = tsquared*t
    return a*tcubic + b*tsquared + c*t + p0

def gene_length(gfffile):
    # 读取基因长度，得到平均长度和最小最大长度
    f = open(gfffile,'r', encoding='utf-8')
    genelength = {}
    for row in f:
        if row[0] != '\n' and row[0] != '#':
            row = row.strip('\n').split('\t')
            if str(row[1]) in genelength.keys():
                continue
            if 'chr' == str(row[1])[3:6]:
                continue
            length = abs(int(row[3]) - int(row[2]))
            genelength[str(row[1])] = length
    f.close()
    lt = []
    for i in genelength.values():
        lt.append(i)
    pj = sum(lt)/len(lt)
    return pj

def gene_length_order(lensfile):
    # 读取基因长度，得到平均长度和最小最大长度
    f = open(lensfile,'r', encoding='utf-8')
    gene_sum = 0
    gene_index = 0
    for row in f:
        if row[0] != '\n' and row[0] != '#':
            row = row.strip('\n').split('\t')
            gene_sum = gene_sum + int(row[2])
            gene_index = gene_index + int(row[1])
    f.close()
    pj = gene_index/gene_sum
    return pj

def cds_to_pep(cds_file, pep_file, fmt='fasta'):
    records = list(SeqIO.parse(cds_file, fmt))
    for k in records:
        k.seq = k.seq.translate()
    SeqIO.write(records, pep_file, 'fasta')
    return True

def read_colinearscan(file):
    data, b, flag, num = [], [], 0, 1
    with open(file) as f:
        for line in f.readlines():
            line = line.strip()
            if re.match(r"the", line):
                num = re.search('\d+', line).group()
                b = []
                flag = 1
                continue
            if re.match(r"\>LOCALE", line):
                flag = 0
                p = re.split(':', line)
                if len(b) > 0:
                    data.append([num, b, p[1]])
                b = []
                continue
            if flag == 1:
                a = re.split(r"\s", line)
                b.append(a)
    return data


def read_mcscanx(fn):
    f1 = open(fn)
    data, b = [], []
    flag, num = 0, 0
    for line in f1.readlines():
        line = line.strip()
        if re.match(r"## Alignment", line):
            flag = 1
            if len(b) == 0:
                arr = re.findall(r"[\d+\.]+", line)[0]
                continue
            data.append([num, b, 0])
            b = []
            num = re.findall(r"\d+", line)[0]
            continue
        if flag == 0:
            continue
        a = re.split(r"\:", line)
        c = re.split(r"\s+", a[1])
        b.append([c[1], c[1], c[2], c[2]])
    data.append([num, b, 0])
    return data


def read_jcvi(fn):
    f1 = open(fn)
    data, b = [], []
    num = 1
    for line in f1.readlines():
        line = line.strip()
        if re.match(r"###", line):
            if len(b) == 0:
                continue
            data.append([num, b, 0])
            b = []
            num += 1
            continue
        a = re.split(r"\t", line)
        b.append([a[0], a[0], a[1], a[1]])
    data.append([num, b, 0])
    return data


def read_coliearity(fn):
    f1 = open(fn)
    data, b = [], []
    flag, num = 0, 0
    for line in f1.readlines():
        line = line.strip()
        if re.match(r"# Alignment", line):
            flag = 1
            if len(b) == 0:
                arr = re.findall('[\.\d+]+', line)
                continue
            data.append([arr[0], b, arr[2]])
            b = []
            arr = re.findall('[\.\d+]+', line)
            continue
        if flag == 0:
            continue
        b.append(re.split(r"\s", line))
    data.append([arr[0], b, arr[2]])
    return data


def read_ks(file, col):
    ks = pd.read_csv(file, sep='\t')
    ks.drop_duplicates(subset=['id1', 'id2'], keep='first', inplace=True)
    ks[col] = ks[col].astype(float)
    ks = ks[ks[col] >= 0]
    ks.index = ks['id1']+','+ks['id2']
    return ks[col]
