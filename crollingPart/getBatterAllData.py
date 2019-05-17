import csv
import requests
from bs4 import BeautifulSoup

fieldNames = ['이름', 'G', '타석', '타수', '득점', '안타', '2타', '3타', '홈런', '루타', '타점', '볼넷', '사구', '고4', '삼진', '타율', '출루', '장타', 'OPS']

teamList = ['doosanbears', 'hanwhaeagles', 'kiatigers', 'kiwoomheroes', 'ktwiz', 'lgtwins', 'lottegiants', 'ncdinos', 'samsunglions', 'skwyverns']
writeFile = open("batter.csv", "wt", newline="")
csvheaderwriter = csv.writer(writeFile)
csvheaderwriter.writerow(fieldNames)
for team in teamList:
    file = open("./teamList/batter/" + team + '_b.csv', mode='r')
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
                    if 2 <= index and index <= 11:
                        try:
                            fields.append(int(p))
                        except ValueError:
                            fields.append(0)
                    elif 14 <= index and index <= 17:
                        try:
                            fields.append(int(p))
                        except ValueError:
                            fields.append(0)
                    elif 21 <= index and index <= 24:
                        try:
                            fields.append(float(p))
                        except ValueError:
                            fields.append(0)
                    elif index == 25:
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

            
