from sklearn.cluster import AgglomerativeClustering

import pandas as pd
import numpy as np
import csv
agg = AgglomerativeClustering(n_clusters=6)

headerList = ['이름', 'G', '타석', '타수', '득점', '안타','2타','3타','홈런','루타','타점','볼넷', '사구', '고4', '삼진', '타율', '출루', '장타', 'OPS']
df = pd.DataFrame(columns=(headerList[15:]))

f = open('../crollingPart/batter.csv', 'rt')
reader = csv.reader(f)
i = 0
name = []

for line in reader:
    if len(line) > 0 and line[0] != '이름' and float(line[2]) >= 150:
        name.append(line[0])
        tmp = []
        for j in range(15, len(line)):
            tmp.append(float(line[j]))
        df.loc[i] = tmp
        i = i + 1
f.close()


factor = agg.fit_predict(df)

print(np.bincount(factor))
result = []
zxczx = np.bincount(factor)

for _ in range(0, len(zxczx)):
        result.append([])

for index in range(0, i):
        result[factor[index]].append(name[index])

for zcv in result:
        print(zcv)