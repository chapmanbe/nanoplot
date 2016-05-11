#! ~/anaconda/bin/py27

from cyvcf2 import VCF
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import Span, HoverTool, PanTool
import sqlite3 as sqlite
import argparse
import sys

parser= argparse.ArgumentParser(description='A tool to plot variant quality.')

parser.add_argument("-v", "--vcf", help="Enter the path to the VCF file you want to analyze.")
parser.add_argument("-t", "--threshold", type=int, help="Enter the quality threshold you want to filter on.") 
parser.add_argument("-vtype", "--variant_type", type=str, help="Enter <SNP> if you are interested in plotting \
single nucleotide polymorphisms or <COM> if you are interested in plotting complex variants.")

args = parser.parse_args()

vcffile = args.vcf
thresh = args.threshold
vt = args.variant_type

# Create a SQLite database to store the data extracted from your VCF.
conn = sqlite.connect('nanoplot_data.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS nanodata
	 (position,
	  quality)""")

# Create empty lists, to be populated by the positions, quality scores, and lengths
# of variants that either pass (gx, gy, gsize) or fail (rx, ry, rsize). These will 
# ultimately be "sourced" as data frames in order to use the HoverTool.

gx = []
gy = []
rx = []
ry = []

gsize = []
rsize = []

# Create the nanoplot_input class.
class nanoplot_input(object):
	def __init__(self, vcffile, thresh):
		self._vcfname = str(vcffile)
		self._threshold = str(thresh)
class nanoplot_data(nanoplot_input):
	def __init__(self, vcffile, thresh):
		self._vcfname = str(vcffile)
	def get_info(self, vcffile, thresh):
		return self._vcfname, self._threshold	

	# Create a method to extract position and quality score info for SNPs in the 
	# provided VCF file, filtered by whether they meet the user-provided quality
	# threshold. As they're extracted, add these values to the SQL database 
	# created earlier.
	def get_snp_data(self, vcffile):
		
		for v in VCF(vcffile): 
			if (v.end - v.start) == 1:
				if v.QUAL > thresh:
					gx.append(float(v.POS) / 1000)
					gy.append(v.QUAL)
					gsize.append(15)
					c.execute("""INSERT INTO nanodata (position, quality) VALUES (?,?);""", (v.POS, v.QUAL))

				elif v.QUAL < thresh:
					rx.append(float(v.POS) / 1000)
					ry.append(v.QUAL)
					rsize.append(15)
					c.execute("""INSERT INTO nanodata (position, quality) VALUES (?,?);""", (v.POS, v.QUAL))

		conn.commit()

	# Now, create a method to extract the same information for complex variants.
	def get_com_data(self, vcffile):

		for v in VCF(vcffile):	
			if (v.end - v.start) > 1:
				if v.QUAL > thresh:
					gx.append(float(v.POS) / 1000)
					gy.append(v.QUAL)
					gsize.append((v.end-v.start)*2)
					c.execute("""INSERT INTO nanodata (position, quality) VALUES (?,?);""", (v.POS, v.QUAL))
				elif v.QUAL < thresh:
					rx.append(float(v.POS) / 1000)
					ry.append(v.QUAL)
					rsize.append((v.end-v.start)*2)
					c.execute("""INSERT INTO nanodata (position, quality) VALUES (?,?);""", (v.POS, v.QUAL))
	# Create the method to plot the previously extracted data with bokeh.
	def plot(self, thresh):

		# Source the lists defined earlier (which will contain values once one of the
		# above methods is called. This step is necessary for the functionality of the HoverTool created later.
		source1 = ColumnDataSource(data=dict(ggx=gx, ggy=gy))
		source2 = ColumnDataSource(data=dict(rrx=rx, rry=ry))
		source3 = ColumnDataSource(data=dict(ggsize=gsize, rrsize=rsize))
		
		# Name the bokeh output.
		output_file("quality.html")

		# Generate the dynamic bokeh figure, called 'p.'
		p = figure(plot_width=1000, plot_height=500) 
		p.title = "Quality-ranked Variants across Genomic Position"

		# Generate a 'threshold line' based on the user's quality score threshold.
		thresh_line = Span(location = thresh, dimension='width', line_color='blue', line_width=3)
		p.renderers.extend([thresh_line])

		# Add x and y axis labels.
		p.yaxis.axis_label = "Phred-scaled Quality Score"
		p.xaxis.axis_label = "Position (kilobases)"

		# Generate the hover function for each red and green circle that is plotted.
		r1 = p.circle(gx, gy, size=gsize, color='green', alpha=0.5, legend="Pass Variant", source=source1)
		r1_hover = HoverTool(renderers=[r1], tooltips=[('Position (kb)', '@ggx') , ('Quality', '@ggy')])
		p.add_tools(r1_hover)

		r2 = p.circle(rx, ry, size=gsize, color='red', alpha=0.5, legend="Fail Variant", source=source2)
		r2_hover = HoverTool(renderers=[r2], tooltips=[('Position (kb)', '@rrx') , ('Quality', '@rry')])
		p.add_tools(r2_hover)

		# Add a legend to the figure.
		p.legend.location = "top_left"
		show(p)

# Create an instance of the "nanoplot_data" class. 
instance = nanoplot_data(vcffile, thresh)

# If the user wants to see a plot of complex variant qualities, plot only
# complex variants.
if vt == 'COM':
	instance.get_com_data(vcffile)
	print instance.plot(thresh)	

# Or, if they want to plot SNPs only, plot SNPs.
elif vt == 'SNP':
	instance.get_snp_data(vcffile)	
	print instance.plot(thresh)
