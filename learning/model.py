import tensorflow as tf

batter_class_num = 10
pitcher_class_num = 6

batter_index = 0
pitcher_index = 0

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
    saver.restore(sess, './models/'+str(batter_index)+'-'+str(pitcher_index)+'.ckpt')
    pred = sess.run(y_pred, feed_dict={x:x_data}) #결과


#한화 sk 타자 투수 정보 수집, 기존 체계에 추가시키기
#2018, 2019자료 사용
#입력 데이터 어떻게 받아올지 생각
#받아 온 데이터 숫자만큼 세션 활성화 시켜서 결과 뽑아내기
#뽑아 낸 결과 어떻게 웹 페이지로 보낼 지 생각
#결과 검증으 어떻게 할지 생각..
