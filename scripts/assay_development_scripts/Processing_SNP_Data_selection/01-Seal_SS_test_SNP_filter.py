# Identifying SNPs in the VCF file of SS seal scats from Dietmar
# Variant calling has already been done to create the Variant call format (VCF) file
# they are the substrate for further analyses

# take a look at the file
from distutils.core import setup
from msvcrt import kbhit


less seal.vcf
# q to exit

# look at the header
grep "##FORMAT" seal.vcf

# check to filter SNPs and Indels
# no sure if this is already done or not on this data
# count the number of variants we have
grep -vc '#' seal.vcf
# 12063

# filter by quality 20 and count again
vcffilter -f  "QUAL >10" seal.vcf  | grep -vc '#'
# 3656

vcftools --vcf seal.vcf --max-missing 0.1 --mac 2 --minQ 15 --recode --recode-INFO-all --out raw.g2mac2
# so we called vcftools, gave it a vcf file, --max-missing 0.1 = keep only variants that have been successfully genotypes in 10% of individuals
# --mac 3 = minor allele count of 2; --minQ 15 = minimum quality score or 15 ; --record-INFO-all keeps all the info flags from the old vcf file in the new one
# and --out is the name of the output file
# this removed most of the data - 1274 sites of 12063

# filter for minimum depth for a gentype call
vcftools --vcf raw.g2mac2.recode.vcf --minDP 3 --recode --recode-INFO-all --out raw.g1mac2dp3 
# --minDP record genotypes that have less than 3 reads
# kept all 1274 - good

# filter out indivduals that didn't sequence well
vcftools --vcf raw.g1mac2dp3.recode.vcf --missing-indv

# this creates an output called out.imiss
cat out.imiss
# this kept them all - good
# highest missing is PV.26 with 76.8% missing

# visualize with a histogram
mawk '!/IN/' out.imiss | cut -f5 > totalmissing
gnuplot << \EOF 
set terminal dumb size 120, 30
set autoscale 
unset label
set title "Histogram of % missing data per individual"
set ylabel "Number of Occurrences"
set xlabel "% of missing data"
#set yr [0:100000]
binwidth=0.01
bin(x,width)=width*floor(x/width) + binwidth/2.0
plot 'totalmissing' using (bin($1,binwidth)):(1.0) smooth freq with boxes
pause -1
EOF

# most have individuals are missing less than 50% of data
# create list of indiv with more than 50% missing
mawk '$5 > 0.5' out.imiss | cut -f1 > lowDP.indv


# now with list, add that to the VCFtools filtering step
vcftools --vcf raw.g1mac2dp3.recode.vcf --remove lowDP.indv --recode --recode-INFO-all --out raw.g1mac2dplm

# so now that removed 3 individuals but kept all the sites

# now restrict the data to variants called in a high percentage of individuals and fiter by mean depth of genotypes
vcftools --vcf raw.g1mac2dplm.recode.vcf --max-missing 0.40 --maf 0.01 --recode --recode-INFO-all --out DP3g50maf01 --min-meanDP 15
# this applied a genotype rate across individuals (40%) - do this by population when there at muliple localities
# so we need a file to define localities (make one from metadata) tutorial has one made
cat popmap

# now create two lists that have that have just he individual names for each pop
mawk '$2 == "BR"' popmap > 1.keep && mawk '$2 == "WL"' popmap > 2.keep

# next use VCFtools to estimate missing data for loci in each pop
vcftools --vcf DP3g95maf05.recode.vcf --keep 1.keep --missing-site --out 1
vcftools --vcf DP3g95maf05.recode.vcf --keep 2.keep --missing-site --out 2 

# look at output
head -3 1.lmiss

# combine the two files and make a list of loci about the threshold of 10% missing data to remove
cat 1.lmiss 2.lmiss | mawk '!/CHR/' | mawk '$6 > 0.1' | cut -f1,2 >> badloci

# get back into VCFtools to remove any of the loci
vcftools --vcf DP3g95maf05.recode.vcf --exclude-positions badloci --recode --recode-INFO-all --out DP3g95p5maf05


# okay so we need to find a way to use the reference genome along with the VCF file to find primers
# try VCF-kit vk primers snip
pip install numpy
pip install VCF-kit
vk setup

