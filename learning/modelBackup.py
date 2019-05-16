import tensorflow as tf
import csv

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
    return list

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

input_x = decode(5,1,1,1) #임의로 입력
print(input_x)
input_y = [0,1,0] #임의로 입력
with tf.Session() as sess:
    batter_index = 9 #batter
    pitcher_index = 5 #pitcher
    saver.restore(sess, './models/'+str(batter_index)+'-'+str(pitcher_index)+'.ckpt')
    tmp = []
    tmp.append(input_x)
    pred = sess.run(y_pred, feed_dict={x:tmp, keep_prob:1.0}) #결과
    hit = pred[0][1]
    go = 1 - pred[0][0]
    s = '예측 타율 : '+str(round(hit, 3))+', 예측 출루율 : '+str(round(go,3))
    print(s)

#한화 sk 타자 투수 정보 수집, 기존 체계에 추가시키기 0.857
#2018, 2019자료 사용
#입력 데이터 어떻게 받아올지 생각
#받아 온 데이터 숫자만큼 세션 활성화 시켜서 결과 뽑아내기
#뽑아 낸 결과 어떻게 웹 페이지로 보낼 지 생각
#결과 검증으 어떻게 할지 생각..
