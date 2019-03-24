from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import csv

pca = PCA(n_components=2)

headerList = ['name','avg','base','slg','ops','wOBA','wRC+']
df = pd.DataFrame(columns=(headerList[1], headerList[2], headerList[3],headerList[4], headerList[5], headerList[6]))

f = open('../crollingPart/batter.csv', 'rt')
reader = csv.reader(f)
i = 0

for line in reader:
    if line[0] != 'name':
       # playerList.append({'name': line[0], 'avg': line[1], 'base': line[2], 'slg': line[3], 'ops': line[4], 'wOBA': line[5], 'wRC+': line[6]})
        df.loc[i] = [float(line[1]), float(line[2]), float(line[3]),float(line[4]), float(line[5]), float(line[6])]
        i = i + 1
f.close()

pca.fit(df)
factor = pca.transform(df)

print(df.shape)
print(factor.shape)
print(pca.components_)