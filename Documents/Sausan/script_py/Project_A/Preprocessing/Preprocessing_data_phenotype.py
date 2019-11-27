'''
A script to preprocess the phenotype data file
design by.https://github.com/SausanCantik
'''

'''
1. Checking Null Data
    * Creating a function to load excel the data
    * Creating dictionary that contain index and assosiated column
    * Creating a function to get all the index in which the column contain null
    * Defining a function which return data dimension, is there any column with null data and if yes, how many
    
2. Indentify Categorical and Numerical data
    *Creating a function to define whether the data in the column is numerical or categorial
    *Creating a function to show the list of trait with numerical data from dataframe
    *Creating a function to show the list of trait with categorial data
    *Creating a function to move from numeric to categorial, vice versa
    
3. Null Data Treatment Numeric
    * Creating A function to group the sample based on the accession
    * Split the sample name based on '-' and store it into variable called 'accession_group'
    * Creating a function to add accession_group as a column in phenotype data and encode the entries
    * Creating a function to calculate accession group means
    
4. Null Data Treatment Categorical
    *Creating a function to replace missing value with mode
    
5. Creating Crosstab

6. Create a function to show bar chart based on categorial crosstab

'''

# libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
%matplotlib inline

#Checking Null Data
#---------------------------------------

# Creating a function to load excel the data
def loaddata():
    excel_path = input('Enter the file path : ')
    # read the .xlsx file
    dataframe = pd.read_excel(excel_path, sheet_name=0)
    return dataframe

# Creating dictionary that contain index and assosiated column
def indexingcolumn(dataframe) :
    cols = list(dataframe)
    key = [] #index
    value = [] #column name
    for i in range (len(cols)):
        key.append(i)
        value.append(cols[i])
    
    col_index = dict(zip(key, value))
    return col_index

# A function to get all the index in which the column contain null
def null_column(dataframe):
    null = list(dataframe.isnull().any())
    index = []
    null_name = []
    for i in range(len(null)):
        if null[i] == True :
            index.append(i)
            col_index = indexingcolumn(dataframe)
            null_name.append(col_index[i])
    length = len(null_name)
    return null_name, length

# Defining a function which return data dimension, is there any column with null data and if yes, how many
def nullstats(dataframe) :
    #dataframe = loaddata(excel_path)
    print ('Data dimension : ', dataframe.shape)
    print ( 'Is there any column with null data ? ', dataframe.isnull().any().any())
    null_name, length = null_column(dataframe)
    print ( 'How many colum with null data ?', length)
