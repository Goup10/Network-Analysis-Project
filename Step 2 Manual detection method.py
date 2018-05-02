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


#read json formatted data into dict
data=[]
with open('tweet.txt') as json_data:
    for line in json_data:
        try:
            data.append(json.loads(line))
        except ValueError:
            pass


#Create sub graph based on both mentions and replies
G = nx.Graph()
for i in data:
    if i['user']['id'] != None:
        if i['in_reply_to_user_id'] != None:
            try:
                G.add_edge(i['user']['id'],
                i['in_reply_to_user_id'],
                text = i['text'],
                weight = 1)
            except IndexError:
                pass
        if i['entities']['user_mentions'] != []:
            try:
                G.add_edge(i['user']['id'],
                i['entities']['user_mentions'][0]['id'],
                text = i['text'],
                weight = 1)
            except IndexError:
                pass

#add dependent variable indicating different networks with 3 or more nodes
sub_graphs = [sg for sg in  nx.connected_component_subgraphs(G) if sg.number_of_nodes() >= 3]


#genrate a dict of lists in the format: (network index : nodes list)
cluster_list=dict()
for i, sg in enumerate(sub_graphs):
    cluster_list[i+1] = []
    for node in sg.nodes(data=True):
        for key,value in cluster_list.items():
            if key == i+1:
                value.append(node[0])


#for each node listed in the above dict, find the corresponding one in original data
#and add a new variable indicating its network group
#numerical value but categorocal in nature
def find_key(input_dict, number):
    for key, value in input_dict.items():
        for node in value:
            if node == number:
                return key

for i in data:
    i['cluster']=find_key(cluster_list, i['user']['id'])



#save selected features to csv for machine learning
#change empty list to empty cell for consistency
for i in data:
    if i['entities']['user_mentions'] == []:
        i['entities']['user_mentions'] = None

#write to csv
f = csv.writer(open("clustered_tweet.csv", "w"))

f.writerow(["user_id", "description", "user_name","verified",'followers_count',
            "friends_count", "listed_count", "favourites_count", "statuses_count",
            "time_zone", "lang", 'place_name','cluster'])

for i in data:
    if i['cluster'] != None:
        f.writerow([i['user']['id'],
                        i['user']['description'],
                        i['user']['name'],
                        i['user']['verified'],
                        i['user']['followers_count'],
                        i['user']['friends_count'],
                        i['user']['listed_count'],
                        i['user']['favourites_count'],
                        i['user']['statuses_count'],
                        i['user']['time_zone'],
                        i['user']['lang'],
                        i['place']['name'],
                        i['cluster'],
                       ])
