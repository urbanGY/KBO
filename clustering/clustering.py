import csv
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

headerList = ['이름','타율','출루','장타','ops','wOBA','wRC+']
df = pd.DataFrame(columns=(headerList[0],headerList[1],headerList[2],headerList[3],headerList[4],headerList[5],headerList[6]))
team = ['기아타이거즈_타자.csv','넥센히어로즈_타자.csv','두산베어스_타자.csv','롯데자이언츠_타자.csv','삼성라이온즈_타자.csv','에스케이와이번스_타자.csv','엔씨다이노스_타자.csv','엘지트윈스_타자.csv','케이티위즈_타자.csv','한화이글스_타자.csv']

i = 0
for teamList in team:
    r = open('../crollingPart/batterOutput/'+teamList,mode='rt') #선수 명단의 맨 앞부분에 해당 팀명 들어가있어야함
    list = csv.DictReader(r)
    for line in list:
        df.loc[i] = [line[headerList[0]],line[headerList[1]],line[headerList[2]],line[headerList[3]],line[headerList[4]],line[headerList[5]],line[headerList[6]]]
        i += 1
    r.close()

data_points = df[[headerList[1],headerList[2],headerList[3],headerList[4],headerList[5],headerList[6]]].values
kmeans = KMeans(n_clusters=4).fit(data_points)
df['cluster'] = kmeans.labels_ #clustering complete
print(df)
print("df to csv complete!")


f = open('clusterOutput/classification.csv',mode='wt',newline='')
fieldnames = ['A','B','C','D']
csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
csv_writer.writeheader()

classList = [[],[],[],[]]
for index in range(0,i):
    if df.iloc[index][7] == 0:
        classList[0].append(df.iloc[index][0])
    if df.iloc[index][7] == 1:
        classList[1].append(df.iloc[index][0])
    if df.iloc[index][7] == 2:
        classList[2].append(df.iloc[index][0])
    if df.iloc[index][7] == 3:
        classList[3].append(df.iloc[index][0])

for index in range(0,max(len(classList[0]),len(classList[1]),len(classList[2]),len(classList[3]))):
    tmp = []
    if index >= len(classList[0]):
        tmp.append(' ')
    else:
        tmp.append(classList[0][index])

    if index >= len(classList[1]):
        tmp.append(' ')
    else:
        tmp.append(classList[1][index])

    if index >= len(classList[2]):
        tmp.append(' ')
    else:
        tmp.append(classList[2][index])

    if index >= len(classList[3]):
        tmp.append(' ')
    else:
        tmp.append(classList[3][index])
    csv_writer.writerow({'A':tmp[0],'B':tmp[1],'C':tmp[2],'D':tmp[3]})
f.close()
