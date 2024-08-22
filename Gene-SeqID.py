"""
Author: John M. Lemas

Date: 25 Oct 2023

Title: Gene Sequence Identifier

Description:
This script will take in a .fasta and a .gff file, and output a file with the following
fields:

GeneID	Chromosome	Sequence	Notes
"""
from Bio import SeqIO# parse the input fasta
import os# double check files before overwriting one

def gff_search():# possible optimization option that needs further adjustment..

	fin = input('Enter the gff file: \n')

	try:
		fin_handle = open(fin)
	except:
		print('... Invalid annotation file. Please try again.\nExiting program..')
		exit()

	df = {'Chromosome':[], 'Start':[], 'End':[], 'Notes':[]}

	for line in fin_handle:
	
		Chromosome, Source, Type, Start, End, Score, Strand, Phase, Notes = line.rstrip().split('\t')
	
		df['Chromosome'].append(Chromosome)
		df['Start'].append(Start)
		df['End'].append(End)
		df['Notes'].append(Notes)

def fasta_search(fasta, Chr, s, e):# First method for creating a dictionary from the fasta file
	try:
		fasta_handle = open(fasta)
	except:
		exit()

	one_line = ''
	seq = ''

	for line in fasta_handle:
		one_line += line.replace('>', '').rstrip()

	print(one_line[:10000])
	fasta_handle.close()
	return one_line

def chrom_seqs(fasta):# much easier method for creating the fasta dictionary. Does take a lot of memory - needs optimization

#	fin_handle = input('Enter the fasta file: \n')

	try:# check for user error during input
		fin_handle = open(fasta)
	except:
		print(f'\t...Invalid file: {fasta}. Please try again.\n>>>Exiting Software.')
		exit()

#	df = {'Chr00':[], 'Chr01A':[], 'Chr01B':[], 'Chr02A':[], 'Chr02B':[],
#	'Chr03A':[], 'Chr03B':[], 'Chr04A':[], 'Chr04B': [], 'Chr05A':[], 'Chr05B':[],
#	'Chr06A':[], 'Chr06B':[], 'Chr07A':[], 'Chr07B':[], 'Chr08A':[], 'Chr08B':[],
#	'Chr09A':[], 'Chr09B':[]}#got it to work this way but its cumbersome and wont accept other chromosome designations

	df = {}# create the empty dictionary

	for chrom in SeqIO.parse(fin_handle, 'fasta'):# capture the chromosomes and sequences
		chrom_id = chrom.id
		seq = str(chrom.seq)

#		print(chrom_id)
#		print(seq[:20])

#		df[chrom_id] = df.get(chrom_id)# not working
		df[chrom_id] = seq# duh. keys dont exist yet. this is way easier.

	fin_handle.close()
#	print(df['Chr00'])
	return df

def main():

	gff = input('>>>Enter the gff file and press enter: \n')# accept the gff input file. maybe I can optimize this to recognize the right file extension?

	try:
		gff_handle = open(gff)
	except:
		print(f'\t... Invalid file: {gff}. Please try again.\n>>>Exiting program..')
		exit()
	
	fasta = input('>>>Enter the fasta file: \n')# accept the fasta input file. maybe I can optimize this to recognize the right file extension?

	print(f'\t... Fetching sequence information for each feature in {gff}.\n\t...this may take a while..')

	fasta_df = chrom_seqs(fasta)# capture the fasta dictionary

#	try:
#		fasta_handle = open(fasta)
#	except:
#		print('... Invalid fasta file. Please try again.\nExiting program..')
#		exit()

	fout = input('Process complete.\n>>>Enter the output file name: \n')# user defined output file

	print('>>>Checking for output file in current working directory..')

	dir_files = list(os.listdir())
	if fout in dir_files:
		user_ans = input(f'>>>Warning: {fout} already exists! Overwrite? y/[n]\n')
		if (user_ans == 'y') or (user_ans == 'Y'):
			fout_handle = open(fout, 'w')
		else:
			print(f'\t...{fout} not overwritten. Try again with another file name.\n>>>Exiting program..')
			exit()

	fout_handle = open(fout, 'w')

	fout_handle.write('\t'.join(['Gene ID', 'Chromosome', 'Feature Length', 'Sequence', '\n']))

	print('>>>Searching annotated features..')

#	gff_header = gff_handle.readline()

	for line in gff_handle:

		if '#' in line:
			continue

		Chromosome, Source, Type, Start, End, Score, Strand, Phase, Notes = line.rstrip().split('\t')

		if Chromosome not in fasta_df:
			print(f'>>>FATAL ERROR: Chromosome Designations in {gff} and {fasta} are not identical.\n\t...exiting program.')
			exit()

		ID = Notes.split(';')
		ID = ID[1]

		feat_len = int(End) - int(Start)

#		Sequence = fasta_search(fasta, Chromosome, Start, End)

		ref_seq = fasta_df[Chromosome]

		feature_seq = ref_seq[ (int(Start) - 1):(int(End) + 1) ]

#		print(type(feature_seq))

		fout_handle.write('\t'.join([ID, Chromosome, str(feat_len), feature_seq, '\n']))

	print(f'\t...process complete\n>>>Feature sequence information written to {fout}.\n>>>Exiting program.')

	gff_handle.close()
#	fasta_handle.close()
	fout_handle.close()

if __name__ == '__main__':
	main()
#	chrom_seqs('genome.fasta')
#	gff_search()
#	fasta_search('genome.fasta', 'Chr01A', '88881', '88929')