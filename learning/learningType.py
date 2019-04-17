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

train_size = len(trainList[0])
label_size = len(labelList[0])

dataset = tf.data.Dataset.from_tensor_slices((trainList,labelList))
dataset = dataset.repeat()
dataset = dataset.shuffle(20000)
dataset = dataset.batch(512)
iterator = dataset.make_initializable_iterator()
next_element = iterator.get_next()

x = tf.placeholder("float", [None,train_size])
y = tf.placeholder("float", [None,label_size])
w = tf.Variable(tf.truncated_normal(shape=[train_size, label_size]), name='weight')
b = tf.Variable(tf.random_normal(shape=[label_size]), name='bias')
logits = tf.matmul(x,w)+b
y_pred = tf.nn.softmax(logits)

loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=logits))
train_step = tf.train.RMSPropOptimizer(1e-3).minimize(loss)

correct_prediction = tf.equal(tf.argmax(y_pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    sess.run(iterator.initializer)

    for i in range(120001):
        x_data, y_data = sess.run(next_element)
        if i%500 == 0:
            train_accuracy = sess.run(accuracy, feed_dict={x: x_data, y: y_data})
            loss_print = sess.run(loss, feed_dict={x: x_data, y: y_data})
            predict_y = sess.run(tf.argmax(y_pred,1), feed_dict={x:x_data})
            print("predict : ",predict_y,"real value : ",y_data)
            print("step : %d, 트레이닝 데이터 정확도: %f, 손실 함수(loss): %f" % (i, train_accuracy, loss_print))
        sess.run(train_step, feed_dict={x: x_data, y: y_data})
