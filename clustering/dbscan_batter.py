from sklearn.cluster import DBSCAN
import csv
import pandas as pd
import numpy as np

headerList = ['이름', 'G', '타석', '타수', '득점', '안타','2타','3타','홈런','루타','타점','볼넷', '사구', '고4', '삼진', '타율', '출루', '장타', 'OPS']
df = pd.DataFrame(columns=(headerList[1:]))

f = open('../crollingPart/batter.csv', 'rt')
reader = csv.reader(f)
i = 0
name = []

for line in reader:
    if len(line) > 0 and line[0] != '이름' and float(line[2]) >= 150:
        name.append(line[0])
        tmp = []
        for j in range(1, len(line)):
            tmp.append(float(line[j]))
        df.loc[i] = tmp
        i = i + 1
f.close()

bMax = -1
clusterMax = -1

for min_samples in range(1, 200):
    for eps in range(1, 200):
        
        cluster = DBSCAN(min_samples=min_samples, eps=eps).fit_predict(df)
        bin = np.bincount(cluster + 1)
        sum = 0
        for s in bin:
            sum += s
        sum = sum / len(bin)
        b = 0
        for s in bin:
            b += abs(sum - s)
        if (bMax == -1 or b < bMax) and len(bin) > 3 and sum > 5:
            bMax = b
            clusterMax = cluster
        
print(clusterMax)
bin = np.bincount(clusterMax + 1)
print(len(bin))
#print(bin)

ss = []
tt = []
for _ in range(0, len(bin)):
    ss.append([])

for index in range(0, i):
    if clusterMax[index] == -1:
        tt.append(name[index])
    else:
        ss[clusterMax[index]].append(name[index])
#    print(clusterMax[index], name[index])

#print(tt)
for qq in ss:
    print(qq)