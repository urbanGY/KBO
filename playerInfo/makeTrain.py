import csv

def make_date(date, list):
    month = date[5:7]
    month = int(month)
    for i in range(3,12):
        if month == i:
            list.append(1)
        else:
            list.append(0)
    return list

def make_inning(inning, list):
    inn = 0
    if inning[1] == '말' or inning[1] == '초':
        inn = int(inning[0])
    else :
        inn = int(inning[0:2])
    if inn <= 3:
        list.append(1)
        list.append(0)
        list.append(0)
    elif inn <= 6:
        list.append(0)
        list.append(1)
        list.append(0)
    else:
        list.append(0)
        list.append(0)
        list.append(1)
    return list

def make_before(before, list):
    death = before[0]
    if death == '1':
        list.append(0)
        list.append(1)
        list.append(0)
    elif death == '2':
        list.append(0)
        list.append(0)
        list.append(1)
    else :
        list.append(1)
        list.append(0)
        list.append(0)

    if before[4] == '루':
        if before[3] == '만':
            for i in range(3):
                list.append(1)
        else:
            for i in range(1,4):
                if int(before[3]) == i:
                    list.append(1)
                else:
                    list.append(0)
    elif before[6] == '루':
        for i in range(1,4):
            if int(before[3]) == i or int(before[5]) == i:
                list.append(1)
            else:
                list.append(0)
    else:
        for i in range(3):
            list.append(0)
    return list

def make_result(result, list):
    length = len(result)
    word = result[length-2:length]
    if word == '안타' or word == '루타' or word == '홈런':
        list.append(0)
        list.append(1)
        list.append(0)
    elif word == ' 볼' or word == '볼넷':
        list.append(0)
        list.append(0)
        list.append(1)
    else:
        list.append(1)
        list.append(0)
        list.append(0)
    return list

teamName = ['doosanbears','kiatigers','kiwoomheros','ktwiz','lgtwins','lottegiants','ncdinos','samsunglions']
fieldnames = ['3','4','5','6','7','8','9','10','11','1 - 3 inning','4 - 6 inning','7 - ? inning','no out','1 out','2 out','base_1','base_2','base_3','out','hit','ball']

# batter_class_size = 3
# pitcher_class_size = 4
# batter_class = []
# pitcher_class = []
# for i in range(batter_class_size):
#     tmp = []
#     batter_class.append(tmp)
#
# for i in range(pitcher_class_size):
#     tmp = []
#     pitcher_class.append(tmp)


for team in teamName:
    team_f = open('../crollingPart/teamList/batter/' + team + '_b.csv', 'rt')
    team_reader = csv.reader(team_f)
    for line in team_reader:
        if line[0] == 'name':
            continue
        player_f = open('./batter/' + team + '/'+ line[0]+'.csv', 'rt')
        player_reader = csv.reader(player_f)
        writeFile = open('./train/'+ team +'/'+ line[0] +'.csv',mode='wt',newline='')
        csv_writer = csv.DictWriter(writeFile, fieldnames=fieldnames)
        csv_writer.writeheader()
        attribute = []
        for day in player_reader:
            #0 - date, 2 - inning, 4 - p_class, 6 - b_class, result - 8, before - 9
            # 000000000 month, 000 inning, 00 death, 000 base
            if day[0] == 'date':
                continue
            attribute = make_date(day[0],attribute)
            attribute = make_inning(day[2],attribute)
            attribute = make_before(day[9],attribute)
            attribute = make_result(day[8],attribute)
            if len(attribute) != 0:
                csv_writer.writerow({'3':attribute[0],'4':attribute[1],'5':attribute[2],'6':attribute[3],'7':attribute[4],'8':attribute[5],'9':attribute[6],'10':attribute[7],'11':attribute[8],'1 - 3 inning':attribute[9],'4 - 6 inning':attribute[10],'7 - ? inning':attribute[11],'no out':attribute[12],'1 out':attribute[13],'2 out':attribute[14],'base_1':attribute[15],'base_2':attribute[16],'base_3':attribute[17],'out':attribute[18],'hit':attribute[19],'ball':attribute[20]})
                attribute = []

        writeFile.close()
        player_f.close()
        print('finish make train ',line[0],'file!')
    team_f.close()
