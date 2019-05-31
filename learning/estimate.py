import numpy as np
import tensorflow as tf
import csv
import math
print('import np, tf, csv, math complelte!')


#유형별 학습시킬 list 분리 저장 ex) 타자 유형 1, 투수 유형 3의 trainList는 trainList[1][3] 으로 접근 가능한 틀 생성
batter_class_num = 8
pitcher_class_num = 7

def getRealHit(batter_class, pitcher_class, name, team):
    player_f = open('../playerInfo/test/' + team + '/'+ name +'.csv', 'rt')
    #open(_url + team + "\\"+ batter_name +'.csv', 'rt')
    player_reader = csv.reader(player_f)

    out_cnt = 0
    hit_cnt = 0
    cnt = 0
    for line in player_reader: #14 == pitcher class
        if line[14] == str(pitcher_class):
            cnt += 1
            if line[8] == '1':
                out_cnt += 1
            if line[9] == '1':
                hit_cnt += 1
    hit = hit_cnt/cnt
    go = 1 - (out_cnt/cnt)
    player_f.close()
    return round(hit,3), round(go,3)

def getList(bat, pit):
    list = []
    for i in range(bat):
        bat = []
        for j in range(pit):
            tmp = [0,0]
            bat.append(tmp)
        list.append(bat)
    return list


train_size = 8 #학습시킬 속성 차원 수
label_size = 3 #결과 차원 수

#각 유형별 학습을 진행해 각각의 model을 생성한다
x = tf.placeholder("float", [None,train_size])
y = tf.placeholder("float", [None,label_size])
keep_prob = tf.placeholder(tf.float32)

w_1 = tf.Variable(tf.truncated_normal(shape=[train_size, train_size*2], stddev=5e-2), name='weight_1')
b_1 = tf.Variable(tf.constant(0.1, shape=[train_size*2]), name='bias_1')
h_fc1 = tf.nn.relu(tf.matmul(x, w_1) + b_1)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

w_2 = tf.Variable(tf.truncated_normal(shape=[train_size*2, train_size*3], stddev=5e-2), name='weight_2')
b_2 = tf.Variable(tf.constant(0.1, shape=[train_size*3]), name='bias_2')
h_fc2 = tf.nn.relu(tf.matmul(h_fc1_drop, w_2) + b_2)
h_fc2_drop = tf.nn.dropout(h_fc2, keep_prob)

w_3 = tf.Variable(tf.truncated_normal(shape=[train_size*3, train_size*2], stddev=5e-2), name='weight_3')
b_3 = tf.Variable(tf.constant(0.1, shape=[train_size*2]), name='bias_3')
h_fc3 = tf.nn.relu(tf.matmul(h_fc2_drop, w_3) + b_3)
h_fc3_drop = tf.nn.dropout(h_fc3, keep_prob)

w_4 = tf.Variable(tf.truncated_normal(shape=[train_size*2, label_size], stddev=5e-2), name='weight_4')
b_4 = tf.Variable(tf.constant(0.1, shape=[label_size]), name='bias_4')
logits = tf.matmul(h_fc3_drop,w_4)+b_4
y_pred = tf.nn.softmax(logits)


#위에서 생성한 틀에 맞춰서 학습시켜야 할 내용 체움
#teamName = ['doosanbears','kiatigers','kiwoomheroes','ktwiz','lgtwins','lottegiants','ncdinos','samsunglions','hanwhaeagles','skwyverns']
teamName = ['doosanbears']
#fieldnames = ['3','4','5','6','7','8','9','10','11','1 - 3 inning','4 - 6 inning','7 - ? inning','no out','1 out','2 out','base_1','base_2','base_3','out','hit','ball','batterName','batterClass','pitcherName','pitcherClass'] default
fieldnames = ['1 - 3 inning','4 - 6 inning','7 - ? inning','no out','1 out','2 out','base_o','base_x','out','hit','ball','batterName','batterClass','pitcherName','pitcherClass']
#21 b_name, 22 b_class, 23 p_name, 24 p_class
saver = tf.train.Saver()
summary = 0
for team in teamName:
    team_f = open('../crollingPart/teamList/batter/' + team + '_b.csv', 'rt')
    team_reader = csv.reader(team_f)
    for line in team_reader: #선수 한명
        if line[0] == 'name':
            continue
        estimate_val = 0 #선수에 대한 표준편차용
        cnt = 0
        player_data = open('../playerInfo/test/' + team + '/'+ line[0] +'.csv', 'rt')
        player_reader = csv.reader(player_data)
        real_restore = getList(batter_class_num, pitcher_class_num)
        for record in player_reader:
            if record[0] == '1 - 3 inning' or record[12] == '-1' or record[14] == '-1': #둘중 하나만 -1이면 list에 안가져옴
                continue
            cnt += 1
            batter_index = int(record[12])
            pitcher_index = int(record[14])
            tmp_train = []
            for n in range(0,8):
                tmp_train.append(record[n])
            test_block = []
            test_block.append(tmp_train)
            with tf.Session() as sess:
                saver.restore(sess, './models/' +str(batter_index)+'-'+str(pitcher_index)+'.ckpt')
                pred = sess.run(y_pred, feed_dict={x:test_block, keep_prob:1.0}) #결과
                hit = round(pred[0][1], 3)
                go = round(1 - pred[0][0], 3) #예측 부분
                if real_restore[batter_index][pitcher_index][0] == 0:
                    real_hit, real_go = getRealHit(batter_index, pitcher_index, line[0], team)
                    real_restore[batter_index][pitcher_index][0] = real_hit
                    real_restore[batter_index][pitcher_index][1] = real_go
                else :
                    real_hit = real_restore[batter_index][pitcher_index][0]
                    real_go = real_restore[batter_index][pitcher_index][1]

                estimate_val += math.pow((hit - real_hit),2)
                estimate_val += math.pow((go - real_go),2)
        if cnt == 0:
            continue
        estimate_val = math.sqrt(estimate_val/cnt)
        print(line[0]+' : ',estimate_val,' cnt : ',cnt)
        summary += estimate_val
        player_data.close()
    team_f.close()
print('summary : ',summary)
