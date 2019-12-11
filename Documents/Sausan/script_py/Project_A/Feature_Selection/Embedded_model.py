'''
A script to select optimum model
design by: https://github.com/SausanCantik

Workflow
0. load data in excel format
1. encode the genotype
2. select the markers
3. embedded MNB model
4. write the output in excel file
'''

#libraries
#--------------------------------------------------------------
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from itertools import combinations
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from itertools import combinations
from sklearn.model_selection import cross_val_score

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

#Defining dataset
#--------------------------------------------------------------
def selecting_markers (traits, selected_markers_path):
    columns = {}
    k = int(input('How many markers to use?    '))
    m = k-1
    for trait in traits:
        dataframe = pd.read_excel(selected_markers_path, sheet_name=trait)
        snp = dataframe['SNP'].loc[:m]
        column = snp.tolist()
        columns[trait] = column
        
    return columns, m

#Embedded model
#--------------------------------------------------------------
def embedded_model(columns, m):
    for trait in traits :
        column = columns[trait]
        X = encoded_genotype[column]
        y = phenotype_data[trait]
        
        #Splitting the dataset into X_train, X_test, y_train, y_test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=13)
        
        #MNB Model
        selected_markers = []
        mnb_accuracy = []
        for i in range (m) :
            i = i+1
    
            #Check point i
            #print ('Iterasi dengan jumlah marker :  {}' .format(i), '\n')
    
            #create a combination of marker
            markers = list(combinations(column,i))
    
            #create a dictionary for marker and the model accuracy
            model_list = {}
    
            #for each combination, generate the Classifier, obtain the model accuracy
            for marker in markers:
                selected = list(marker)
                #marker_model['Marker'] = marker
                trainX = X_train[selected]
                testX = X_test[selected]
                        
                #build the svm model using training data
                model = MultinomialNB()       
                model.fit(trainX, y_train)

                #testing the model
                predictions = model.predict(testX)

                #model evaluation
                scores = cross_val_score(model, trainX, y_train, cv=5)
                #marker_model['SVC Accuracy'] = scores.mean()
                #marker_model['SVC std'] = scores.std()*2
                marker_accuracy = scores.mean()
                
                #store the marker evaluation score
                model_list[marker] = marker_accuracy
        
                #check point
                #print (model_list)
        
                #select the most accurate model
                optimum = max(list(model_list.values()))
        
                #for each combination class get the optimum combination based on max accuracy
                mark = list(model_list.keys())[list(model_list.values()).index(optimum)]
            selected_markers.append(mark)
            optimum = round(optimum, 2)
            mnb_accuracy.append(optimum)
    
        #final output
        df1 = pd.DataFrame(list(zip(selected_markers, mnb_accuracy)), columns = ['Markers', 'Accuracy'])
        
        #write the sheet as excel sheet
        with pd.ExcelWriter('Embedded_model.xlsx', engine="openpyxl", mode='a') as writer:
            df1.to_excel(writer, sheet_name='{}' .format(trait))

#Running program
#--------------------------------------------------------------
print('LOADING THE EXCEL FILES')
print('=======================================')
print('Enter the path for genotype data')
genotype_data = loaddata()
print ('Genotype data loaded. Dimension : ' , genotype_data.shape)
print('Enter the path for phenotype data')
phenotype_data = loaddata()
print ('Phenotype data loaded. Dimension : ' , phenotype_data.shape)
print('Enter the PATH of selected_marker.xlsx')
selected_markers_path = input()
print ('Selected markers data path loaded')
print('\n')

print('currently running : DATA ENCODING')
print('=======================================')
encoded_genotype = genotype_encoder(genotype_data)
print('\n')

print('SELECTING MARKERS')
print('=======================================')
phenotype_data = phenotype_data.drop(columns='<Trait>')
phenotype_data = phenotype_data.drop(columns='Accession_group')
traits = list(phenotype_data)
columns, m = selecting_markers (traits, selected_markers_path)

print('currently runing : EMBEDDED MODEL')
print('=======================================')
df = {'Plant' : 'Capsicum annuum', 'Genotype' : '3 markers', 'Created by': 'Sausan Cantik|2019'}
pd.Series(df).to_excel('Embedded_model.xlsx')
embedded_model(columns, m)
print('you now have a file called: Embedded_model.xlsx ')
