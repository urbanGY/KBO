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
r = open('batterList/doosan_b.csv',mode='rt') #선수 명단의 맨 앞부분에 해당 팀명 들어가있어야함
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
            output[i] = round(output[i],3);
        return output             
    
f = open('output/'+list[0]+'.csv',mode='wt',newline='')
url = "http://www.statiz.co.kr/player.php?opt=1&name="
csv_writer = csv.writer(f)
csv_writer.writerow(['이름','타율','출루','장타','ops','wOBA','wRC+'])
for n in range(1,len(list)):
    print(url+list[n])
    data = get_data(url+list[n])
    arr = get_arr(data)
    if len(arr) != 0:
        attr = make_attribute(arr)    
        csv_writer.writerow([list[n],attr[0],attr[1],attr[2],attr[3],attr[4],attr[5]])
    else:
        print(list[n]+' 크롤링 제대로 안됨')
f.close()

