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



#result analysis of model 2
df = pd.read_csv('result with huge community with location.csv')
df['true cluster'] = df['true cluster'].apply(lambda S:S.strip('cluster '))
df['true cluster'] = df['true cluster'].apply(int)
df['cluster result'] = df['cluster result'].apply(lambda S:S.strip('Cluster '))
df['cluster result'] = df['cluster result'].apply(int)
df['cluster result'] = df['cluster result'] + 1


#put results and truth into dict for cross comparison
cluster1 = dict()
cluster2 = dict()

for index, row in df.iterrows():
    if row['true cluster'] not in cluster1:
        cluster1[row['true cluster']] = []
    for key, value in cluster1.items():
        if key == row['true cluster']:
            value.append(row['user_id'])

for index, row in df.iterrows():
    if row['cluster result'] not in cluster2:
        cluster2[row['cluster result']] = []
    for key, value in cluster2.items():
        if key == row['cluster result']:
            value.append(row['user_id'])


#find the values that intersect regardless of cluster index
difference = dict()
for key, value in cluster2.items():
    for i in value:
        for k,v in cluster1.items():
            for j in v:
                if j == i:
                    if k not in difference:
                        difference[k] = set(value).intersection(v)


#calculate the percentage of correctly clustered users with weight assigned according to the
#number of users in each cluster
percent_difference=dict()
for key,value in difference.items():
    for k,v in cluster1.items():
        if key == k:
            percent_difference[k] = (len(value)/len(v))

weight=dict()
total_length=0
for key, value in cluster1.items():
    total_length += len(value)

for key, value in cluster1.items():
    weight[key] = len(value)/total_length

score=0
for key, value in percent_difference.items():
    for k, v in weight.items():
        if k == key:
            score += value * v

print (score)




#result analysis of model 4
df = pd.read_csv('result with huge community without location.csv')
df['true cluster'] = df['true cluster'].apply(lambda S:S.strip('cluster '))
df['true cluster'] = df['true cluster'].apply(int)
df['cluster result'] = df['cluster result'].apply(lambda S:S.strip('Cluster '))
df['cluster result'] = df['cluster result'].apply(int)
df['cluster result'] = df['cluster result'] + 1


#put results and truth into dict for cross comparison
cluster1 = dict()
cluster2 = dict()

for index, row in df.iterrows():
    if row['true cluster'] not in cluster1:
        cluster1[row['true cluster']] = []
    for key, value in cluster1.items():
        if key == row['true cluster']:
            value.append(row['user_id'])

for index, row in df.iterrows():
    if row['cluster result'] not in cluster2:
        cluster2[row['cluster result']] = []
    for key, value in cluster2.items():
        if key == row['cluster result']:
            value.append(row['user_id'])


#find the values that intersect regardless of cluster index
difference = dict()
for key, value in cluster2.items():
    for i in value:
        for k,v in cluster1.items():
            for j in v:
                if j == i:
                    if k not in difference:
                        difference[k] = set(value).intersection(v)


#calculate the percentage of correctly clustered users with weight assigned according to the
#number of users in each cluster
percent_difference=dict()
for key,value in difference.items():
    for k,v in cluster1.items():
        if key == k:
            percent_difference[k] = (len(value)/len(v))

weight=dict()
total_length=0
for key, value in cluster1.items():
    total_length += len(value)

for key, value in cluster1.items():
    weight[key] = len(value)/total_length

score=0
for key, value in percent_difference.items():
    for k, v in weight.items():
        if k == key:
            score += value * v

print (score)


#result analysis of model 6
df = pd.read_csv('result without huge community with location.csv')
df['true cluster'] = df['true cluster'].apply(lambda S:S.strip('cluster '))
df['true cluster'] = df['true cluster'].apply(int)
df['cluster result'] = df['cluster result'].apply(lambda S:S.strip('Cluster '))
df['cluster result'] = df['cluster result'].apply(int)
df['cluster result'] = df['cluster result'] + 1


#put results and truth into dict for cross comparison
cluster1 = dict()
cluster2 = dict()

for index, row in df.iterrows():
    if row['true cluster'] not in cluster1:
        cluster1[row['true cluster']] = []
    for key, value in cluster1.items():
        if key == row['true cluster']:
            value.append(row['user_id'])

for index, row in df.iterrows():
    if row['cluster result'] not in cluster2:
        cluster2[row['cluster result']] = []
    for key, value in cluster2.items():
        if key == row['cluster result']:
            value.append(row['user_id'])


#find the values that intersect regardless of cluster index
difference = dict()
for key, value in cluster2.items():
    for i in value:
        for k,v in cluster1.items():
            for j in v:
                count=0
                if j == i:
                    if k not in difference:
                        difference[k] = set(value).intersection(v)



#calculate the percentage of correctly clustered users with weight assigned according to the
#number of users in each cluster
percent_difference=dict()
for key,value in difference.items():
    for k,v in cluster1.items():
        if key == k:
            percent_difference[k] = (len(value)/len(v))

weight=dict()
total_length=0
for key, value in cluster1.items():
    total_length += len(value)

for key, value in cluster1.items():
    weight[key] = len(value)/total_length

score=0
for key, value in percent_difference.items():
    for k, v in weight.items():
        if k == key:
            score += value * v

print (score)


#result analysis of mode 8
df = pd.read_csv('result without huge community without location.csv')
df['true cluster'] = df['true cluster'].apply(lambda S:S.strip('cluster '))
df['true cluster'] = df['true cluster'].apply(int)
df['cluster result'] = df['cluster result'].apply(lambda S:S.strip('Cluster '))
df['cluster result'] = df['cluster result'].apply(int)
df['cluster result'] = df['cluster result'] + 1


#put results and truth into dict for cross comparison
cluster1 = dict()
cluster2 = dict()

for index, row in df.iterrows():
    if row['true cluster'] not in cluster1:
        cluster1[row['true cluster']] = []
    for key, value in cluster1.items():
        if key == row['true cluster']:
            value.append(row['user_id'])

for index, row in df.iterrows():
    if row['cluster result'] not in cluster2:
        cluster2[row['cluster result']] = []
    for key, value in cluster2.items():
        if key == row['cluster result']:
            value.append(row['user_id'])


#find the values that intersect regardless of cluster index
difference = dict()
for key, value in cluster2.items():
    for i in value:
        for k,v in cluster1.items():
            for j in v:
                count=0
                if j == i:
                    if k not in difference:
                        difference[k] = set(value).intersection(v)



#calculate the percentage of correctly clustered users with weight assigned according to the
#number of users in each cluster
percent_difference=dict()
for key,value in difference.items():
    for k,v in cluster1.items():
        if key == k:
            percent_difference[k] = (len(value)/len(v))

weight=dict()
total_length=0
for key, value in cluster1.items():
    total_length += len(value)

for key, value in cluster1.items():
    weight[key] = len(value)/total_length

score=0
for key, value in percent_difference.items():
    for k, v in weight.items():
        if k == key:
            score += value * v

print (score)
