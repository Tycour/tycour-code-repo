from Bio import SeqIO
from Bio.Seq import reverse_complement
import re
import pandas as pd

### Inputs
# Pacbio Reads


pacbio_reads_path = "/Users/thomascourty/Downloads/pacbio-kmer_78734079.0.fasta"

# kmer sequence
kmer_seq = "AGAAGAATAGAATCAGAAAAGTCGG"

# Execution
pacbio_readname = [pacbio_read.id for pacbio_read in SeqIO.parse(pacbio_reads_path, "fasta")]
columns = ['seq', 'matches_for', 'for_hits', 'matches_rev', 'rev_hits', 'total_hits']
pacbio_hits_df = pd.DataFrame(index=pacbio_readname, columns=columns)

for pacbio_read in SeqIO.parse(pacbio_reads_path, "fasta"):
    matches_for = [m.start() for m in re.finditer(kmer_seq, str(pacbio_read.seq))]
    for_hits = len(matches_for)
    matches_rev = [m.start() for m in re.finditer(reverse_complement(kmer_seq), str(pacbio_read.seq))]
    rev_hits = len(matches_rev)
    total_hits = for_hits + rev_hits
    pacbio_hits_df.at[pacbio_read.id, 'matches_for'] = str(matches_for)
    pacbio_hits_df.at[pacbio_read.id, 'seq'] = str(pacbio_read.seq)
    pacbio_hits_df.at[pacbio_read.id, 'for_hits'] = for_hits
    pacbio_hits_df.loc[pacbio_read.id]['matches_rev'] = str(matches_rev)
    pacbio_hits_df.at[pacbio_read.id, 'rev_hits'] = rev_hits
    pacbio_hits_df.loc[pacbio_read.id]['total_hits'] = total_hits

# Output (.csv?)
pacbio_hits_df.to_csv('pacbio_hits_df.csv')
