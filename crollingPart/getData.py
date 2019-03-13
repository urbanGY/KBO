import csv
from bs4 import BeautifulSoup
import requests


r = open('eagles_b.csv',mode='rt') #선수 명단의 맨 앞부분에 해당 팀명 들어가있어야함
list = r.read().splitlines()
r.close()
#25가 호잉


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

def write_csv(name,data,csv_writer):
    for i in range(0,len(data)):
            s = data[i].get_text()
            if len(s) < 1:
                continue
            if s[len(s)-1].isdigit():
                continue
            else:            
                a = []
                for j in range(i+20,i+26):
                    a.append(data[j].get_text())
                csv_writer.writerow([name,a[0],a[1],a[2],a[3],a[4],a[5]])
                i += 26        
    
f = open('output/'+list[0]+'.csv',mode='wt',newline='')
url = "http://www.statiz.co.kr/player.php?opt=1&name="
csv_writer = csv.writer(f)
csv_writer.writerow(['이름','타율','출루','장타','ops','wOBA','wRC+'])
for n in range(1,27):
    print(url+list[n])
    data = get_data(url+list[n])
    write_csv(list[n],data,csv_writer)
f.close()

