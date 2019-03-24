from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import csv

headerList = ['name','avg','base','slg','ops','wOBA','wRC+']
playerList = []
df = pd.DataFrame(columns=(headerList[3],headerList[4]))

kmeans = KMeans(n_clusters=2)
f = open('../crollingPart/batter.csv', 'rt')
reader = csv.reader(f)
i = 0

for line in reader:
    if line[0] != 'name':
        playerList.append({'name': line[0], 'avg': line[1], 'base': line[2], 'slg': line[3], 'ops': line[4], 'wOBA': line[5], 'wRC+': line[6]})
        df.loc[i] = [float(line[3]),float(line[4])]
        i = i + 1
f.close()

kmeans.fit(df.values)
print(kmeans.labels_)
group1 = []
group2 = []

for index in range(0, i):
    if kmeans.labels_[index] == 0:
        group1.append(playerList[index]['name'])
    else :
        group2.append(playerList[index]['name'])

print(group1)
print(group2)

