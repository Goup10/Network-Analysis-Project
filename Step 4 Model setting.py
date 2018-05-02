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


# divide dataset according to diffferent model settings

# 1. with huge community with location
#class balance target level: 50:50 for datasets containing huge community
#Upsample minority class
#Separate majority and minority classes
data = pd.read_csv('cleaned_tweet.csv')
data_majority = data[data.cluster == 'cluster 1']
data_minority = data[data.cluster != 'cluster 1']

#Upsample minority class
data_minority_upsampled = resample(data_minority,
                                 replace=True,     # sample with replacement
                                 n_samples=17421,    # 17421/17421=minority/majority=5/5
                                 random_state=123) # reproducible results

#Combine majority class with upsampled minority class
data_upsampled = pd.concat([data_majority, data_minority_upsampled])
del data_upsampled['Unnamed: 0']

#Display new class counts
print (data_upsampled.cluster.value_counts())
data_upsampled.to_csv('huge community with location.csv')


# 2. with huge community without location
data = pd.read_csv('huge community with location.csv')
data = data.loc[:,'user_id':'cluster']
data.to_csv('huge community without location.csv')


# 3. without huge community with location
data = pd.read_csv('cleaned_tweet.csv')
data = data[data['cluster'] != 'cluster 1']
data.to_csv('without huge community with location.csv')


# 4. without huage community without location
data = pd.read_csv('without huge community with location.csv')
data = data.loc[:,'user_id':'cluster']
data.to_csv('without huge community without location.csv')
