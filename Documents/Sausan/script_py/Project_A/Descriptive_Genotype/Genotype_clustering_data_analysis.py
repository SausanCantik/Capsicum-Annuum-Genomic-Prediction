'''
A script to cluster genotype data
design by: https://github.com/SausanCantik

Workflow
0. given the excel file
1. list the bases
2. encode the data
3. determine the number of clusters
4. perform kmeans clustering
5. save the output in excel format
'''

#libraries
import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
#%config InlineBackend.figure_format='retina'

#a function to list all the genotype
def string_list(df):
    base = []
    for j in range(1493):
        j= j+1
        for i in range(400):
            entity = df.loc[i].iloc[j]
            if entity not in base :
                base.append(entity)
    return base

#a function to encode the data
def encoding(df):
    base = string_list(df)
    le = preprocessing.LabelEncoder()
    le.fit(base)
    list(le.classes_)

    #Encode the whole SNPs in 400 samples
    data_encoded = []
    for i in range(1493):
        i=i+1
        encoded = le.transform(df.iloc[:,i])
        data_encoded.append(encoded)
    return data_encoded

#a function for determining the number of cluster
def defining_cluster_number(df):
    data_encoded = encoding(df)
    
    #creating dataframe from the encoding data
    matrix = pd.DataFrame(data_encoded, columns=df.iloc[:,0])

    #transpose the matrix to get table size of 400 x 1493
    data = matrix.transpose()
    data.head()
    
    # Standardize the data to have a mean of ~0 and a variance of 1
    X_std = StandardScaler().fit_transform(data)

    # Create a PCA instance: pca
    pca = PCA(n_components=20)
    principalComponents = pca.fit_transform(X_std)

    # Save components to a DataFrame
    PCA_components = pd.DataFrame(principalComponents)
    
    #determining the number of k
    ks = range(1, 10)
    inertias = []
    for k in ks:
        # Create a KMeans instance with k clusters: model
        model = KMeans(n_clusters=k)
    
        # Fit model to samples
        model.fit(PCA_components.iloc[:,:3])
    
        # Append the inertia to the list of inertias
        inertias.append(model.inertia_)
    
    plt.plot(ks, inertias, '-o', color='black')
    plt.xlabel('number of clusters, k')
    plt.ylabel('inertia')
    plt.xticks(ks)
    plt.show()
    
    return PCA_components 
    
#a function to perform kmeans clustering
def kmeans_clustering(k, PCA_components):  
    # Creating a new dataframe from PC[0] and PC[1]
    data_pca = pd.DataFrame({'PC 1': PCA_components[0], 'PC 2': PCA_components[1]})

    #training using kmeans
    model = KMeans(n_clusters = k)
    kmeans = model.fit(np.array(data_pca))
    clust_labels = model.predict(data_pca)
    center = model.cluster_centers_
    kmeans = pd.DataFrame(clust_labels)
    data_pca.insert((data_pca.shape[1]),'kmeans',kmeans)
    
    #Plot the clusters obtained using k means
    fig = plt.figure()
    ax = fig.add_subplot(111)
    scatter = ax.scatter(data_pca['PC 1'], data_pca['PC 2'], c=kmeans[0],s=150)
    ax.set_title('K-Means Clustering')
    ax.set_xlabel('PC 1')
    ax.set_ylabel('PC 2')
    plt.colorbar(scatter)
    plt.show()
    
    return data_pca

# running

print ('Insert the path to genotype data in excel format :')
path = input()
data_excel = pd.read_excel(path)
df = data_excel.drop(axis = 0, index=400)
PCA_components = defining_cluster_number(df)
k = int(input('Enter the number of clusters:  '))
data_pca = kmeans_clustering(k, PCA_components)

#saving the output
data_pca['Sample ID'] = df.iloc[:,0]
data_pca.to_excel('clustering_genotype_1.xlsx')
print ('you now have a file called: clustering genotype_1.xlsx')
