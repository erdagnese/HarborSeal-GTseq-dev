#!/usr/bin/env python
# callinGeno_v1.0.py, 170216, ninh - is a wrapper program running GTseq_Genotyper_v3.pl in multiprocess mode and scoring sex and/or hybrid markers
# callinGeno_v2.0.py, 170511 - simplify and make robust panel selection and compatibility with other labs
# callinGeno_v2.1.py, 170809 - move typing function to salmonBioInfo and reorganize probeSeq files
# callinGeno_v2.2.py, 180212 - streamline multiprocessing
# callinGeno_v2.3.py, 190221 - Tom - allow use of as many threads as machine has
# callinGeno_v2.4.py, 190221 - Tom - changed multiproccessing to use thread pool and to use multiple threads to call sex markers
# in terminal $ callinGeno_v2.4.py<enter>

import sys, os, glob, math, time, colorama, re
import multiprocessing as mp
from subprocess import call

def genotype(file, probe_file):
	genos = re.sub('\.fastq$', '.genos', file)
	genos = re.sub('^initial', '', genos)
	call('GTseq_Genotyper_v3.pl ' + probe_file + ' ' + file + ' > ' + genos, shell=True)
	
	
def Main():
	start = time.time()
	# determine panel to use for scoring
	##### this is the path of the directory with all the probeseq files in it
	probeSeqDirPath = '/genstorage2/GTseq/support_files/markerList_inputs/'
	##### organization: ['panel_abbreviation', 'panel name', 'probeseq_file_name.csv']
	probeSeqDict = {1: ['PanelName', 'Species', 'ProbeFileName.csv']}
	
	print('\nPanels available for scoring GTseq data.\n')
	for p, shortName in sorted(probeSeqDict.items()):
		print(str(p) + ' ' + shortName[0] + '  ' + shortName[1])
	print('')
	pSeq = input('Choose a number corresponding to the panel you want to score: ')
	try:
		probeSeqFile = probeSeqDict.get(int(pSeq))
		probeFile = probeSeqDirPath + probeSeqFile[2]
	except:
		print('\nYou must enter a number. Try running callinG again.\n\n')
		sys.exit()
	
	fqFileL = []
	for file in sorted(glob.glob('*.fastq')): fqFileL.append(file)

	# multiprocess calling genotype of subsets of fastqs - use all threads
	threads = mp.cpu_count()	#get number of threads

	print('Now genotyping ', str(len(fqFileL)), ' samples using ', str(threads), ' thread(s).')

	process_pool = mp.Pool(processes = threads)
	for fastq_file in fqFileL:
		process_pool.apply_async(genotype, args = (fastq_file, probeFile))
	process_pool.close()	#close the pool to new tasks
	process_pool.join()		#join the processes
	
	
	hours, rem = divmod(time.time()-start, 3600)
	minutes, seconds = divmod(rem, 60)
	print("\nTotal run time {:0>2}:{:0>2}:{:05.2f}\n\n".format(int(hours),int(minutes),seconds))

Main()
