#import library
import json
import pandas as pd
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize

import fileinput
import os
import networkx as nx
import scipy as sp
import numpy as np
import csv

from sklearn.preprocessing import Imputer
from sklearn.base import TransformerMixin
from sklearn.utils import resample
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA


data = pd.read_csv('clustered_tweet.csv')


#fill missing numerical values with median and categorical values with mode
class DataFrameImputer(TransformerMixin):

    def __init__(self):
        """Impute missing values.

        Columns of dtype object are imputed with the most frequent value
        in column.

        Columns of other types are imputed with median of column.

        """

    def fit(self, X, y=None):
        self.fill = pd.Series([X[c].value_counts().index[0]
            if X[c].dtype == np.dtype('O') else X[c].median() for c in X],
            index=X.columns)
        return self

    def transform(self, X, y=None):
        return X.fillna(self.fill)

data = DataFrameImputer().fit_transform(data)
data_copy=data.copy()


#keep unique user into one file and calcuate mean of their followers and etc. counts
#incase they have changed during the 7 day peirod
unique_user_data = data.drop_duplicates(subset='user_id')

data = data_copy
data = data.drop(data.loc[:,'description':'verified'].columns, axis=1)
data = data.drop(data.loc[:,'time_zone':'cluster'].columns, axis=1)
data = data.groupby('user_id').mean().reset_index()
data = data.join(unique_user_data.set_index('user_id'), on='user_id',rsuffix='asd_')

unique_user_data=data
unique_user_data = unique_user_data.drop(unique_user_data.loc[:,'followers_countasd_':'statuses_countasd_'].columns, axis=1)

#open original dataset
data=data_copy

#define count location of tweets for each user
def user_by_region_per_artist(i):
    global data
    global unique_user_data
    filtered_data = data[data.place_name == i]
    filtered_places_per_user = filtered_data.groupby('user_id')['place_name'].size().reset_index(name='%s' % i)
    unique_user_data = unique_user_data.join(filtered_places_per_user.set_index('user_id'), on='user_id',rsuffix='asd_')

#apply function to each region code
region=[]
for i in data['place_name']:
    if i not in region:
        region.append(i)
for i in region:
    user_by_region_per_artist(i)


#fill empty cells with 0 for CPA analysis
unique_user_data = unique_user_data.fillna(0)
x = unique_user_data.loc[:,'Barking':'Frank Brightside & Sons']

#create more coloumns in dataframe to fill PCA values
count = 1
while count <= 32:
    unique_user_data['location_vector_%i' %count]=None
    count += 1

#PCA analysis by automatically setting dimension to the lowest that satisties a 0.95 condition
pca = PCA(n_components=0.95)
unique_user_data.loc[:,'location_vector_1':] = pca.fit_transform(x)
print ('explained variance ratio: %s' % pca.explained_variance_ratio_)

#remove location varibales
unique_user_data = unique_user_data.drop(unique_user_data.loc[:,'Barking':'Frank Brightside & Sons'].columns, axis=1)
del unique_user_data['place_name']

data = unique_user_data


# rescale data to range of 0 to 1
# because only passion score per artist and passion score of playlists are out of range,
# we therefore only need to normalize these two

scaler = MinMaxScaler()
data[['followers_count']] = scaler.fit_transform(data[['followers_count']])
data[['friends_count']] = scaler.fit_transform(data[['friends_count']])
data[['listed_count']] = scaler.fit_transform(data[['listed_count']])
data[['favourites_count']] = scaler.fit_transform(data[['favourites_count']])
data[['statuses_count']] = scaler.fit_transform(data[['statuses_count']])

#tranform dependent variable into categorical format
data['cluster'] = data['cluster'].apply(str)
data['cluster'] = "cluster " + data['cluster']


# keep only communities with at least 3 nodes
counts = data['cluster'].value_counts().to_dict()
list_of_cluster=[]
for key, value in counts.items():
    if value >= 3:
        list_of_cluster.append(key)

data = data.loc[data['cluster'].isin(list_of_cluster)]
counts = data['cluster'].value_counts().to_dict()


#genrate a dict of lists in the format: (network index : nodes list)
cluster_list=dict()
for index, row in data.iterrows():
    if row['cluster'] not in cluster_list.keys():
        cluster_list[row['cluster']] = []

for index, row in data.iterrows():
    for key, value in cluster_list.items():
        if row['cluster'] == key:
            value.append(row['user_id'])


# rename dict key and column entry for clarity
count = 1
while count <= len(counts):
    for key in cluster_list.keys():
        if type(key) == str:
            cluster_list[count] = cluster_list.pop(key)
            count+= 1

for key, value in cluster_list.items():
        for node in value:
            data.loc[(data['user_id'] == node),'cluster' ]=key


#tranform dependent variable into categorical format
data['cluster'] = data['cluster'].apply(str)
data['cluster'] = "cluster " + data['cluster']


#save to csv
data.to_csv('cleaned_tweet.csv')
