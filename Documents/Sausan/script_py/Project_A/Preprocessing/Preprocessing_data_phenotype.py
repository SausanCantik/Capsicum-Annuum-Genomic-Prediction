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
#%matplotlib inline

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

#Indentify Categorical and Numerical data
#----------------------------------------------

#A function to define whether the data in the column is numerical or categorial
def classifying_column(dataframe) :
    numeric = [] #list column name with numerical data
    categorial = [] #list column name with categorial data
    col_index = indexingcolumn(dataframe)
    
    for i in range (len(list(dataframe))) :
        if i == 0 :
            print ('Excluded column : ', col_index[i], '\n')
        else :
            entry = len(dataframe[col_index[i]].unique())
            if  entry > 5 :
                numeric.append(col_index[i])
            else :
                categorial.append(col_index[i])
    return numeric, categorial

#A function to show the list of trait with numerical data from dataframe
def numerical_trait(dataframe):
    numeric, categorial = classifying_column(dataframe)
    print('Traits with numerical data : ','\n',numeric, '\n')
    print('Total count : ' ,len(numeric) ,'Traits', '\n')
    
#A function to show the list of trait with categorial data
def categorial_trait(dataframe):
    numeric, categorial = classifying_column(dataframe)
    print('Traits with categorial data : ','\n',categorial, '\n')
    print('Total count : ' ,len(categorial) , 'Traits', '\n')
    
#A function to move from numeric to categorial, vice versa
def moving_numeric_categorial(numeric, categorial):
    '''
    In order to run this function, you need to specify these two parameter :
    
    numeric : list of traits with numerical data
    categorial : list of traits with categorial data
    
    if you want to use the column name from the raw data (the excel file), you may use
    this function :
    
    classifying_column(dataframe), which will return the parameters required for moving_numeric_categorial() 
    '''
    
    to_move = input('Which column name to move? : ') #takes only one name at a time
    null = ['none', 'NONE', 'None']
    
    if to_move in numeric :
        numeric.remove(to_move)
        categorial.append(to_move)
        print ('{} has been successfully removed from numeric to categorial' .format(to_move) )
        
        #check if is in categorial dataset
        print ('is {} still exist in numerical data list ? ' .format(to_move) , to_move in numeric)
        print ('is {} already in categorial data list ? ' .format(to_move) , to_move in categorial)
            
    elif to_move in categorial :
        categorial.remove(to_move)
        numeric.append(to_move)
        print ('{} has been successfully removed from categorial to numeric' .format(to_move) )
        
        #check if is in numerical dataset
        print ('is {} still exist in categorial data list ? ' .format(to_move) , to_move in categorial)
        print ('is {} already in numerical data list ? ' .format(to_move) , to_move in numeric)
        
    elif to_move in null :
        pass
    
    else :
        print ('Are you sure there is no typo ? The column name is not found in the dataset')
        
    return numeric, categorial

#Null Data Treatment Numeric
#----------------------------------

#Creating A function to group the sample based on the accession
#split the sample name based on '-' and store it into variable called 'accession_group'
def string_split (dataframe) :
    column_name = list(dataframe)
    sample_ID = column_name[0]
    accession_group = []
    for word in dataframe[sample_ID] : 
        split = word.split('-')
        accession_group.append(split[0])
        
    return accession_group

#A function to add accession_group as a column in phenotype data and encode the entries
def column_expansion (dataframe):       
    accession_group = string_split(dataframe)
    
    #encode the entries
    from sklearn import preprocessing #input encoder library
    
    le = preprocessing.LabelEncoder()
    accession_group = le.fit(accession_group).transform(accession_group)
           
    #Add column 'accession_group' to dataframe
    dataframe['Accession_group'] = accession_group
    
    return dataframe

# A function to calculate accession group means
def group_means(numeric, dataframe):
    
    #group the sample based on accession
    df = column_expansion (dataframe)
    
    #calculate column mean group by accession_group
    mean_values = {}
    
    for trait in numeric :
        group_mean = df.groupby('Accession_group')[trait].mean()
        mean_values[trait] = group_mean
        
    return mean_values

#Null Data Treatment Categorical
#----------------------------------

def fillna_categorial(categorial, dataframe):
    mode_value = []
    
    for i in range(len(categorial)):
        mode = int(dataframe[categorial[i]].mode())
        mode_value.append(mode)
        
    replacement = dict(zip(categorial, mode_value))
    dataframe = dataframe.fillna(value=replacement)
    
    return dataframe

#Creating crosstab
#------------------

def categorial_crosstab():
    #defining the trait with categorial data
    numeric, categorial = classifying_column(dataframe)
    
    #replacing NaN with mode value
    df = fillna_categorial(categorial, dataframe)
    
    #creating the containers for the dictionary
    trait = []
    category = []
    frequency = []
           
    for i in range(len(categorial)) :
        trait_i = categorial[i]
        frequency_i = list(df[trait_i].value_counts(sort = False))
        category_i = list(df[trait_i].unique())
    
        #Update the containers
        trait.append(trait_i)
        frequency.append(frequency_i)
        category.append(category_i)
        
    #create dictionary with trait as key and category and frequency as values
    d = {'Trait' : trait, 'Category' : category, 'Freq' : frequency}
    
    #create DataFrame from the dictionary
    crosstab = pd.DataFrame(d)
            
    return crosstab

# create a function to show bar chart based on categorial crosstab

def crosstab_barplot() :
    
    crosstab = categorial_crosstab()
    trait = input('Whict trait to show ? ')
    a = list(crosstab['Category'][crosstab['Trait']==trait])
    objects = a[0]
    y_pos = np.arange(len(objects))
    b = list(crosstab['Freq'][crosstab['Trait']==trait])
    performance = b[0]

    plt.bar(y_pos, performance, align='center')
    plt.xticks(y_pos, objects)
    plt.ylabel('Frequency')
    plt.xlabel('Category')
    plt.title('Frequency Distribution of trait {}' .format(trait))
    
    plt.savefig('{}.png' .format(trait))
    print('you now have a file called {}.png'.format(trait))
    result = plt.show()
    print (result)
    return result

#Running the program
#-----------------------
print('LOAD PHENOTYPE DATA')
print('=======================================')
dataframe = loaddata()

print('CHECKING NULL DATA')
print('=======================================')
nullstats(dataframe)

print('IDENTIFY CATEGORICAL AND NUMERICAL DATA')
print('=======================================')
numerical_trait(dataframe)
categorial_trait(dataframe)

print('MOVING TRAIT')
print('=======================================')
numeric, categorial = classifying_column(dataframe)
numeric, categorial = moving_numeric_categorial(numeric, categorial)
numeric, categorial = moving_numeric_categorial(numeric, categorial)

print('NULL DATA TREATMENT CATEGORICAL')
print('=======================================')
phenotype_data = fillna_categorial(categorial, dataframe)

print('WRITE OUTPUT TO .XLSX')
print('=======================================')
phenotype_data.to_excel("phenotype_after_treatment.xlsx")
print('you now have file called : phenotype_after_treatment.xlsx')
crosstab = categorial_crosstab()
crosstab.to_excel("crosstab_data_phenotype.xlsx")
print('you now have file called : crosstab_data_phenotype.xlsx')

print('WRITE OUTPUT TO .JPG')
print('=======================================')
result = crosstab_barplot()
