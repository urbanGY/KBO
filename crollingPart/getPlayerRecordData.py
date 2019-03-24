import csv
from bs4 import BeautifulSoup
import requests

'''
doosan_b.csv
eagles_b.csv
kia_b.csv
kt_b.csv
lg_b.csv
lotte_b.csv
nc_b.csv
nexen_b.csv
samsung_b.csv
sk_b.csv

'''

def get_html(url):
    output = ""
    response = requests.get(url)
    if response.status_code == 200:
        output = response.text
    return output    

def get_data(url):
    text = get_html(url)
    soup = BeautifulSoup(text, 'html.parser')
    data = soup.find_all("td",{"class":"statdata"}) #가까운 table을 찾고 그 안에 모든 td를 추출, 반환형이 string 아님
    return data

def get_arr(data):
    arr = []
    for i in range(0,len(data)):
            s = data[i].get_text()
            if len(s) < 1:
                continue
            if s[len(s)-1].isdigit():
                continue
            else:
                if data[i+20].get_text() == '' or data[i+20].get_text() == '0.000': #공백 전적 제거
                    i += 26
                    continue
                a = []
                for j in range(i+20,i+26):
                    a.append(data[j].get_text())
                arr.append(a)    
                i += 26
    if len(arr) != 0:            
        del(arr[len(arr)-1]) #통산전적 제거           
    return arr


def make_attribute(arr):
    length = len(arr)
    if length == 1:
        return arr[0]
    else:
        output = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        n = 0
        for i in range(1,length+1):
            n += i
        for i in range(1,length):
            for j in range(0,6):
                output[j] += (float(arr[i-1][j])/n)*i        
        for i in range(0,6):
            output[i] += float(arr[length-1][i])*(1-float(n-length)/n)
        for i in range(0,6):
            output[i] = round(output[i],3)
        return output

teamList = ['doosanbears','kiwoomheros','ktwiz','lottegiants','ncdinos','samsunglions','lgtwins', 'kiatigers']
fieldnames = ['name','avg','base','slg','ops','wOBA','wRC+']
url = "http://www.statiz.co.kr/player.php?opt=1&name="
writeFile = open('batter.csv',mode='wt',newline='')
csv_writer = csv.DictWriter(writeFile, fieldnames=fieldnames)
csv_writer.writeheader()

for team in teamList:
    f = open('./teamList/batter/' + team + '_b.csv', 'rt')
    print('./teamList/batter/' + team + '_b.csv')
    reader = csv.reader(f)
    playerList = {'name': [],'birth': []}
    for line in reader:
        name = line[0]
        birth = line[1]
        if(birth != 'birth'):
            playerList['name'].append(name)
            playerList['birth'].append(birth)
    
    f.close()
    
    for index in range(0, len(playerList['name'])):
        playerUrl = url + playerList['name'][index] + "&birth=" + playerList['birth'][index]
        data = get_data(playerUrl)
        arr = get_arr(data)
        if len(arr) != 0:
            attr = make_attribute(arr)
            csv_writer.writerow({'name':playerList['name'][index], 'avg':attr[0], 'base':attr[1], 'slg':attr[2], 'ops':attr[3], 'wOBA':attr[4], 'wRC+':attr[5]})
        else:
            print(playerUrl, "크롤링 안됨")

writeFile.close()


"""
for teamList in team:
    r = open('batterList/'+teamList,mode='rt') #선수 명단의 맨 앞부분에 해당 팀명 들어가있어야함
    list = r.read().splitlines()
    r.close()
    f = open('batterOutput/'+list[0]+'.csv',mode='wt',newline='')
    url = "http://www.statiz.co.kr/player.php?opt=1&name="
    fieldnames = ['이름','타율','출루','장타','ops','wOBA','wRC+']
    csv_writer = csv.DictWriter(f, fieldnames=fieldnames)
    csv_writer.writeheader()
    for n in range(1,len(list)):
        print(url+list[n])
        data = get_data(url+list[n])
        arr = get_arr(data)
        if len(arr) != 0:
            attr = make_attribute(arr)   
            csv_writer.writerow({'이름':list[n], '타율':attr[0], '출루':attr[1], '장타':attr[2], 'ops':attr[3], 'wOBA':attr[4], 'wRC+':attr[5]})
        else:
            print(list[n]+' 크롤링 제대로 안됨')
    f.close()
"""
