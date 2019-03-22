import csv
import requests
from bs4 import BeautifulSoup

def get_data(allUrl, personUrl):
    result = {'name': [], 'birth': []}
    pidList = []
    for url in allUrl:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        playerList = soup.find('table', {'class': 'tb_player_info'}).find_all('li')
        for li in playerList:
            pid = 0
            string = str(li)
            for i in range(0, len(string)):
                try:
                    pid = pid * 10 + int(string[i])
                except ValueError:
                    continue
     
            pidList.append(pid)
    
    for pid in pidList:
        name = ""
        birth = ""
        params = {'pid' : pid}
        response = requests.get(personUrl, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        ddList = soup.find('dl', {'class': 'pl_description'}).find_all('dd')
        for dd in ddList:
            string = str(dd)
            index = string.split("<strong>")[1].split("</strong>")[0].strip()
            if index == "이름":
                name = string.split(":")[1].split('/')[0].strip()
            elif index == "생년월일":
                birth = string.split(":")[1].split('<')[0].strip()
        
        birth = birth.replace("년 ", '-').replace("월 ", "-").replace("일", '').strip()

        result['name'].append(name)
        result['birth'].append(birth)
    
    return result

pitcherUrl = ['http://ncdinos.com/player/pitcher']
batterUrl = ['http://ncdinos.com/player/catcher', 'http://ncdinos.com/player/infielder', 'http://ncdinos.com/player/outfielder']
personUrl = 'http://ncdinos.com/player/person'

r = open('./pitcher/ncdinos_p.csv', 'wt', newline='')
fieldnames = ['name', 'birth']

pitcherList = get_data(pitcherUrl, personUrl)
batterList = get_data(batterUrl, personUrl)

print(pitcherList)
print(batterList)

writer = csv.DictWriter(r, fieldnames=fieldnames)
writer.writeheader()

for i in range(0, len(pitcherList['name'])):
    writer.writerow({'name': pitcherList['name'][i], 'birth': pitcherList['birth'][i]})

r.close()

r = open('./batter/ncdinos_b.csv', 'wt', newline='')

writer = csv.DictWriter(r, fieldnames=fieldnames)
writer.writeheader()

for i in range(0, len(batterList['name'])):
    writer.writerow({'name': batterList['name'][i], 'birth': batterList['birth'][i]})

r.close()