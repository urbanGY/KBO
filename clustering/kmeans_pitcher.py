from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import csv

headerList = ['이름', '출장', '완투', '완봉', '선발', '승','패','세','홀드','이닝','실점','자책', '타자', '안타', '홈런', '볼넷', '고4', '사구', '삼진', '보크', '폭투', 'WHIP', 'ERA+', 'FIP+']
df = pd.DataFrame(columns=(headerList[21:]))

f = open('../crollingPart/pitcher.csv', 'rt')
reader = csv.reader(f)
i = 0
name = []

for line in reader:
    if len(line) > 0 and line[0] != '이름' and float(line[9]) >= 31:
        name.append(line[0])
        tmp = []
        for j in range(21, len(line)):
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

f = open('./clusterOutput/classification_pitcher_2.csv', mode = 'wt', newline = '')
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


