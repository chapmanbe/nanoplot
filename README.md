# nanoplot
Visualize variant data.

*Written by Tom Sasani for MDCRC 6521 at the University of Utah.*

## About

**nanoplot** is a very basic toolkit that allows users to create useful visualizations of VCF metadata in [bokeh](http://bokeh.pydata.org/en/latest/).

During the course of a rotation in Aaron Quinlan's lab, I performed a number of whole genome sequencing experiments
on a strain of *Vaccinia* virus. Once I obtained sequencing reads, I aligned them to the *Vaccinia* reference genome
and found mutations in my sample with a program called **Freebayes**. The full list of variants present in the virus samples I sequenced
is stored in a "variant call format," or **VCF**, file. Because the *Vaccinia* genome is relatively small (~190 kilobases), the
VCF files I produced only contained a few hundred to a thousand individual variants, including both single and multi-nucleotide
polymorphisms. As a way to visualize the data in these VCF files, I wrote **nanoplot**, a simple program that plots each variant
as a function of its quality score (the likelihood that the variant is "real," and not called in error). 

## Usage

To visually determine which variants in a VCF meet a quality score threshold, simply run:

`python nanoplot.py -v [VCF] -t [threshold] -vtype [variant type]`

The `-vtype` option should be followed by either 'COM' or 'SNP', depending on whether you want to visualize 
complex variants (i.e., multi-nucleotide polymorphisms) or SNPs.

## Dependencies

`nanoplot` requires Python 2.7. Additionally, it requires the following two libraries.

**bokeh** ____To install, run `conda install bokeh`.

**cyvcf2** ____To install, run `pip install cyvcf2`.


