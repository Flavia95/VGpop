# VGpop

The aim is drive standard population genetic analyses using pangenomic data models.
Typically represented in the Graphical Fragment Assembly (GFA) format, these models can represent whole genome alignments in a compact graphical structure. 

**I have focused on algorithms for bubble detection that allow us to generate Variant Call Format (VCF) files from graphs**.

I use this projection to drive standard population genetic analyzes, and as a mechanism to validation results that I obtain from pangenome graph based population genetic analyzes which I am designing.

### Component Required

ODGI

- Building from *GitHub* [odgi](https://github.com/vgteam/odgi)

- Download from *Bioconda* [odgi](https://anaconda.org/bioconda/odgi)


### Download

Clone the source locally:
git clone https://github.com/Flavia95/VGpop.git
cd VGpop

#### 1. bubblepop

#### 2. gfa2vcf

Before run the script GfatoVcf.py, you need to:
1. Convert the GFA format to the ODGI format

By example:
odgi build -g samplePath3.gfa -o samplePath3.odgi

The odgi format as input to the script.
2. With -path specify the path of the odgi library and with -input specify the input file as odgi format

python GfatoVcf.py -path /../odgi/lib/ -input /../samplePath3.odgi

Description of the script:
DescriptionGfatoVcf.md

#### 3. gfa2tajima

arg1= spiegazione arg2= average number of pairwise differences (avePairDiff)

### Author

Flavia Villani

### License

MIT



