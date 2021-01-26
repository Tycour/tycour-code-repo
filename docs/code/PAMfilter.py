import re
import pandas as pd
import xlrd
import csv

from openpyxl import load_workbook

pam='NGG'

df = pd.read_excel('~/Downloads/candidateYkmers.xltx')

def PAMfilter(df, pam):
    '''
    Input: a list of kmer DNA sequences
    Output: a list of candidate gRNAs filtered by PAM sequence
    '''

    pam_len = len(pam)

    iupac_dict = {
        'A': 'A',
        'C': 'C',
        'G': 'G',
        'T': 'T',
        'R': '[AG]',
        'Y': '[CT]',
        'S': '[GC]',
        'W': '[AT]',
        'K': '[GT]',
        'M': '[AC]',
        'B': '[CGT]',
        'D': '[AGT]',
        'H': '[ACT]',
        'V': '[ACG]',
        'N': '[ACGT]',
    }
    iupac_pam = ''.join([iupac_dict[letter] for letter in pam])
    pattern = re.compile(iupac_pam)

    correct_indexes = []
    for index in df.index:
        if pattern.match(df['seq'][index][-3:]):
            correct_indexes.append(index)
    print(correct_indexes)
    # correct_indexes = [index for index in df.index if pattern.match(df['seq'][index][-pam_len:])]

    corrected_df = df.loc[correct_indexes]

    corrected_df.to_csv('filteredYkmers.csv')


    # with open('filteredYkmers.csv', 'wb') as file:
    #     for line in filtered_candidates:
    #         file.write(line)
    #         file.write('\n')

    # return filtered_candidates



# PAMfilter(df, pam)