# -*- coding: utf-8 -*-i

#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import fetch_mldata
from chainer import cuda,Variable,optimizers
import chainer.functions as F
import sys

batchsize = 100
n_epoch = 10
n_units = 10

def forward(x_data, y_data, train = True):
	x, t = Variable(x_data),Variable(y_data)
	h1 = F.dropout(F.sigmoid(model.l1(x)), train=train)
	h2 = F.dropout(F.sigmoid(model.l2(h1)),train=train)
	y = model.l3(h2)
	return F.softmax_cross_entropy(y,t), F.accuracy(y,t)


'''
print("fetch MNIST dataset")
mnist = fetch_mldata('MNIST original')
mnist.data = mnist.data.astype(np.float32);
mnist.data /= 255
mnist.target = mnist.target.astype(np.int32)
'''

N = 100
x_train, x_test = np.split(mnist.data,[N])
y_train, y_test = np.split(mnist.target, [N])
N_test = y_test.size

model = FunctionSet(	l1=F.Linear(3, n_units),
						l2=F.Linear(n_units, n_units),
						l3=F.Linear(n_units, 1))

optimizer = optimizers.Adam()
optimizer.setup(model.collect_parameters())

train_loss = []
train_acc = []
test_loss = []
test_acc = []

l1_w = []
l2_w = []
l3_w = []

for epoch in xrange(1,n_epoch+1):
	print('epoch',epoch)
	#training
	#exchange random
	perm = np.random.permutation(N)
	sum_accuracy = 0
	sum_loss = 0

	#training each batchsize
	for i in xrange(0,N,batchsize):
		x_batch = x_train[perm[i:i+batchsize]]
		y_batch = y_train[perm[i:i+batchsize]]

		#勾配を初期化
		optimizer.zero_grads()
		#順伝搬で誤差と精度算出
		loss ,acc = forward(x_batch,y_batch)
		#誤差逆伝搬で勾配を計算
		loss.backward()
		optimizer.update()

		train_loss.append(loss.data)
		train_acc.append(acc.data)

		sum_loss += float(cuda.to_cpu(loss.data)) * batchsize
		sum_accuracy += float(cuda.to_cpu(acc.data)) * batchsize


	print('train mean loss = {}, accuracy = {}'.format(sum_loss /N ,sum_accuracy / N))

	#evaluation
	#テストデータから誤差と正解精度を算出、汎化性能を確認
	sum_accuracy = 0
	sum_loss = 0
	for i in xrange(0,N_test,batchsize):
		x_batch = x_test[i:i+batchsize]
		y_batch = y_test[i:i+batchsize]

		#順伝搬
		loss,acc = forward(x_batch,y_batch, train = False)

		test_loss.append(loss.data)
		test_acc.append(acc.data)
		sum_loss += float(cuda.to_cpu(loss.data)) * batchsize
		sum_accuracy += float(cuda.to_cpu(acc.data)) * batchsize

	print('test mean loss = {}, accracy = {}'.format(sum_loss /N_test,sum_accuracy / N_test))

	#学習したパラメータを保存
	l1_w.append(model.l1.W)
	l2_w.append(model.l2.W)
	l3_w.append(model.l3.W)

print('finish learning ... ')
