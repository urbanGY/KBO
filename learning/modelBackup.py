import tensorflow as tf
import csv
import vs
#오재원 김성민
def decode(j,k,l):
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
    for x in range(0,2): #base - 1 -> o
        if x == l:
            list.append(1)
        else :
            list.append(0)
    return list

def get_batter_class(name): #batter class 찾는 함수
    batter_url = "C:\\Users\\sfsfk\\Desktop\\develope\\softWareProject\\BaseballPredict\\KBO\\clustering\\clusterOutput\\classification_batter_2.csv"
    # batter_url = "../clustering/clusterOutput/classification_batter_2.csv"
    batter_class_f = open(batter_url, mode='rt',newline='')#기존 train file 가져옴
    batter_class_reader = list(csv.reader(batter_class_f))#타자 class dictionary
    batter_class_num = len(batter_class_reader[0])
    for line in batter_class_reader:
        for i in range(batter_class_num):
            if line[i] == name:
                print("*** batter_class -> ",i)
                return i
    print("*** batter_class fail -> -2")
    return -2

def get_pitcher_class(name): #batter class 찾는 함수
    pitcher_url = "C:\\Users\\sfsfk\\Desktop\\develope\\softWareProject\\BaseballPredict\\KBO\\clustering\\clusterOutput\\classification_pitcher_2.csv"
    # pitcher_url = "../clustering/clusterOutput/classification_pitcher_2.csv"
    pitcher_class_f = open(pitcher_url, mode='rt',newline='')#기존 train file 가져옴
    pitcher_class_reader = list(csv.reader(pitcher_class_f))#투수 class dictionary
    pitcher_class_num = len(pitcher_class_reader[0])
    for line in pitcher_class_reader:
        for i in range(pitcher_class_num):
            if line[i] == name:
                print("*** pitcher_class -> ",i)
                return i
    print("*** pitcher_class fail -> -2")
    return -2

def get_batter_team(name):
    _url = "C:\\Users\\sfsfk\\Desktop\\develope\\softWareProject\\BaseballPredict\\KBO\\crollingPart\\teamList\\batter\\"
    # _url = "../crollingPart/teamList/batter/"
    teamName = ['doosanbears','kiatigers','kiwoomheroes','ktwiz','lgtwins','lottegiants','ncdinos','samsunglions','hanwhaeagles','skwyverns']
    for team in teamName:
        team_f = open(_url + team + '_b.csv', 'rt')
        team_reader = csv.reader(team_f)
        for line in team_reader:
            if line[0] == name:
                return team
    return '-1'

def get_batter_birth(name):
    _url = "C:\\Users\\sfsfk\\Desktop\\develope\\softWareProject\\BaseballPredict\\KBO\\crollingPart\\teamList\\batter\\"
    # _url = "../crollingPart/teamList/batter/"
    teamName = ['doosanbears','kiatigers','kiwoomheroes','ktwiz','lgtwins','lottegiants','ncdinos','samsunglions','hanwhaeagles','skwyverns']
    for team in teamName:
        team_f = open(_url + team + '_b.csv', 'rt')
        team_reader = csv.reader(team_f)
        for line in team_reader:
            if line[0] == name:
                return line[1]
    return '-1'

def getRealHit(batter_name, pitcher_name):
    _url = "C:\\Users\\sfsfk\\Desktop\\develope\\softWareProject\\BaseballPredict\\KBO\\playerInfo\\test\\"
    # _url = "../playerInfo/test/"
    batter_class = get_batter_class(batter_name)
    pitcher_class = get_pitcher_class(pitcher_name)
    team = get_batter_team(batter_name)
    print('batter_class : ',batter_class)
    print('pitcher_class : ',pitcher_class)
    print('team : ',team)
    player_f = open(_url + team + "\\"+ batter_name +'.csv', 'rt')
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
    return str(round(hit,3)), str(round(go,3))

def runModel(input, checker):
    train_size = 8
    label_size = 3

    x = tf.placeholder("float", [None,train_size])
    y = tf.placeholder("float", [None,label_size])
    keep_prob = tf.placeholder(tf.float32)
    if checker == 1:
        runModel.w_1 = tf.Variable(tf.truncated_normal(shape=[train_size, train_size*2], stddev=5e-2), name='weight_1')
        runModel.b_1 = tf.Variable(tf.constant(0.1, shape=[train_size*2]), name='bias_1')
    h_fc1 = tf.nn.relu(tf.matmul(x, runModel.w_1) + runModel.b_1)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    if checker == 1:
        runModel.w_2 = tf.Variable(tf.truncated_normal(shape=[train_size*2, train_size*3], stddev=5e-2), name='weight_2')
        runModel.b_2 = tf.Variable(tf.constant(0.1, shape=[train_size*3]), name='bias_2')
    h_fc2 = tf.nn.relu(tf.matmul(h_fc1_drop, runModel.w_2) + runModel.b_2)
    h_fc2_drop = tf.nn.dropout(h_fc2, keep_prob)

    if checker == 1:
        runModel.w_3 = tf.Variable(tf.truncated_normal(shape=[train_size*3, train_size*2], stddev=5e-2), name='weight_3')
        runModel.b_3 = tf.Variable(tf.constant(0.1, shape=[train_size*2]), name='bias_3')
    h_fc3 = tf.nn.relu(tf.matmul(h_fc2_drop, runModel.w_3) + runModel.b_3)
    h_fc3_drop = tf.nn.dropout(h_fc3, keep_prob)

    if checker == 1:
        runModel.w_4 = tf.Variable(tf.truncated_normal(shape=[train_size*2, label_size], stddev=5e-2), name='weight_4')
        runModel.b_4 = tf.Variable(tf.constant(0.1, shape=[label_size]), name='bias_4')
    logits = tf.matmul(h_fc3_drop,runModel.w_4)+runModel.b_4
    y_pred = tf.nn.softmax(logits)

    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=logits))
    train_step = tf.train.GradientDescentOptimizer(1e-3).minimize(loss)



    batter_name = input[0]
    pitcher_name = input[1]
    inning = int(input[2])
    out = int(input[3])
    base = int(input[4])
    print('in modelBackup... ',batter_name,pitcher_name,inning,out,base)

    batter_index = get_batter_class(batter_name) #batter
    pitcher_index = get_pitcher_class(pitcher_name) #pitcher
    input_x = decode(inning, out, base) #임의로 입력
    print('input x : ',input_x)
    _url = "C:\\Users\\sfsfk\\Desktop\\develope\\softWareProject\\BaseballPredict\\KBO\\learning\\models\\"
    # _url = "./models/"
    with tf.Session() as sess:
        print('checker : ',checker)
        if checker == 1:
            print('first time!!!!')
            runModel.saver = tf.train.Saver()
        runModel.saver.restore(sess, _url +str(batter_index)+'-'+str(pitcher_index)+'.ckpt')

        tmp = []
        tmp.append(input_x)
        pred = sess.run(y_pred, feed_dict={x:tmp, keep_prob:1.0}) #결과

        hit = pred[0][1]
        go = 1 - pred[0][0] #예측 부분

        vs_hit, vs_go = vs.GetData(batter_name,get_batter_birth(batter_name),pitcher_name)
        if(vs_hit != 0.0):
            hit = (hit *0.85)+(vs_hit*0.15)
            go = (go *0.85)+(vs_go*0.15)

        output = []
        output.append(str(round(hit, 3))) #예측 타율
        output.append(str(round(go, 3))) #예측 출루율

        real_hit, real_go = getRealHit(batter_name,pitcher_name)
        output.append(real_hit)
        output.append(real_go)
        return output
