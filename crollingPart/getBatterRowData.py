import csv
from bs4 import BeautifulSoup
import requests

batterFileList = ['doosanbears_b', 'kiatigers_b', 'kiwoomheros_b', 'ktwiz_b', 'lgtwins_b', 'lottegiants_b', 'ncdinos_b', 'samsunglions_b']

def getBatterData(name, birth) :
    url = 'http://www.statiz.co.kr/player.php?opt=1&name=' + name + '&birth=' + birth
    response = requests.get(url)
    if response.status_code != 200:
        return
    
    output = response.text
    soup = BeautifulSoup(output, 'html.parser')
    table = soup.find_all('div', {'class' : 'box-body no-padding table-responsive'})
    print(table)
    soup = BeautifulSoup(table.get_text(), 'html.parser')


for filename in batterFileList:
    batterFile = open('./teamList/batter/' + filename + '.csv', 'rt')
    
    reader = csv.reader(batterFile)

    for line in reader:
        if line[0] == 'name':
            continue
        getBatterData(line[0], line[1])
    
