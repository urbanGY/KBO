import tensorflow as tf
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

################## 바꿔줘야 할 부분########################
batter_class_num = 5
pitcher_class_num = 5

player_data = open('../playerInfo/test/lottegiants/이대호.csv', 'rt')
player_reader = csv.reader(player_data)

batter_index = 3 #batter
################## 바꿔줘야 할 부분########################

player_split = [] #틀 만들기
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
    player_split[pit_index][inn_index][out_index][base_index].append(result) #틀 채우기


################################################################## model part
def decode(i,j,k,l):
    list = []
    for x in range(0,3): #inning
        if x == j:
            list.append(1)
        else :
            list.append(0)
    for x in range(0,3): #out
        if x == k:
            list.append(1)
        else :
            list.append(0)
    for x in range(0,2): #base
        if x == l:
            list.append(1)
        else :
            list.append(0)
    return i, list

train_size = 8
label_size = 3

x = tf.placeholder("float", [None,train_size])
y = tf.placeholder("float", [None,label_size])
keep_prob = tf.placeholder(tf.float32)

w_1 = tf.Variable(tf.truncated_normal(shape=[train_size, train_size*2], stddev=5e-2), name='weight')
b_1 = tf.Variable(tf.constant(0.1, shape=[train_size*2]), name='bias')
h_fc1 = tf.nn.relu(tf.matmul(x, w_1) + b_1)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

w_2 = tf.Variable(tf.truncated_normal(shape=[train_size*2, train_size*3], stddev=5e-2), name='weight')
b_2 = tf.Variable(tf.constant(0.1, shape=[train_size*3]), name='bias')
h_fc2 = tf.nn.relu(tf.matmul(h_fc1_drop, w_2) + b_2)
h_fc2_drop = tf.nn.dropout(h_fc2, keep_prob)

w_3 = tf.Variable(tf.truncated_normal(shape=[train_size*3, train_size*2], stddev=5e-2), name='weight')
b_3 = tf.Variable(tf.constant(0.1, shape=[train_size*2]), name='bias')
h_fc3 = tf.nn.relu(tf.matmul(h_fc2_drop, w_3) + b_3)
h_fc3_drop = tf.nn.dropout(h_fc3, keep_prob)

w_4 = tf.Variable(tf.truncated_normal(shape=[train_size*2, label_size], stddev=5e-2), name='weight')
b_4 = tf.Variable(tf.constant(0.1, shape=[label_size]), name='bias')
logits = tf.matmul(h_fc3_drop,w_4)+b_4
y_pred = tf.nn.softmax(logits)

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=logits))
train_step = tf.train.GradientDescentOptimizer(1e-3).minimize(loss)

saver = tf.train.Saver()
value = 0
for i in range(pitcher_class_num): #pitcher
    for j in range(3): #inning
        for k in range(3): #out
            for l in range(2): #base
                if len(player_split[i][j][k][l]) <= 10:
                    continue
                real_hit, real_go = getHit(player_split[i][j][k][l])#해당 상황에서의 타율, 출루율 계산
                pitcher_index, input_x = decode(i,j,k,l) #임의로 입력
                with tf.Session() as sess:
                    saver.restore(sess, './models/'+str(batter_index)+'-'+str(pitcher_index)+'.ckpt')
                    tmp = []
                    tmp.append(input_x)
                    pred = sess.run(y_pred, feed_dict={x:tmp, keep_prob:1.0}) #결과
                    pred_hit = pred[0][1]
                    pred_go = 1 - pred[0][0]
                    value += (real_go - pred_go) ** 2
                    print("pitcher class : %d , inning : %d , out : %d , base : %d - case size : %d"%(i,j,k,l,len(player_split[i][j][k][l])))
                    print("예측) 타율 : %.3f , 출루율 : %.3f - > 실제) 타율 : %.3f , 출루율 : %.3f\n"%(pred_hit,pred_go,real_hit,real_go))
print(value)
