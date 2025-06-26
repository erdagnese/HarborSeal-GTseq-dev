# optimization pipeline from WDFW for GTseq SNP panels

# Step 0: run bcl2fastq to demultiplex if not already done
nohup bcl2fastq --barcode-mismatches 0 --no-lane-splilstting --use-bases-mask y150,I6n,I6n --output-dir ../

# Step 0.25: Rename and archive .fq multiplex file; unzip .fq file; transfer BCsplit file to working directory.

#Step 0.5:  Demultiplex the fastq (.fq) file
	dmxc –bc BCsplit   .csv –lib    .fq

#Step 0.5.5: Concatenate all fastq files into a single .fq
	cat *.fastq > Concatenated.fastq

#GTs
#Step 1: generate a hash file with all unique sequences
./GTseq_HashSeqs.pl Concatenated.fastq > Concatenated.hash  #  takes a few minutes

#Step 2: This step searches for all forward and probe sequences to determine the on-target ratio. You will need an input file 
#(AssayInfo.txt). The input file is a tab delimited file with no header. Probe 1 and 2 are essentially 14 base pairs surrounding the SNP of interest. 
#You can have variations in all oligos e.g. [AT]. Create by grabbing the forward primer from the primer order sheet or the results file from batchprimer3. 
#Create the probe 1 and 2 sequences by using the panel.txt, batch_catalog.tags.tsv and batch_sumstats.tsv with concensusFastaFetch_forassayinfo.py. 
#Then use MID/RIGHT/LEFT formulas in excel to grab 7bp on either side of the SNP for both SNPs. If there are IUPAC codes in the probe sequences, 
#those need to be replaced with actual nucleotides. It is an overnight run. Step 3 below can be run concurrently. For both steps, 
#the output file sizes don’t update until the process is completely done. The first line of the tab-delimited input file might look something like this 
#(note that underline/bold SNPs are for clarity and are not part of text file):

# Sfo_1512_18455	CATATCCTGAGACGGAAACGAT	TGGAGAGGT[A/T][GT]TCT	TGGAGACGT[A/T][GT]TCT

#Command for Step 2
./GTseq_SeqTest.pl AssayInfo.txt  Concatenated.hash > PvGTseqRd1_seqtest.csv


#Step 3: This step searches for primer interactions i.e. looking for sequences with all combinations of forward and reverse 
#primers. It is an overnight run. Technically the script is looking for the complement of the reverse primer, but list the reverse 
#primers as is and not as their reverse complement. If a sequence is an on-target read, this script will not find the reverse 
#primer. To put it another way, the script only finds bad mis-priming reads. Create this file using the locus and forward
# sequence from AssayInfo.txt and grab the reverse sequence from the batchprimer3 output. The first line of the tab delimited 
#input.txt file might look something like this, where the first sequence is the forward primer and the second is the reverse 
#primer:

#	Sfo_6668_49060	AACCACTGTATAAGCAGGGTCA	GGAGCGATAATGAACTACAGTGA
	
#Command for Step 3
./GTseq_Primer-Interaction-Test.pl Pv_FWD_REV.txt Concatenated.hash > PvGTseq_Primer_interaction.txt

# Steps 4 and 5 happen outside of the terminal

# Perform part of the GT-Seq pipeline (demultiplex, callinGeno_v2.4.py, and then GTseq_SummaryFigures.py) with the second round panel 
# to extract genotypes, on-target reads, read depth etc. You will need to create a probeseq.csv file to run wrapper script. Use AssayInfo.txt file and original file used to generate whitelist for SNP nucleotides. The ProbeSeq.csv file should be ordered in this way without a header:
# Locus, SNP1, SNP2, Probe1, Probe2, ForwardPrimer, Correction1, Correction2
#Note: initially set all of the corrections to 0 and edit probseq.csv file for unix/linux end of line conversion

# Commands for Step 6 - first one WDFW lab did
# dmxc –bc BCsplit   .csv –lib    .fq
perl GTseq_Genotyper_v3.pl
python callinGeno_v2.4.py
python GTseq_SummaryFigures_v3.py

