import csv
from bs4 import BeautifulSoup
import requests

def get_html(url):
    output = ""
    response = requests.get(url)
    if response.status_code == 200:
        output = response.text
    return output

def get_data(url):
    text = get_html(url)
    soup = BeautifulSoup(text, 'html.parser')
    table = soup.find("table",{"class":"table-striped"})
    if table is not None:
        data = table.find_all("td") #가까운 table을 찾고 그 안에 모든 td를 추출, 반환형이 string 아님
    else :
        data = 'no_data'
    return data


teamName = ['doosanbears','kiatigers','kiwoomheros','ktwiz','lgtwins','lottegiants','ncdinos','samsunglions']
yearList = ['2017','2016','2015','2014']
fieldnames = ['date','opponent','inning','pitcher','p_class','batter','b_class','P','result','before']

for team in teamName:
    team_f = open('../crollingPart/teamList/batter/' + team + '_b.csv', 'rt')
    team_reader = csv.reader(team_f)
    playerList = {'name':[],'birth':[]}
    for line in team_reader:
        name = line[0]
        birth = line[1]
        if(birth != 'birth'):
            playerList['name'].append(name)
            playerList['birth'].append(birth)
    team_f.close()
    print('complete get '+ team +' player name, birth List!')

     # 2018은 validate data 로 별도로 분리
    for i in range(0, len(playerList['name'])):
        writeFile = open('./batter/'+ team +'/'+ playerList['name'][i] +'.csv',mode='wt',newline='')
        csv_writer = csv.DictWriter(writeFile, fieldnames=fieldnames)
        csv_writer.writeheader()
        for year in yearList:
            url = "http://www.statiz.co.kr/player.php?opt=6&sopt=0&name="+ playerList['name'][i] +"&birth="+ playerList['birth'][i] +"&re=0&da=1&year="+ year +"&plist=&pdate="
            list = get_data(url)
            if list == 'no_data':
                continue
            for n in range(0, len(list), 14):
                csv_writer.writerow({'date':list[n].get_text(),'opponent':list[n+1].get_text(),'inning':list[n+2].get_text(),'pitcher':list[n+3].get_text(),'p_class':'A','batter':list[n+4].get_text(),'b_class':'B','P':list[n+5].get_text(),'result':list[n+6].get_text(),'before':list[n+7].get_text()})
        writeFile.close()
        print('complete write '+playerList['name'][i]+' file!')
