'''
A script to select optimum marker
design by: https://github.com/SausanCantik

Workflow
0. load data in excel format
1. encode the genotype
2. select the marker
3. write the output in excel file
'''

#libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest, chi2

#Load the data and identify the number of rows from each data
#--------------------------------------------------------------
def loaddata():
    excel_path = input('Enter the file path : ')
    # read the .xlsx file
    dataframe = pd.read_excel(excel_path, sheet_name=0)
    return dataframe

#Encoding the data
#--------------------------------------------------------------
def genotype_encoder(genotype_data) :
    genotype_data.drop(columns='Samples', axis = 1, inplace=True)
    encoded_genotype = genotype_data.apply(LabelEncoder().fit_transform)
    return encoded_genotype

#Features selection using chi2 independent test
#---------------------------------------------------------------
def marker_selection(encoded_genotype, phenotype_data):
    #loop for all traits
    selected_markers = {}
    phenotype_data = phenotype_data.drop(columns='<Trait>')
    phenotype_data = phenotype_data.drop(columns='Accession_group')
    traits = list(phenotype_data)
    for trait in traits :
        # Create features and target
        X = encoded_genotype
        y = phenotype_data[trait]

        # Select two features with highest chi-squared statistics
        chi2_selector = SelectKBest(chi2, k=10)
        chi2_selector.fit(X, y)

        # Look at scores returned from the selector for each feature
        chi2_scores = pd.DataFrame(list(zip(list(encoded_genotype), chi2_selector.pvalues_)), columns=['SNP', 'pval'])
        chi2_scores.sort_values('pval', ascending=True, inplace=True)
                
        #Features with the highest score
        kbest = np.asarray(list(encoded_genotype))[chi2_selector.get_support()]
        selected_markers[trait] = kbest
        
        #write the sheet as excel sheet
        with pd.ExcelWriter('Selected_marker.xlsx', engine="openpyxl", mode='a') as writer:
            chi2_scores.to_excel(writer, sheet_name='{}' .format(trait))
            
        #check point
        print(trait)

#Running program
#---------------------------------------------------------------
print('LOADING THE EXCEL FILES')
print('=======================================')
print('Enter the path for genotype data')
genotype_data = loaddata()
print ('Genotype data loaded. Dimension : ' , genotype_data.shape)
print('Enter the path for phenotype data')
phenotype_data = loaddata()
print ('Phenotype data loaded. Dimension : ' , phenotype_data.shape)
print('\n')

print('currently running : DATA ENCODING')
print('=======================================')
encoded_genotype = genotype_encoder(genotype_data)
print('\n')

print('currently runing : MARKER SELECTION')
print('=======================================')
df = {'Plant' : 'Capsicum annuum', 'Genotype' : '10 markers', 'Created by': 'Sausan Cantik|2019'}
pd.Series(df).to_excel('Selected_marker.xlsx')
marker_selection(encoded_genotype, phenotype_data)
print('you now have a file called: Selected_marker.xlsx ')
