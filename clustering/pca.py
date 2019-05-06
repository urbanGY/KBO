from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import csv

pca = PCA(n_components=5)

headerList = ['이름', '타율','BABIP','볼넷%','삼진%','볼/삼','ISO','타수/홈런', 'OPS', 'RC', 'RC/27', 'wRC', 'SPD', 'wSB', 'wOBA', 'wRAA']
df = pd.DataFrame(columns=(headerList[1], headerList[2], headerList[3],headerList[4], headerList[5], headerList[6], headerList[7], headerList[8], headerList[9], headerList[10],
                           headerList[11], headerList[12], headerList[13], headerList[14], headerList[15]))

f = open('../crollingPart/kbreportBatter.csv', 'rt')
reader = csv.reader(f)
i = 0


for line in reader:

        if line[0] != '이름':
                #playerList.append({'name': line[0], 'avg': line[1], 'base': line[2], 'slg': line[3], 'ops': line[4], 'wOBA': line[5], 'wRC+': line[6]})
                df.loc[i] = [float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6]), float(line[7]), float(line[8]), float(line[9]), float(line[10]), float(line[11]), float(line[12]), float(line[13]), float(line[14]), float(line[15])]
                i = i + 1
f.close()

pca.fit(df)
factor = pca.transform(df)

print(df.shape)
print(factor.shape)
print(pca.components_)