import requests
from bs4 import BeautifulSoup
import csv

DataList=[[]]
nameList = ['양현종', '해커', '니퍼트', '소사', '윤성환', '장원준', '유희관', '우규민', '차우찬', '손승락', '이재학', '임창민', '함덕주', '심창민', '임창용', '백정현', '김진성', '윤규진', '송승준', '임정우', '이현승', '김세현', '신재웅', '권혁', '김승회', '윤길현', '윤희상', '이민호', '박희수', '김강률', '이동현', '장시환', '안영명', '전유수', '박정배', '채병용', '정찬헌', '송은범', '금민철', '윤지웅', '권오준', '홍성용', '배장호', '임준혁', '장원삼', '노경은', '오주원', '이상화', '최금강', '진해수', '하영민', '유원상', '심동섭', '한승혁', '김사율', '이동걸', '최동환', '심수창', '박근홍', '송창식', '윤근영', '임현준', '민성기', '고효준', '이명우', '정재원']
def GetData(name):
    req = requests.get("http://old.statiz.co.kr/stat.php?mid=stat&re=1&ys=2015&ye=2018&se=0&ty=0&qu=auto&po=0&pl="+name+"&da=1&o1=Year&o2=OutCount&de=0&lr=0&ml=1&sn=30")
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
        for k in range(13, 18):
            stat = (data[i * 30 + k].get_text())
            list.append((stat))

        stat = (data[i*30+24].get_text())
        list.append((stat))
        DataList.append(list)
        list = []

def GetData_first(name, index):
    req = requests.get("http://old.statiz.co.kr/stat.php?mid=stat&re=1&ys=2015&ye=2018&se=0&ty=0&qu=auto&po=0&pl="+name+"&da=2&o1=Year&o2=OutCount&de=0&lr=0&ml=1&sn=30")
    cont = req.content
    soup = BeautifulSoup(cont, "html.parser")
    list = []
    data = soup.find_all("td", {"class": "statdata"})

    for i in range(0, 4):
        for k in range(5, 7):
            stat = (float)(data[i * 27 + k].get_text())
            DataList[(index - 1) * 4 + (i + 1)].append(stat)
        for k in range(9, 11):
            stat = (float)(data[i * 27 + k].get_text())
            DataList[(index - 1) * 4 + (i + 1)].append(stat)
        stat = (float)(data[i * 27 + 12].get_text())
        DataList[(index - 1) * 4 + (i + 1)].append(stat)
        stat = (float)(data[i * 27 + 15].get_text())
        DataList[(index - 1) * 4 + (i + 1)].append(stat)
        stat = (float)(data[i * 27 + 17].get_text())
        DataList[(index - 1) * 4 + (i + 1)].append(stat)
        stat = (float)(data[i * 27 + 22].get_text())
        DataList[(index - 1) * 4 + (i + 1)].append(stat)
        stat = (float)(data[i * 27 + 25].get_text())
        DataList[(index - 1) * 4 + (i + 1)].append(stat)
        list = []

def GetData_Second(name, index):
    req = requests.get("http://old.statiz.co.kr/stat.php?mid=stat&re=1&ys=2015&ye=2018&se=0&ty=0&qu=auto&po=0&pl="+name+"&da=7&o1=Year&o2=OutCount&de=0&lr=0&ml=1&sn=30")
    cont = req.content
    soup = BeautifulSoup(cont, "html.parser")
    list = []
    data = soup.find_all("td", {"class": "statdata"})

    for i in range(0, 4):
        stat = (float)(data[i * 23 + 5].get_text())
        DataList[(index - 1) * 4 + (i + 1)].append(stat)

        list = []



for name in nameList:
    GetData(name)

index = 1
for name in nameList:
    GetData_first(name, index)
    index += 1

index = 1
for name in nameList:
    GetData_Second(name, index)
    index += 1

titleList_1 = ['이름', '연도', '피안타', '피2루타', '피3루타', '피홈런', 'FIP', 'K/9', 'BB/9', '삼진율', '사구율', 'PFR', '피안타율', '피장타율','경기당이닝수', 'P/PA', '뜬공/땅볼', '장타/안타']
resultList = DataList;

csvfile = open("PitcherData.csv", "wt", newline="")
csvheaderwriter = csv.DictWriter(csvfile, fieldnames=titleList_1)
csvheaderwriter.writeheader()
csvwriter = csv.writer(csvfile)
for row in resultList:
    csvwriter.writerow(row)
csvfile.close()

