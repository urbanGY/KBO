import csv

def getIndex(list):
    for n in range(len(list)):
        if list[n] == '1':
            return n

def getHit(list):
    hit_cnt = 0
    out_cnt = 0
    for n in list:
        if n == 0:
            out_cnt += 1
        if n == 1:
            hit_cnt += 1
    hit = hit_cnt/len(list)
    go = 1-(out_cnt/len(list))
    return hit, go

batter_class_num = 10
pitcher_class_num = 6

player_data = open('../playerInfo/test/doosanbears/오재원.csv', 'rt')
player_reader = csv.reader(player_data)

player_split = []
for i in range(pitcher_class_num):
    pit_block = []
    for j in range(3):
        inn_block = []
        for k in range(3):
            out_block = []
            for l in range(2):
                base_block = []
                out_block.append(base_block)
            inn_block.append(out_block)
        pit_block.append(inn_block)
    player_split.append(pit_block)


# 000 000 00 - 000 - b bc p pc
# player_split[pitcher][inning][out][base] -> 0,1,2 (out, hit, go)
# 0 1 2 -> inning , 3 4 5 -> out count , 6 7 -> base o/x
for record in player_reader:
    if record[0] == '1 - 3 inning' or record[12] == '-1' or record[14] == '-1': #둘중 하나만 -1이면 list에 안가져옴
        continue
    pit_index = int(record[14])
    inn_index = getIndex(record[0:3])
    out_index = getIndex(record[3:6])
    base_index = getIndex(record[6:8])
    result = getIndex(record[8:11])
    player_split[pit_index][inn_index][out_index][base_index].append(result)

for i in range(pitcher_class_num): #pitcher
    for j in range(3): #inning
        for k in range(3): #out
            for l in range(2): #base
                if len(player_split[i][j][k][l]) == 0:
                    continue
                #print("pitcher class : %d , inning : %d , out : %d , base : %d - case size : %d"%(i,j,k,l,len(player_split[i][j][k][l])))
                print(i,j,k,l,len(player_split[i][j][k][l]))
                hit, go = getHit(player_split[i][j][k][l])
                print("타율 : %.3f , 출루율 : %.3f\n"%(hit,go))
