import requests
from bs4 import BeautifulSoup
import csv

def GetData(batter, birth, pitcher):
    i = 0
    req = requests.get("http://www.statiz.co.kr/player.php?opt=5&sopt=0&name="+batter+"&birth="+birth+"&re=0&da=0&year=1000")
    cont = req.content
    soup = BeautifulSoup(cont, "html.parser")

    td = soup.find_all("td", {"style": "white-space:nowrap;text-align:center;vertical-align:middle;"})
    data = soup.find_all("td", {"class": "statdata"})
    stat = (float)(data[18].get_text())
    max = int(len(td))

    for i in range(0, max):
        if td[i].get_text() == pitcher:
            PA = (int)(data[(i) * 24 + 0].get_text())
            PA = str(PA)
            AB = (int)(data[(i) * 24 + 1].get_text())
            AB = str(AB)
            Hit = (int)(data[(i) * 24 + 3].get_text())
            Hit = str(Hit)
            HR = (int)(data[(i) * 24 + 6].get_text())
            HR = str(HR)
            BB = (int)(data[(i) * 24 + 11].get_text()) + (int)(data[(i) * 24 + 12].get_text()) + (int)(data[(i) * 24 + 13].get_text())
            BB = str(BB)
            avg = (float)(data[(i) * 24 + 18].get_text())
            #print(batter+"의 "+pitcher+" 상대 통산 전적은 "+PA+"타석 "+AB+"타수 "+Hit+"안타 "+BB+"사사구 "+HR+"홈런입니다.")
            print(batter+"의 "+pitcher+" 상대 통산 타율은 "+str(avg)+" 입니다.")
    return avg
