'''
A script to preprocess the genotype data file
design by.https://github.com/SausanCantik

Workflow
1. Load the data and identify the number of rows from each data
2. Screen missing genotype
3. Identify the markers
4. Identify the excesive samples form either data
5. Remove the excessive samples
6. Identify the sample plate code from the accession code
7. Delete the row of particular sample from the genotype data
'''

#libraries
import pandas as pd
import numpy as np

#Load the data and identify the number of rows from each data
#--------------------------------------------------------------

def loaddata():
    excel_path = input('Enter the file path : ')
    # read the .xlsx file
    dataframe = pd.read_excel(excel_path, sheet_name=0)
    return dataframe

#Screening missing genotype
#----------------------------------------------
def missing_treatment(genotype_dataframe) :
    
    #defining the genotype
    base = ['N']
    
    #listing all features
    features = list(genotype_dataframe)
    
    #missing treatment looping process
    for feature in features :
        
        #identify missing genotype
        genotype = genotype_dataframe[feature].unique()
        
        if base in genotype :
            #calculating missing genotype in a feature
            N_value = genotype_dataframe[feature].value_counts(normalize=True).get('N')
    
            #define the major genotype of each feature
            stats = genotype_dataframe[feature].describe()
            mode = stats['top']
        
            #setting threshold
            threshold = 0.2
    
            #missing genotype treatment
            if N_value > threshold :
                print('Dropping {}' .format(feature))
                genotype_dataframe.drop(columns=feature, inplace=True)
        
            else :
                print('Replacing missing genotype in feature {}' .format(feature))
                genotype_dataframe[feature].replace('N', mode, inplace=True)
                
        else :
            print('No missing genotype in {}' .format(feature))
                    
    return genotype_dataframe  

#Identifying the markers
#------------------------------------------------

def string_list(genotype_dataframe) :
    import pandas as pd
    
    #genotype_dataframe.drop(columns='Samples', inplace=True)
    columns = list(genotype_dataframe)
    genotype = []
    marker = {}
    for column in columns :
        marker[column] = genotype_dataframe[column].unique().tolist()
        genotype.extend(marker[column])
        
    #get the unique value
    genotype = pd.DataFrame(genotype)
    genotype = genotype[0].unique().tolist()
    return genotype

#Identify the excesive samples form either data
#-------------------------------------------------------

def sample_in_genotpe (genotype_dataframe) :
    sample_genotype = []
    for sample in genotype_dataframe['Samples']:
        name_split = sample.split('-', 5)
        sample_accession = name_split [5]
        sample_genotype.append(sample_accession)
        
    sample_genotype.sort()
    return sample_genotype

#Removing the excessive samples
#---------------------------------------------

def remove_samples(sample_to_remove) :
    length = len(sample_to_remove)
    for i in range(length) :
        sample = sample_to_remove[i]
        if sample in sample_genotype :
            #confirming the sample is in the list
            print('Before : is {} in the list ?    ' .format(sample), sample in sample_genotype) #shoud be true
        
            #removing the sample
            sample_genotype.remove(sample)
        
            #confirming the sample is removed
            print('After : is {} in the list ?    ' .format(sample), sample in sample_genotype, '\n') #should be false
        else :
            print('{} is no longer in the list' .format(sample))
        
    #confirming the Samples are now equal
    df = pd.DataFrame()
    df['Genotype'] = sample_genotype
    df['Phenotype'] = sample_phenotype
    print('Any NaN value anymore? ', df.isnull().any().any())
    
    return df

#Identify the sample plate code from the accession code
#--------------------------------------------------------

def split_combine (genotype_data) :
    #genotype_data = genotype_data.drop(labels=400, axis=0)
    label_genotype = list(genotype_data)
    sample_id = genotype_data[label_genotype[0]]
    ID = {}
    for sample in sample_id :
        name_split = sample.split('-', 5)
        sample = name_split[0] + '-' + name_split[1] + '-' + name_split[2] + '-' + name_split[3] + '-' + name_split[4]
        ID[name_split[5]] = sample 
        
    return ID

#List sample from genotype data given the accession code
#-------------------------------------------------------------

def sample_ID(genotype_dataframe) :
    to_remove = []
    ID = split_combine(genotype_dataframe)
    sample_to_remove = 'Ca09-6', 'Ca27-7', 'Ca32-6', 'Ca35-6', 'Ca36-6', 'Ca39-1', 'Ca45-7', 'Ca55-7', 'Ca58-7'
    for sample in sample_to_remove :
        hapus = ID[sample] + '-' + sample
        to_remove.append(hapus)
        
    return to_remove

#Delete the row of particular sample from the genotype data
#------------------------------------------------------------------

def delete_row(genotype_dataframe) :
    print ('Dimension Before: ', genotype_dataframe.shape )
    
    #gather the list of samples to remove
    to_remove = sample_ID(genotype_data)
    
    for sample in to_remove :
        genotype_dataframe = genotype_dataframe[genotype_dataframe.Samples != sample]
        
    print ('Dimension After: ', genotype_dataframe.shape )
    
    #write output
    file_output = genotype_dataframe.to_excel('genotype_after_treatment.xlsx')
    
    return file_output

#Running the program
print('LOADING DATA')
print('=======================================')
genotype_data = loaddata()
genotype_data.drop(genotype_data.index[400], inplace=True)
#genotype_data.drop(columns='Samples', inplace=True)
phenotype_data = loaddata()
print ('Genotype data loaded. Dimension : ' , genotype_data.shape)
genotype_data.tail(3)
print ('Phenotype data loaded. Dimension : ', phenotype_data.shape)
phenotype_data.head(3)

print('MISSING DATA TREATMENT')
print('=======================================')
genotype_dataframe = missing_treatment(genotype_data)

print('IDENTIFYIING SAMPLES ON BOTH DATA')
print('=======================================')
sample_genotype = sample_in_genotpe(genotype_dataframe)
sample_phenotype = phenotype_data['<Trait>']
df = pd.DataFrame()
df['Genotype'] = sample_genotype
df['Phenotype'] = sample_phenotype
df.loc[387:]

print('REMOVING EXCESSIVE SAMPLES')
print('=======================================')
sample_to_remove = 'Ca09-6', 'Ca27-7', 'Ca32-6', 'Ca35-6', 'Ca36-6', 'Ca39-1', 'Ca45-7', 'Ca55-7', 'Ca58-7'
df = remove_samples(sample_to_remove)
df.tail(10)
to_remove = sample_ID(genotype_data)
output1 = delete_row(genotype_data)
print('\n','You now have a file called : genotype_after_treatment.xlsx')
