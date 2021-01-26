import re
import pandas as pd
import xlrd

pam='NGG'
df = pd.read_excel('~/Downloads/candidateYkmers.xltx')

def IUPAC_to_Pattern(pam):
    '''
    Reads an IUPAC format Protospacer Adjacent Motif (PAM) and compiles every permutation into a 'pattern' readable by re
    '''
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
    return pattern

def PAMfilter(df, pam):

    pam_len = len(pam)
    pattern = IUPAC_to_Pattern(pam)

    ### Create list of indices corresponding to kmers with correct PAM sequence
    correct_indexes = []
    for index in df.index:
        # First brackets after 'df' indicate column name, the second indicate index (#), the third indicate position in value at that cell in the df
        # Checks if the final letters in the kmer match the pattern
        if pattern.match(df['seq'][index][-pam_len:]):
            correct_indexes.append(index)

    ### Shorter way to do the same thing as above (list comprehension)
    # correct_indexes = [index for index in df.index if pattern.match(df['seq'][index][-pam_len:])]

    ### Make new dataframe whose indices
    corrected_df = df.loc[correct_indexes]

    ### Save the dataframe to a new file
    corrected_df.to_csv('filteredYkmers.csv')

    print('Filtered file is saved in your current repository.')

    return


### Execution
PAMfilter(df, pam)