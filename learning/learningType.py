import numpy as np
import tensorflow as tf
import csv
print('import np, tf, csv complelte!')


#유형별 학습시킬 list 분리 저장 ex) 타자 유형 1, 투수 유형 3의 trainList는 trainList[1][3] 으로 접근 가능한 틀 생성
batter_class_num = 8
pitcher_class_num = 7

trainList = []
labelList = []

for i in range(batter_class_num):
    train_pit = []
    label_pit = []
    for j in range(pitcher_class_num):
        train_tmp = []
        label_tmp = []
        train_pit.append(train_tmp)
        label_pit.append(label_tmp)
    trainList.append(train_pit)
    labelList.append(label_pit)


#위에서 생성한 틀에 맞춰서 학습시켜야 할 내용 체움
teamName = ['doosanbears','kiatigers','kiwoomheroes','ktwiz','lgtwins','lottegiants','ncdinos','samsunglions','hanwhaeagles','skwyverns']
#fieldnames = ['3','4','5','6','7','8','9','10','11','1 - 3 inning','4 - 6 inning','7 - ? inning','no out','1 out','2 out','base_1','base_2','base_3','out','hit','ball','batterName','batterClass','pitcherName','pitcherClass'] default
fieldnames = ['1 - 3 inning','4 - 6 inning','7 - ? inning','no out','1 out','2 out','base_o','base_x','out','hit','ball','batterName','batterClass','pitcherName','pitcherClass']
#21 b_name, 22 b_class, 23 p_name, 24 p_class
for team in teamName:
    team_f = open('../crollingPart/teamList/batter/' + team + '_b.csv', 'rt')
    team_reader = csv.reader(team_f)
    for line in team_reader: #선수 한명
        if line[0] == 'name':
            continue
        player_data = open('../playerInfo/train/' + team + '/'+ line[0] +'.csv', 'rt')
        player_reader = csv.reader(player_data)
        for record in player_reader:
            if record[0] == '1 - 3 inning' or record[12] == '-1' or record[14] == '-1': #둘중 하나만 -1이면 list에 안가져옴
                continue
            bat_index = int(record[12])
            pit_index = int(record[14])
            tmp_train = []
            tmp_label = []
            for n in range(0,8):
                tmp_train.append(record[n])
            for n in range(8,11):
                tmp_label.append(record[n])
            trainList[bat_index][pit_index].append(tmp_train)
            labelList[bat_index][pit_index].append(tmp_label)


train_size = len(trainList[0][0][0]) #학습시킬 속성 차원 수
label_size = len(labelList[0][0][0]) #결과 차원 수



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

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=logits))
train_step = tf.train.GradientDescentOptimizer(1e-3).minimize(loss)

#새로운 정확도 판정 방법 필요
#correct_prediction = tf.equal(tf.argmax(y_pred, 1), tf.argmax(y, 1))
#accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

for batter_index in range(batter_class_num):
    for pither_index in range(pitcher_class_num):
        t_size = len(trainList[batter_index][pither_index])
        dataset = tf.data.Dataset.from_tensor_slices((trainList[batter_index][pither_index],labelList[batter_index][pither_index]))
        dataset = dataset.repeat()
        dataset = dataset.shuffle(len(trainList[batter_index][pither_index])*2)
        dataset = dataset.batch(32)
        iterator = dataset.make_initializable_iterator()
        next_element = iterator.get_next()

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            sess.run(iterator.initializer)
            saver = tf.train.Saver()
            print('[',batter_index,']','[',pither_index,'] learning start !')
            for i in range(t_size*8):
                x_data, y_data = sess.run(next_element)
                if i == 0 or i == (t_size*8)-1:
                    loss_print = sess.run(loss, feed_dict={x: x_data, y: y_data, keep_prob: 1.0})
                    predict_y = sess.run(y_pred, feed_dict={x:x_data, keep_prob: 1.0})
                    print("predict : ",predict_y[0]," , real : ",y_data[0])
                    print("step : %d, 손실 함수(loss): %f" % (i, loss_print))
                sess.run(train_step, feed_dict={x: x_data, y: y_data, keep_prob: 0.9})
            print('[',batter_index,']','[',pither_index,'] learning end !\n\n')
            saver.save(sess, './models/'+str(batter_index)+'-'+str(pither_index)+'.ckpt')
