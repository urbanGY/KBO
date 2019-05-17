from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import csv

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

for k in range(5, 6):
        kmeans = KMeans(n_clusters=k, n_init = 2000)
        kmeans.fit(df)
        factor = kmeans.predict(df)

        result = []
        zxczx = np.bincount(factor)
        print(kmeans.inertia_)
        for _ in range(0, len(zxczx)):
                result.append([])

        for index in range(0, i):
                result[factor[index]].append(name[index])

        maxLen = 0
        for zcv in result:
                if maxLen < len(zcv):
                        maxLen = len(zcv)
                print(zcv)

f = open('./clusterOutput/classification_batter_2.csv', mode = 'wt', newline = '')
field = []
for i in range(0, len(result)):
        field.append(i)

csv_writer = csv.DictWriter(f, fieldnames=field)
csv_writer.writeheader()

for i in range(0, maxLen):
        tmp = {}
        for j in range(0, len(result)):
                if len(result[j]) <= i:
                        tmp[j] = '공백'
                else:
                        tmp[j] = result[j][i]
        csv_writer.writerow(tmp)

f.close()                


