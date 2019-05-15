import csv
import requests
from bs4 import BeautifulSoup

fieldNames = ['이름', '출장', '완투', '완봉', '선발', '승', '패', '세', '홀드', '이닝', '실점', '자책', '타자', '안타', '홈런', '볼넷', '고4', '사구', '삼진', '보크', '폭투']

teamList = ['doosanbears', 'hanwhaeagles', 'kiatigers', 'kiwoomheroes', 'ktwiz', 'lgtwins', 'lottegiants', 'ncdinos', 'samsunglions', 'skwyverns']
writeFile = open("pitcher.csv", "wt", newline="")
csvheaderwriter = csv.writer(writeFile)
csvheaderwriter.writerow(fieldNames)
for team in teamList:
    file = open("./teamList/pitcher/" + team + '_p.csv', mode='r')
    reader = csv.reader(file)
    for line in reader:
        if line[0] != "name":
            print(line[0], line[1])
            request = requests.get("http://www.statiz.co.kr/player.php?opt=0&name=" + line[0] + "&birth=" + line[1])
            soup = BeautifulSoup(request.content, "html.parser")
            data = soup.select("td.statdata")
            index = 0
            flag = False
            fields = [line[0]]
            for line in data:
                if flag == True :
                    index = index + 1
                    p = str(line).split('</span>')[0].split('>')[-1]
                    if 1 <= index and index <= 20:
                        try:
                            fields.append(float(p))
                        except ValueError:
                            fields.append(0)
                    elif index == 21:
                        flag = False
                if line.previous_element == '통산':
                    flag = True
                    index = 0
            
            if len(fields) == len(fieldNames):
                csvheaderwriter.writerow(fields)
            else:
                print('크롤링 실패')
    file.close()
writeFile.close()

            
