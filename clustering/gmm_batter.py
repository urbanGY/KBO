from sklearn import mixture
import pandas as pd
import numpy as np
import csv

gmm = mixture.GaussianMixture(n_components=4, covariance_type='full', n_init=2000)

headerList = ['이름', 'G', '타석', '타수', '득점', '안타','2타','3타','홈런','루타','타점','볼넷', '사구', '고4', '삼진']
df = pd.DataFrame(columns=(headerList[1], headerList[2], headerList[3], headerList[4], headerList[5], headerList[6], headerList[7], headerList[8], headerList[9], headerList[10], headerList[11], headerList[12], headerList[13], headerList[14]))

f = open('../crollingPart/batter.csv', 'rt')
reader = csv.reader(f)
i = 0
name = []

for line in reader:
    if len(line) > 0 and line[0] != '이름' and float(line[2]) >= 100:
        name.append(line[0])
        df.loc[i] = [float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6]), float(line[7]), float(line[8]), float(line[9]), float(line[10]), float(line[11]), float(line[12]), float(line[13]), float(line[14])]
        i = i + 1
f.close()

gmm.fit(df)
factor = gmm.predict(df)

print(np.bincount(factor))
result = []
zxczx = np.bincount(factor)

for _ in range(0, len(zxczx)):
        result.append([])

for index in range(0, i):
        result[factor[index]].append(name[index])

for zcv in result:
        print(zcv)