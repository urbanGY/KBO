import numpy as np
import tensorflow as tf
import csv
print('import np, tf, csv complelte!')

#label feature : 출루/출루실패
#input feature : date, inning , before
teamName = ['doosanbears','kiatigers','kiwoomheros','ktwiz','lgtwins','lottegiants','ncdinos','samsunglions']
fieldnames = ['3','4','5','6','7','8','9','10','11','1 - 3 inning','4 - 6 inning','7 - ? inning','no out','1 out','2 out','base_1','base_2','base_3','out','hit','ball']

trainList = []
labelList = []
for team in teamName:
    team_f = open('../crollingPart/teamList/batter/' + team + '_b.csv', 'rt')
    team_reader = csv.reader(team_f)
    for line in team_reader:
        if line[0] == 'name':
            continue
        player_data = open('../playerInfo/train/' + team + '/'+ line[0] +'.csv', 'rt')
        player_reader = csv.reader(player_data)
        for record in player_reader:
            if record[0] == '3':
                continue
            tmp_train = []
            tmp_label = []
            for n in range(0,18):
                tmp_train.append(record[n])
            for n in range(18,21):
                tmp_label.append(record[n])
            trainList.append(tmp_train)
            labelList.append(tmp_label)
print(len(trainList))
print(len(labelList))
