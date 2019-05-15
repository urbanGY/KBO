import tensorflow as tf
import csv

def getResult(y):
    if y[0] is '1':
        return '아웃'
    if y[1] is '1':
        return '안타'
    if y[2] is '1':
        return '볼넷'

def showSplitClass(b, p, list, clas):
    splitClass = []
    for i in range(b):
        v = []
        for j in range(p):
            tmp = []
            v.append(tmp)
        splitClass.append(v)
    for i in range(len(list)):
        splitClass[clas[i][0]][clas[i][1]].append(list[i])
    for i in range(b):
        for j in range(p):
            print('b : ',i,' , p : ',j)
            for x in splitClass[i][j]:
                print(x)
            print('')

def showLimit(b, p, list):
    for i in range(b):
        for j in range(p):
            print('b : ',i,' , p : ',j)
            hit_a = 0
            go_a = 0
            count_a = 0

            hit_b = 0
            go_b = 0
            count_b = 0

            hit_c = 0
            go_c = 0
            count_c = 0
            for x in list[i][j]:
                if x[2] == '안타':
                    hit_a += x[0]
                    go_a += x[1]
                    count_a += 1
                if x[2] == '볼넷':
                    hit_b += x[0]
                    go_b += x[1]
                    count_b += 1
                if x[2] == '아웃':
                    hit_c += x[0]
                    go_c += x[1]
                    count_c += 1
            if count_a is 0 or count_b is 0 or count_c is 0:
                continue
            print('안타일 때 예측 타율 평균 : ',hit_a/count_a,', 예측 출루 평균 : ',go_a/count_a)
            print('볼넷일 때 예측 타율 평균 : ',hit_b/count_b,', 예측 출루 평균 : ',go_b/count_b)
            print('아웃일 때 예측 타율 평균 : ',hit_c/count_c,', 예측 출루 평균 : ',go_c/count_c)
            print('')




x_data = []
y_data = []
classifier = []
player_data = open('../playerInfo/test/doosanbears/오재원.csv', 'rt')
player_reader = csv.reader(player_data)

for record in player_reader:
    if record[0] == '3' or record[22] == '-1' or record[24] == '-1': #둘중 하나만 -1이면 list에 안가져옴
        continue
    tmp_train = []
    tmp_label = []
    tmp_class = []
    for n in range(0,18):
        tmp_train.append(record[n])
    for n in range(18,21):
        tmp_label.append(record[n])
    tmp_class.append(int(record[22]))
    tmp_class.append(int(record[24]))
    x_data.append(tmp_train)
    y_data.append(tmp_label)
    classifier.append(tmp_class)


train_size = len(x_data[0])
label_size = len(y_data[0])

batter_class_num = 10
pitcher_class_num = 6

x = tf.placeholder("float", [None,train_size])
y = tf.placeholder("float", [None,label_size])
w = tf.Variable(tf.truncated_normal(shape=[train_size, label_size], stddev=5e-2), name='weight')
b = tf.Variable(tf.constant(0.1, shape=[label_size]), name='bias')

logits = tf.matmul(x,w)+b
y_pred = tf.nn.softmax(logits)
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=logits))
train_step = tf.train.GradientDescentOptimizer(1e-3).minimize(loss)

saver = tf.train.Saver()

with tf.Session() as sess:
    splitClass = []
    for i in range(batter_class_num):
        v = []
        for j in range(pitcher_class_num):
            tmp = []
            v.append(tmp)
        splitClass.append(v)

    text_list = []
    for i in range(len(x_data)):
        batter_index = classifier[i][0]
        pitcher_index = classifier[i][1]
        saver.restore(sess, './models/'+str(batter_index)+'-'+str(pitcher_index)+'.ckpt')
        #print(sess.run(w)) 모델별로 다른 w값 가짐을 확인
        tmp = []
        tmp.append(x_data[i])
        pred = sess.run(y_pred, feed_dict={x:tmp}) #결과
        hit = pred[0][1]
        go = 1 - pred[0][0]
        block = []
        block.append(hit)
        block.append(go)
        block.append(getResult(y_data[i]))
        splitClass[batter_index][pitcher_index].append(block)
        s = '예측 타율 : '+str(round(hit, 3))+', 예측 출루율 : '+str(round(go,3))+' -> 실제 결과 : '+getResult(y_data[i])
        text_list.append(s)
    showSplitClass(batter_class_num, pitcher_class_num, text_list, classifier)
    #showLimit(batter_class_num,pitcher_class_num,splitClass)

        #print("예측 타율 : %.3f , 예측 출루율 : %.3f  -> 실제결과 : %s" % (hit,go,getResult(y_data[i])))

        #print(pred,' - ',y_data[i])약식 표현


#한화 sk 타자 투수 정보 수집, 기존 체계에 추가시키기
#2018, 2019자료 사용
#입력 데이터 어떻게 받아올지 생각
#받아 온 데이터 숫자만큼 세션 활성화 시켜서 결과 뽑아내기
#뽑아 낸 결과 어떻게 웹 페이지로 보낼 지 생각
#결과 검증으 어떻게 할지 생각..
