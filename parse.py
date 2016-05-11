from cyvcf2 import VCF
import argparse

"""
Now that you've plotted all of the variants in your VCF,
maybe you'd like to view the full VCF output for a given variant
(or variants) and take a closer look at its metadata.
"""

parser = argparse.ArgumentParser()

parser.add_argument("-v", "--vcf", help="Enter the path to the VCF file you analyzed with nanoplot.py.")
parser.add_argument("-p", "--positions", nargs='*', help="Enter the position (or range of positions) of the variant(s) from which you want to gather full VCF metadata.")
parser.add_argument("-o", "--outfile", help="Name the output VCF file.")  
args = parser.parse_args()

vcfFile = VCF(args.vcf)
user_pos = args.positions
title = args.outfile

out = open(title, "w")


# If the user provides a range of variant positions, find
# all variants at positions within that range.

if len(user_pos) == 2:
	lower = int(user_pos[0])
	upper = int(user_pos[1])

	for v in vcfFile:
		if v.POS >= lower and v.POS <= upper:
			v = str(v)
			out.write(v)

# If the user only wants to find a variant at a single position,
# grab that variant.

elif len(user_pos) == 1:
	for v in vcfFile:
		if v.POS == user_pos:
			v = str(v)
			out.write(v)
		else:
			break

# Since the above two code blocks cover the only two possible options
# available to the user, return an error message if the user provides
# anything else in the -p argument.

else:
	print "Sorry, -p must accept either a single position or a range between two positions."
