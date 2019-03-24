import csv
from bs4 import BeautifulSoup

fieldnamesBatter = ['이름', '타율','BABIP','볼넷%','삼진%','볼/삼','ISO','타수/홈런', 'OPS', 'RC', 'RC/27', 'wRC', 'SPD', 'wSB', 'wOBA', 'wRAA']
fieldnamesPitcher = ['이름', '삼진%', '볼넷%', '삼/볼', '피안타율', '피출루율', '피장타율', '피OPS', 'WHIP', 'BABIP', 'LOB%', 'ERA', 'RA9-ERA', 'FIP', 'kFIP', 'WAR']

def getTrList(fileName):
    f = open(fileName, 'rt')
    soup = BeautifulSoup(f.read(), 'html.parser')
    trList = soup.find_all('tr')
    f.close()
    return trList

def getBatterList(fileName):
    r = []
    trList = getTrList(fileName)

    for tr in trList:
        td = tr.find_all('td')
        if len(td) != 0:
            player = {}
            player['이름'] = str(td[1]).split('">')[2].split('<')[0].strip().replace('*', '')
            index = 4
            for field in fieldnamesBatter :
                if field == '이름':
                    continue
                if str(td[index]).split('>')[1].split('<')[0].strip() == '-' :
                    player[field] = '500'
                else:
                    player[field] = float(str(td[index]).split('>')[1].split('<')[0].strip())
                index = index + 1
            r.append(player)
    return r

def getPitcherList(fileName):
    r = []
    trList = getTrList(fileName)

    for tr in trList:
        td = tr.find_all('td')
        if len(td) != 0:
            flag = False
            player = {}
            player['이름'] = str(td[1]).split('">')[2].split('<')[0].strip().replace('*', '')
            index = 3
            for field in fieldnamesPitcher:
                if field == '이름':
                    continue
                if str(td[index]).split('>')[1].split('<')[0].strip() == '-':
                    flag = True
                    break
                player[field] = float(str(td[index]).split('>')[1].split('<')[0].strip())
                index = index + 1

            if flag == False:
                r.append(player)
    return r

kbreportBatterFile = ['.\\kbreport\\batter\\kbreport1.txt', '.\\kbreport\\batter\\kbreport2.txt', '.\\kbreport\\batter\\kbreport3.txt', '.\\kbreport\\batter\\kbreport4.txt', '.\\kbreport\\batter\\kbreport5.txt', 
                      '.\\kbreport\\batter\\kbreport6.txt', '.\\kbreport\\batter\\kbreport7.txt', '.\\kbreport\\batter\\kbreport8.txt']
kbreportPitcherFile = ['.\\kbreport\\pitcher\\kbreport1.txt', '.\\kbreport\\pitcher\\kbreport2.txt']

writeFile = open('kbreportBatter.csv',mode='wt',newline='')
csv_writer = csv.DictWriter(writeFile, fieldnames=fieldnamesBatter)
csv_writer.writeheader()

for fileName in kbreportBatterFile:
    recordList = getBatterList(fileName)
    for record in recordList:
        csv_writer.writerow(record)

writeFile.close()

writeFile = open('kbreportPitter.csv', mode='wt', newline='')
csv_writer = csv.DictWriter(writeFile, fieldnames=fieldnamesPitcher)
csv_writer.writeheader()

for fileName in kbreportPitcherFile:
    recordList = getPitcherList(fileName)
    for record in recordList:
        csv_writer.writerow(record)

writeFile.close()