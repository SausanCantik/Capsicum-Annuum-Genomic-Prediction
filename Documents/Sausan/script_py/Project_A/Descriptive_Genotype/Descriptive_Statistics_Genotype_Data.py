'''
A script to show descriptive statistics of genotype data
design by: https://github.com/SausanCantik

Workflow
0. Given the vcf file
1. Create a function to read vcf
2. Show allel distribution throughout chromosoms
3. Plot bases total count
'''

#library
import io
import os
import pandas as pd
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline

#A function to read VCF file

def read_vcf(path):
    with open(path, 'r') as f:
        lines = [l for l in f if not l.startswith('##')]
    return pd.read_csv(
        io.StringIO(''.join(lines)),
        dtype={'#CHROM': str, 'POS': int, 'ID': str, 'REF': str, 'ALT': str,
               'QUAL': str, 'FILTER': str, 'INFO': str},
        sep='\t'
    ).rename(columns={'#CHROM': 'CHROM'})

#A function to visualize the genotype total count

def plot_totalcount(df) :
    genotype_count = df['REF'].value_counts()
    objects = ['C','G','A','T']
    total_count = genotype_count[:4]

    #plotting
    plt.bar(objects, total_count, align='center')
    plt.ylabel('total_count')
    plt.xlabel('genotype')
    plt.title('genotype total count')

    plt.show()

#==============================================================================
#Running
path = input() #"C:/Users/Biotech/Documents/Sausan/IPYNB/Genotypes_targeted_Bowtie2-Genome_Freebayes-ploidy2-min-count-8_NGS1223_2018-12-24.vcf"
df = read_vcf(path)

#Show frequency of allel throughout chromosoms
counts = df.groupby('CHROM')['REF'].value_counts()
counts = counts.to_frame(name = 'Frequency')
counts.to_excel('Descriptive Statistics Genotype.xlsx')
print ('You now have a file called : Descriptive Statistics Genotype.xlsx ')

#plot total count
plot_totalcount(df)
