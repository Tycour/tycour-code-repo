import re
import pandas as pd
import xlrd

### Inputs
# PAM is NGG by default
pam = 'NGG'
df = pd.read_excel('/Users/thomascourty/Downloads/candidateYkmers.xltx')
pb_list = open('/Users/thomascourty/Downloads/pac-reads-Kmer-allPAM.txt')


def rev_comp(seq):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    return ''.join([complement[base] for base in seq[::-1]])

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

def PAMfilter(df, pam, pb_list=None):

    pam_len = len(pam)
    pattern = IUPAC_to_Pattern(pam)
    pattern_rev = IUPAC_to_Pattern(rev_comp(pam))

    ### Create list of indexes corresponding to kmers with correct PAM sequence
    correct_indexes = []
    for index in df.index:
        # First brackets after 'df' indicate column name, the second indicate index (#), the third indicate position in value at that cell in the df
        # Checks if the final letters in the kmer match the pattern
        seq = df['seq'][index]
        if pattern.match(seq[-pam_len:]):
            correct_indexes.append(index)
        elif pattern_rev.match(seq[:pam_len]):
            print('hello')
            correct_indexes.append(index)

    ### Make new dataframe with correct indexes
    corrected_df = df.loc[correct_indexes]

    ### Add column data for pacbio read name
    kmer_to_pacbio = []
    with pb_list as file:
        for line in file:
            fields = line.split('\t')[:-1]
            kmer_id = fields[0]
            pb_read = fields[2]
            kmer_seq = fields[4]
            kmer_to_pacbio.append((kmer_id, pb_read, kmer_seq))

    corrected_df['pacbio_readname'] = ''

    for index in df.index:
        print(corrected_df['seq'][index])

    ### Save the dataframe to a new file
    # corrected_df.to_csv('filteredYkmers.csv')

    print('Filtered file is saved in your current repository.')

    return



### Execution
PAMfilter(df, pam, pb_list)

