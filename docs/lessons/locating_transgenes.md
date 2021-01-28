# Locating Transgene Insertions

Before starting this tutorial, you need to be familiar with using `conda` and installing packages in the terminal.

This tutorial is meant to be run on your own laptop and inside your own terminal.

If using Windows, you may need to install and use a Ubuntu/Linux Virtual Environment as many python packages do not support Windows OS.

Conda packages to install:
- filtlong
- NanoPlot
- minimap2


# 1. Preparing Files

MinKNOW/Guppy outputs reads in `.fast5` and `.fastq` formats. The fastq files are the ones we are interested in at the moment.

You can find these on the Lab's Linux in `/var/lib/MinKNOW/data/reads/`.

For downstream applications, you will need to merge all the fastq files in the `fastq_pass` folder into one. You may also want to compress the resulting file to reduce the file's size.

```
cat *.fastq > lineName_pass.fastq
```

```
gzip lineName_pass.fastq > lineName.fastq.gz
```

# 2. Generating Sequencing Statistics

Review how much coverage you got to inform how stringent the filtering step should be.
If you can see a spike of reads at 3.6kb, this might mean your library prep has failed.

```
NanoPlot --fastq lineName_pass.fastq.gz -o NanoPlot
```

#3. Filtering Reads

There are other options you can check out using `filtlong -h` that give you more control over filtering. However, this command should work roughly on any kind of data.

You can optionally repeat the NanoPlot command at this step to check you have filtered correctly.

```
filtlong --min_length 1000 --min_mean_q 75 lineName_pass.fastq.gz > lineName_filter.fastq.gz
```

# 4. Aligning Reads to Reference Genome

Before this step, add an extra contig representing your contruct to the end of the genome reference fasta file. This is `AgamP4_lineName.fasta` in the following command.

```
minimap2 -a -o lineName_AgamP4_align.sam AgamP4_lineName.fasta lineName_filter.fastq.gz
```

# 5. Sorting & Indexing the Alignment

This can be done directly inside IGV:
- *Tools*
- *Run igvtools...*
- Command: *Sort*
- Input File: *Browse*
- *Run*

This will create a `.sorted.sam` file in the same directory (you may delete the unsorted file to make space).

For indexing, in the same igvtools window:
- Command: *Index*
- Input File: *Browse* (choose the sorted file now)
- *Run*

# 6. Visualising in IGV

Load the genome reference with your contruct added on:
- *Genomes*
- *Load Genome from File*

Load your sorted alignment file:
- *File*
- *Load from File*

Go to the contig that represents your construct and click on reads that cover the end of the construct. If successful, these should reveal supplementary alignments in the genome which you can manually checkout!


---

Back to [Main Page](https://github.com/Tycour/crisanti-toolshed/blob/main/docs/index.md)