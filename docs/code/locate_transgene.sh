# Locating Random Transgene Insertions Bioinformatics Pipeline (2021)
# Thomas Courty, Sr Research Technician - Crisanti Lab, Imperial College London

# Conda packages to install:
# filtlong
# NanoPlot
# minimap2
# samtools

# 1. Preparing Files (on Lab Linux)

# cat *.fastq > lineName_pass.fastq
# gzip lineName_pass.fastq > lineName.fastq.gz

# 2. Generating Sequencing Statistics

NanoPlot --fastq lineName_pass.fastq.gz -o NanoPlot

# 3. Filtering Reads

filtlong --min_length 1000 --min_mean_q 75 lineName_pass.fastq.gz > lineName_filter.fastq.gz

# 4. Aligning Reads to Reference Genome

minimap2 -a -o lineName_AgamP4_align.sam AgamP4_lineName.fasta lineName_filter.fastq.gz

# 5. Sorting & Indexing the Alignment

samtools sort lineName_AgamP4_align.sam > lineName_AgamP4_align.sorted.bam
samtools index lineName_AgamP4_align.sorted.bam

# 6. Visualising in IGV

# Load the genome reference with your contruct added on:
# Genomes
# Load Genome from File

# Load your sorted alignment file:
# File
# Load from File

# Go to the contig that represents your construct and click on reads that cover the end of the construct. If successful, these should reveal supplementary alignments in the genome which you can manually checkout!

### END