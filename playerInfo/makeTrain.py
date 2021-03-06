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
        list.append(0) #out convention

    # if before[4] == '루':
    #     if before[3] == '만':
    #         for i in range(3):
    #             list.append(1)
    #     else:
    #         for i in range(1,4):
    #             if int(before[3]) == i:
    #                 list.append(1)
    #             else:
    #                 list.append(0)
    # elif before[6] == '루':
    #     for i in range(1,4):
    #         if int(before[3]) == i or int(before[5]) == i:
    #             list.append(1)
    #         else:
    #             list.append(0)
    # else:
    #     for i in range(3):
    #         list.append(0)
    if before[4] == '루':
        list.append(1)
        list.append(0)
    else:
        list.append(0)
        list.append(1)
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

teamName = ['doosanbears','kiatigers','kiwoomheroes','ktwiz','lgtwins','lottegiants','ncdinos','samsunglions','hanwhaeagles','skwyverns']
#fieldnames = ['3','4','5','6','7','8','9','10','11','1 - 3 inning','4 - 6 inning','7 - ? inning','no out','1 out','2 out','base_1','base_2','base_3','out','hit','ball','batterName','batterClass','pitcherName','pitcherClass'] default
fieldnames = ['1 - 3 inning','4 - 6 inning','7 - ? inning','no out','1 out','2 out','base_o','base_x','out','hit','ball','batterName','batterClass','pitcherName','pitcherClass']

batter_class_f = open('../clustering/clusterOutput/classification_batter_2.csv', mode='rt',newline='')#기존 train file 가져옴
batter_class_reader = list(csv.reader(batter_class_f))#타자 class dictionary
pitcher_class_f = open('../clustering/clusterOutput/classification_pitcher_2.csv', mode='rt',newline='')#기존 train file 가져옴
pitcher_class_reader = list(csv.reader(pitcher_class_f))#투수 class dictionary

batter_class_num = len(batter_class_reader[0])
pitcher_class_num = len(pitcher_class_reader[0])
def get_batter_class(name): #batter class 찾는 함수
    for line in batter_class_reader:
        for i in range(batter_class_num):
            if line[i] == name:
                return i
    return -1

def get_pitcher_class(name): #batter class 찾는 함수
    for line in pitcher_class_reader:
        for i in range(pitcher_class_num):
            if line[i] == name:
                return i
    return -1


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
        batter_class = get_batter_class(line[0])#타자 class 미리 추출
        #player_f = open('./batter/' + team + '/'+ line[0]+'.csv', 'rt')
        player_f = open('./batter_test/' + team + '/'+ line[0]+'.csv', 'rt')
        player_reader = csv.reader(player_f)
        #writeFile = open('./train/'+ team +'/'+ line[0] +'.csv',mode='wt',newline='')
        writeFile = open('./test/'+ team +'/'+ line[0] +'.csv',mode='wt',newline='')
        csv_writer = csv.DictWriter(writeFile, fieldnames=fieldnames)
        csv_writer.writeheader()
        attribute = []

        for day in player_reader:
            #0 - date, 2 - inning, 4 - p_class, 6 - b_class, result - 8, before - 9
            # 000000000 month, 000 inning, 00 death, 000 base
            if day[0] == 'date':
                continue
            #attribute = make_date(day[0],attribute) date 제거
            attribute = make_inning(day[2],attribute) # 0 1 2
            attribute = make_before(day[9],attribute) # 3 4 5 , 6 7
            attribute = make_result(day[8],attribute) # 8 9 10
            attribute.append(day[5])#batter Name 11
            attribute.append(batter_class)#batter class 12
            attribute.append(day[3])#pither name 13
            attribute.append(get_pitcher_class(day[3]))#pitcher class 14
            if len(attribute) != 0:
                csv_writer.writerow({'1 - 3 inning':attribute[0],'4 - 6 inning':attribute[1],'7 - ? inning':attribute[2],'no out':attribute[3],'1 out':attribute[4],'2 out':attribute[5],'base_o':attribute[6],'base_x':attribute[7],'out':attribute[8],'hit':attribute[9],'ball':attribute[10],'batterName':attribute[11],'batterClass':attribute[12],'pitcherName':attribute[13],'pitcherClass':attribute[14]})
                attribute = []

        writeFile.close()
        player_f.close()
        print('finish make train ',line[0],'file!')
    team_f.close()
batter_class_f.close()
