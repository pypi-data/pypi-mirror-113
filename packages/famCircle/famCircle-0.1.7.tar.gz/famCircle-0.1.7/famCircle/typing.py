import os
import numpy as np
import pandas as pd

class typing():
    def __init__(self, options):
        for k, v in options:
            setattr(self, str(k), v)
            print(k, ' = ', v)

    def readoutfile(self):
        out_list = str(self.domainlist).split(',')
        fam_out = []
        for i in out_list:
            pathlist = self.domainpath + '/' + str(i)
            f = open(pathlist, 'r', encoding='utf-8')
            for row in f:
                if row[0] != '#' and row[0] != '\n':
                    row = row.strip('\n').split()
                    fam_out.append(row)
        df = pd.DataFrame(fam_out)
        df.rename(columns={0: 'target_name', 1: 'accession',
                                2: 'tlen', 3: 'query_name', 4: 'accession1', 5: 'qlen',
                                6: 'E-value', 7: 'score', 8: 'bias', 9: '#', 10: 'of', 11: 'c-Evalue',
                                12: 'i-Evalue', 13: 'score2', 14: 'bias2', 15: 'from', 16: 'to',
                                17: 'from1', 18: 'to1', 19: 'from2', 20: 'to2', 21: 'acc',
                                22: 'description_of_target'}, inplace=True)
        df.drop_duplicates(subset = 'target_name')# 去重
        return df

    def readks(self):
        read_ks = []
        f = open('ath_ath.collinearity.ks', 'r', encoding='utf-8')
        for row in f:
            if row[0] != '#' and row[0] != '\n':
                row = row.strip('\n').split('\t')
                if row[0] != 'id1' and len(row) != 2:
                    read_ks.append(row)
        kspd = pd.DataFrame(read_ks)
        kspd.rename(columns={0: 'id1', 1: 'id2',
                                2: 'ka_NG86', 3: 'ks_NG86',
                                4: 'ka_YN00', 5: 'ks_YN00'}, inplace=True)
        return kspd

    def run(self):
        df = self.readoutfile()
        # kspd = self.readks()
        fam_name = np.array(df['target_name'].astype(str))
        # ks_lt = np.array(kspd[['id1','id2']])
        # if self.position == 'outer':
        #     for i,j in ks_lt:
        #             if i in fam_name and j in fam_name:
        #                 with open(self.savefile, "a", newline='', encoding='utf-8') as file:
        #                     file.write(i + '\t' + j + '\n')
        #                     file.close()
        # elif self.position == 'inner':
        for i in fam_name:
            with open(self.savefile, "a", newline='', encoding='utf-8') as file:
                file.write(i + '\n')
                file.close()