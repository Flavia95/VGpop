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
```
git clone https://github.com/Flavia95/VGpop.git
cd VGpop
```
#### FUNCTIONS

##### 1. gfa2vcf 

Before run the script GfatoVcf.py, you need to:
1. Convert the GFA format to the ODGI format

By example:
```
odgi build -g samplePath3.gfa -o samplePath3.odgi
```
The odgi format as input to the script.

2. With -path specify the path of the odgi library and with -input specify the input file as odgi format
```
python GfatoVcf.py -path /../odgi/lib/ -input /../samplePath3.odgi
```

##### 2. bubblepop

##### 3. allele_freq
        arg1: matrix
        arg2: collections
        
##### 4. num_sequences
        arg1: matrix

##### 5. num_segregating_sites
        arg1: matrix

##### 6. count_differences
        arg1: matrix

##### 7. avg_num_pairwise_differences
        arg1: matrix

##### 8. tajimas_d
        arg1: num_sequences
        arg2: num_segregating_sites
        arg3: avg_num_pairwise_differences 

### Author

Flavia Villani

### License

MIT
