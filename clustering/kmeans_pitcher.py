from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import csv

kmeans = KMeans(n_clusters=10, n_init = 2000)

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


kmeans.fit(df)
factor = kmeans.predict(df)

result = []
zxczx = np.bincount(factor)

for _ in range(0, len(zxczx)):
        result.append([])

for index in range(0, i):
        result[factor[index]].append(name[index])

maxLen = 0
for zcv in result:
        if maxLen < len(zcv):
                maxLen = len(zcv)
        print(zcv)
"""
f = open('./clusterOutput/classification_pitcher.csv', mode = 'wt', newline = '')
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
"""

