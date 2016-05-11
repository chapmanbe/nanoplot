# rotationTools
Visualize and store genomic data.

*Developed by Tom Sasani for MDCRC 6521 at the University of Utah.*

## About

**rotationTools** is a very basic toolkit that allows users to create useful visualizations of VCF metadata in [bokeh](http://bokeh.pydata.org/en/latest/), and extract relevant information from BED files.


## Usage

To visually determine which variants in a VCF meet a quality score threshold, simply run:

`python plot_qual.py [vcf] [threshold]`

## Dependencies

**bokeh** 

To install, run `conda install bokeh`.

**cyvcf2**

To install, run `pip install cyvcf2`.

