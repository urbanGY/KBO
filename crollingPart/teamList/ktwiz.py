import csv
from bs4 import BeautifulSoup
import requests

def get_pitcherData(url):
    r = {'name': [], 'birth': []}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'tab_sty_02'}).find_all('tr')
    for tr in table:
        tdlist = tr.find_all('td')
        index = 0
        flag = False
        name = ""
        birth = ""
        for td in tdlist:
            string = str(td).split("<td>")
            
            if index == 1:
                name = str(td).split(">")[3].split("</p")[0].strip()
            elif index == 4:
                birth = str(td).split("<td>")[1].split("</td>")[0].strip()
            elif len(string) > 1 and index == 2:
                if str(td).split("<td>")[1].split("</td>")[0].strip() != "투수":
                    flag = True
                    break
            index = index + 1
        
        if name != "" and flag == False:
            r['name'].append(name)
            birth = birth.replace('.', '-')
            r['birth'].append(birth)
    return r

def get_batterData(url):
    r = {'name': [], 'birth': []}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'tab_sty_02'}).find_all('tr')
    for tr in table:
        tdlist = tr.find_all('td')
        index = 0
        flag = False
        name = ""
        birth = ""
        for td in tdlist:
            string = str(td).split("<td>")
            
            if index == 1:
                name = str(td).split(">")[3].split("</p")[0].strip()
            elif index == 4:
                birth = str(td).split("<td>")[1].split("</td>")[0].strip()
            elif len(string) > 1 and index == 2:
                index2 = str(td).split("<td>")[1].split("</td>")[0].strip()
                if index2 == "투수" or index2 == "코치" or index2 == "감독":
                    flag = True
                    break
            index = index + 1
        
        if name != "" and flag == False:
            r['name'].append(name)
            birth = birth.replace('.', '-')
            r['birth'].append(birth)
    return r


pitcherList = get_pitcherData('http://www.ktwiz.co.kr/sports/site/baseball/player/all.do')
batterList = get_batterData('http://www.ktwiz.co.kr/sports/site/baseball/player/all.do')

print(pitcherList)
print(batterList)

r = open('./pitcher/ktwiz_p.csv', 'wt', newline='')
fieldnames = ['name', 'birth']

writer = csv.DictWriter(r, fieldnames=fieldnames)
writer.writeheader()

for i in range(0, len(pitcherList['name'])):
    writer.writerow({'name': pitcherList['name'][i], 'birth': pitcherList['birth'][i]})

r.close()

r = open('./batter/ktwiz_b.csv', 'wt', newline='')

writer = csv.DictWriter(r, fieldnames=fieldnames)
writer.writeheader()

for i in range(0, len(batterList['name'])):
    writer.writerow({'name': batterList['name'][i], 'birth': batterList['birth'][i]})

r.close()