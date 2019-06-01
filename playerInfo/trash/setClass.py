import csv

batter_class_num = 4
pitcher_class_num = 4

teamName = ['doosanbears','kiatigers','kiwoomheroes','ktwiz','lgtwins','lottegiants','ncdinos','samsunglions']
fieldnames = ['3','4','5','6','7','8','9','10','11','1 - 3 inning','4 - 6 inning','7 - ? inning','no out','1 out','2 out','base_1','base_2','base_3','out','hit','ball','batterName','batterClass','pitcherName','pitcherClass']

batter_class_f = open('../clustering/clusterOutput/classification.csv', mode='rt',newline='')#기존 train file 가져옴
batter_class_reader = csv.reader(batter_class_f)#타자 class dictionary
#pitcher_class_f = open('location', mode='rt',newline='')#기존 train file 가져옴
#pitcher_class_reader = csv.reader(pitcher_class_f)#투수 class dictionary

def get_batter_class(name): #batter class 찾는 함수
    for class_index in range(batter_class_num):
        r = 1
        while(batter_class_reader[r][class_index] is not None):
            if batter_class_reader[r][class_index] == name:
                return class_index
            r += 1

# get_pitcher_class func



for team in teamName:
    team_f = open('../crollingPart/teamList/batter/' + team + '_b.csv', 'rt')
    team_reader = csv.reader(team_f)
    for name in team_reader:
        if name[0] == 'name':
            continue
        batter_class = get_batter_class(name[0]) #set batter class
        train_f = open('./train/' + team + '/'+ name[0]+'.csv', 'rt') #분류 빼고 준비된 트레이닝 파일 불러옴
        train_reader = csv.reader(train_f) #수정해야할 train
        for line in train_reader:
            #pitcher_name = line[]

        train_f.close()
    team_f.close()
batter_class_f.close()
