from sklearn.cluster import DBSCAN
import csv
import pandas as pd
import numpy as np

headerList = ['이름', '홈런%', '볼넷%', '삼진%', '절대장타율', '타석','안타','2루타','3루타','홈런','볼넷','삼진', '타율', '출루율', '장타율', '뜬/땅', 'RAA']
df = pd.DataFrame(columns=(headerList[5], headerList[6], headerList[7], headerList[8], headerList[9], headerList[10], headerList[11]))

f = open('../crollingPart/test.csv', 'rt')
reader = csv.reader(f)
i = 0
name = []

for line in reader:
    if len(line) > 0 and line[0] != '이름':
        index = i
        for j in range(0, len(name)):
            if name[j] == line[0]:
                index = j

        if index == i :
            name.append(line[0])
            df.loc[i] = [float(line[6]), float(line[7]), float(line[8]), float(line[9]), float(line[10]), float(line[11]), float(line[12])]
            i = i + 1
        else:
            for j in range(6, 13):
                df.loc[index][j - 6] = df.loc[index][j - 6] + float(line[j])

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
        if (bMax == -1 or b < bMax) and len(bin) > 8 and sum > 5:
            bMax = b
            clusterMax = cluster
print(clusterMax)
bin = np.bincount(clusterMax + 1)
print(len(bin))
print(bin)

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