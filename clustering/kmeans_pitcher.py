from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import csv

headerList = ['이름', '출장', '완투', '완봉', '선발', '승','패','세','홀드','이닝','실점','자책', '타자', '안타', '홈런', '볼넷', '고4', '사구', '삼진', '보크', '폭투']
df = pd.DataFrame(columns=(headerList[1], headerList[2], headerList[3], headerList[4], headerList[5], headerList[6], headerList[7], headerList[8], headerList[9], headerList[10], headerList[11], headerList[12], headerList[13], headerList[14], headerList[15], headerList[16], headerList[17], headerList[18], headerList[19]))

f = open('../crollingPart/pitcher.csv', 'rt')
reader = csv.reader(f)
i = 0
name = []

for line in reader:
    if len(line) > 0 and line[0] != '이름' and float(line[9]) >= 31:
        name.append(line[0])
        df.loc[i] = [float(line[1]), float(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6]), float(line[7]), float(line[8]), float(line[9]), float(line[10]), float(line[11]), float(line[12]), float(line[13]), float(line[14]), float(line[15]), float(line[16]), float(line[17]), float(line[18]), float(line[19])]
        i = i + 1

f.close()

kmeans = KMeans(n_clusters=6, n_init = 2000)

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


