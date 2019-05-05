import requests
from bs4 import BeautifulSoup
import csv

nameList = ['최형우', '손아섭', '나성범', '양의지', '최정', '김재환', '박민우', '서건창', '민병헌', '정근우', '김태균', '유한준', '박석민', '김하성', '강민호', '박용택', '오지환', '박건우', '이범호', '김주찬', '김재호', '나지완', '박경수', '오재일',  '박해민', '이재원', '김민성', '이용규', '오재원', '이택근', '최주환', '송광민', '정성훈', '김강민', '정훈', '허경민', '김성현', '손시헌', '이명기', '최준석', '박한이', '채태인', '채은성', '이종욱', '정의윤', '박정권', '모창민', '이성열', '노수광', '나주환', '고종욱', '박동원', '최진행', '이지영', '김문호', '서동욱', '김성욱', '정상호', '손주인', '임훈', '김용의', '지석훈', '김주형', '강경학', '문규현',  '하준호', '강한울', '이성우', '박기혁']

def GetData(name):
    req = requests.get("http://old.statiz.co.kr/stat.php?mid=stat&re=0&ys=2015&ye=2018&se=0&ty=0&qu=auto&po=0&pl="+name+"&da=2&o1=Year&o2=TPA")
    cont = req.content
    soup = BeautifulSoup(cont, "html.parser")

    data = soup.find_all("td", {"class": "statdata"})
    year = soup.find_all("td", {"class": "colhead_stz"})
    font = soup.find_all("font", {"class": ""})
    list = []


    for i in range(0, 4):
        thisYear = (int)(year[i].get_text())
        list.append(name)
        list.append(thisYear)
        for j in range(3, 6):
            k = j + i*21
            stat = (float)(data[k].get_text())
            list.append(stat)
        stat = (float)(data[i*21+7].get_text())
        list.append((stat))
        DataList.append(list)
        list = []
#YEAR  HR%   BB%   K%   IsoP
#연도 홈런%  볼넷%  삼진% 절대장타율(장타율-타율)


def GetData_first(name, index):
    req = requests.get("http://old.statiz.co.kr/stat.php?mid=stat&re=0&ys=2015&ye=2018&se=0&ty=0&qu=auto&po=0&pl="+name+"&da=1&o1=Year&o2=TPA")
    cont = req.content
    soup = BeautifulSoup(cont, "html.parser")
    list = []
    data = soup.find_all("td", {"class": "statdata"})

    for i in range(0, 4):
        stat = (float)(data[i * 29 + 3].get_text())
        DataList[(index - 1) * 4 + (i + 1)].append(stat)
        for k in range(6, 10):
            stat = (float)(data[i * 29 + k].get_text())
            DataList[(index - 1) * 4 + (i + 1)].append(stat)
        stat = (float)(data[i * 29 + 14].get_text())
        DataList[(index - 1) * 4 + (i + 1)].append(stat)
        stat = (float)(data[i * 29 + 17].get_text())
        DataList[(index - 1) * 4 + (i + 1)].append(stat)
        for k in range(21, 24):
            stat = (float)(data[i * 29 + k].get_text())
            DataList[(index - 1) * 4 + (i + 1)].append(stat)
        list = []
#타출장

def GetData_second(name, index):
    req = requests.get("http://old.statiz.co.kr/stat.php?mid=stat&re=0&ys=2015&ye=2018&se=0&ty=0&qu=auto&po=0&pl="+name+"&da=6&o1=Year&o2=TPA")
    cont = req.content
    soup = BeautifulSoup(cont, "html.parser")

    data = soup.find_all("td", {"class": "statdata"})


    for i in range(0, 4):
        k = 5 + i*23
        stat = (float)(data[k].get_text())
        DataList[(index-1) * 4 + (i + 1)].append(stat)
#FO/GO 뜬공아웃/땅볼아웃

def GetData_third(name, index):
    req = requests.get("http://old.statiz.co.kr/stat.php?mid=stat&re=0&ys=2015&ye=2018&se=0&ty=0&qu=auto&po=0&pl="+name+"&da=9&o1=Year&o2=TPA")
    cont = req.content
    soup = BeautifulSoup(cont, "html.parser")

    data = soup.find_all("td", {"class": "statdata"})


    for i in range(0, 4):
        k = 15 + i*21
        stat = (float)(data[k].get_text())
        DataList[(index-1) * 4 + (i + 1)].append(stat)
#XH/H - 장타/안타

def GetData_fourth(name, index):
    req = requests.get("http://old.statiz.co.kr/stat.php?mid=stat&re=0&ys=2015&ye=2018&se=0&ty=0&qu=auto&po=0&pl="+name+"&da=12&o1=Year&o2=TPA")
    cont = req.content
    soup = BeautifulSoup(cont, "html.parser")

    data = soup.find_all("td", {"class": "statdata"})


    for i in range(0, 4):
        k = 26 + i*29
        stat = (float)(data[k].get_text())
        DataList[(index-1) * 4 + (i + 1)].append(stat)
#RAA - 평균 대비 득점 생산(주루)




ballList = ['직구',	'슬라',	'커브',	'첸졉',	'스플',	'싱커',	'너클']

DataList = [[]]
BallValueList = [[]]
BallPerList = [[]]

for name in nameList:
    GetData(name)

index = 1
for name in nameList:
    GetData_first(name, index)
    index += 1

index = 1
for name in nameList:
    GetData_second(name, index)
    index += 1

index = 1
for name in nameList:
    GetData_third(name, index)
    index += 1

index = 1
for name in nameList:
    GetData_fourth(name, index)
    index += 1

    i = 0
titleList_1 = ['이름', '연도', '홈런%', '볼넷%', '삼진%', '절대장타율', '타석', '안타', '2루타', '3루타', '홈런', '볼넷', '삼진', '타율', '출루율', '장타율', '뜬공/땅볼', '장타/안타', 'RAA']
resultList = DataList + BallValueList + BallPerList
csvfile = open("test.csv", "wt", newline="")
csvheaderwriter = csv.DictWriter(csvfile, fieldnames=titleList_1)
csvheaderwriter.writeheader()
csvwriter = csv.writer(csvfile)
for row in resultList:
    csvwriter.writerow(row)
csvfile.close()
