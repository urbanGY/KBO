import csv
from bs4 import BeautifulSoup
import requests


def get_data(personUrl, pcodeList):
    for pcode in pcodeList:
        response = requests.get(personUrl + str("?pcode=") + str(pcode))
        soup = BeautifulSoup(response.text, "html.parser")

        roster = soup.find('div', {'class': 'roster_list_new'}).find_all('a')

        for player in roster:
            string = str(player)
            param = string.split('href="')[1].split('"')[0]
            print(personUrl + param, "\n")

        


personUrl = 'http://www.giantsclub.com/html'
pitcherUrl = [819]
batterUrl = [820, 821, 822]

get_data(personUrl, pitcherUrl)