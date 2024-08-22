# Gene-SeqID
This python script will take in a fasta formatted genome and a IWGC annotation file resulting in a new file containing gene IDs from the annotation file and sequences from the genome. 

## Detailed Description:

This script requires an annotation file in gff3 file format, and its corresponding genome as a fasta file. These files must contain identical chromosome designations (ie Chr00 in the annotation file and >Chr00 in the fasta file). Alterations to these designations, such as differences in capitalization or leading zeros, will not work in this program. I have coded the program to recognize these errors, as well as mistyping a file name and not overwriting a file that already exists. 

This python script will create a dictionary containing the chromosome designation as a key and the chromosome sequence as a value. This obviously takes a fair bit of memory, but it was the easiest way for me to get this to work. I’d like to optimize this in the future if I can. Once the dictionary is made it loops over the annotation file line by line, saves each field as a tuple, and prints the gene ID, chromosome, feature length, and gene sequence to the new file. 

I designed this script to work with reference genomes and annotation files for weedy species that were created by the [International Weeds Genomics Consortium (IWGC)](https://www.weedgenomics.org/), but it should work for all genome/annotation combos that fit the above description. 
