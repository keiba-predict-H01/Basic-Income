# -*- coding: utf-8 -*-
import sys
import numpy as np
import pandas as pd
import matplotlib as plt
import MySQLdb
from sshtunnel import SSHTunnelForwarder
from chainer import cuda,Variable,FunctionSet,optimizers
import chainer.functions as F
import dataMolding as M

#セッション開始？、あすかのコード参照
def StartSSHSession():
	server = SSHTunnelForwarder(
			('yuruhuwa-bourg.sakura.ne.jp', 22),
			ssh_username="yuruhuwa-bourg",
			ssh_password="eh4uat56gu",
			remote_bind_address=('mysql541.db.sakura.ne.jp', 3306)
			)

	server.start()
	return server

#あすかのコード参照
def GetConnection(port):
	connection = MySQLdb.connect(
		host='127.0.0.1',
		port=port,
		user='yuruhuwa-bourg',
		passwd='1q2w3e4r',
		db='yuruhuwa-bourg_keiba',
		charset='utf8')
		#charset=shift_jis)
	return connection

#あすかのコード参照
def StopSSHSession(server, connection):
	connection.close()
	server.stop()

#データをDBから取ってくる。あすかのコード参照
def getDataFromDB(sql):
	server = StartSSHSession()
	connection = GetConnection(server.local_bind_port)
	cursor = connection.cursor()

	try:
		cursor.execute(sql)
		data = cursor.fetchall()
		#for row in test_data:
		#	print(row)

	except MySQLdb.Error as e:
		print('MySQLdb.Error: ', e)
		StopSSHSession(server, connection)

	connection.commit()
	StopSSHSession(server,connection)

	return data

#Pandas型に変換
def transPdFrame(tuple):
	tmp = np.array(tuple)
	return pd.DataFrame(tmp)

#ニューラルネットワークの準伝搬（学習）、trainはドロップアウトの有無
def forward(x,y,model,train = False):
	x, t = Variable(x),Variable(y)
	h1 = F.dropout(F.sigmoid(model.l1(x)), train=train)
	h2 = F.dropout(F.sigmoid(model.l2(h1)),train=train)
	y = model.l3(h2)
	return F.mean_squared_error(y,t)

 #学習したモデルにテストデータを入力し、最終結果を出す
def test_output(x,model,train = False):
	x = Variable(x)
	h1 = F.dropout(F.sigmoid(model.l1(x)), train=train)
	h2 = F.dropout(F.sigmoid(model.l2(h1)),train=train)
	y = model.l3(h2)
	return y

#上位3位の馬を抽出
def selectTop3Horse(result,horseList,num=3):
	resultMat = np.hstack((result,testHorseName))
	sortMat = np.sort(resultMat,axis =0)
	print(sortMat)
	return sortMat[0:num]

if __name__ == "__main__":

	#順位を知りたいレースのIDを指定
	testUrl = '201705050412'

	#訓練データ
	sql = "SELECT tkd.horse_year,tkd.basis_weight FROM t_keiba_data_result AS tkd "
	train = np.array(getDataFromDB(sql))
	#horse_data = transPdFrame(horse_data)

	#教師データ
	sql = "SELECT tkd.score FROM t_keiba_data_result AS tkd "
	target = np.array(getDataFromDB(sql))

	#馬名取得
	sql = "SELECT * FROM m_horse"
	horse_name = np.array(getDataFromDB(sql))
	#print(horse_name)

	#テストデータ
	sql = "SELECT tkd.horse_year,tkd.basis_weight FROM t_keiba_predata AS tkd WHERE tkd.url = " + testUrl
	#sql += "WHERE t_keiba_predata.key = hogehoge"
	#sql += "WHERE t_keiba_info.date = '201704020211' "
	#test_data = transPdFrame(getDataFromDB(sql))
	test = np.array(getDataFromDB(sql))
	print(test)

	#テストデータの馬名
	sql = "SELECT m_horse.horse_name FROM m_horse WHERE m_horse.horse_id IN ( SELECT tkd.horse_name_id FROM t_keiba_predata AS tkd WHERE tkd.url = " + testUrl + " )"
	testHorseName = getDataFromDB(sql)
	print(testHorseName)

	#パラメタの正則化
	train = M.normalization(pd.DataFrame(train),0)
	train = M.normalization(pd.DataFrame(train),1)
	#train = M.normalization(pd.DataFrame(train),2)

	test = M.normalization(pd.DataFrame(test),0)
	test = M.normalization(pd.DataFrame(test),1)
	#test = M.normalization(pd.DataFrame(test),2)

	#計算高速化のためフォーマット変換
	train = np.array(train,dtype=np.float32)
	target = np.array(target,dtype=np.float32)
	test = np.array(test,dtype=np.float32)

	#学習モデルの作成
	n_units = 5
	model = FunctionSet(	l1=F.Linear(2, n_units),
							l2=F.Linear(n_units, n_units),
							l3=F.Linear(n_units, 1))
	#最適化手法のセット
	optimizer = optimizers.Adam()　#最適化手法の決定、AdamまたはSGD推奨
	optimizer.setup(model)　#モデルのセットアップ

	#学習
	n_epoch = 50　#学習回数
	batchsize = 50 #１回の勾配計算にかけるデータ数

	train_loss = []
	train_acc = []

	for epoch in range(1,n_epoch+1):
		print("epoch",epoch)
		perm = np.random.permutation(train.shape[0])
		sum_accuracy = 0
		sum_loss = 0

	#訓練データの学習
		for i in range(0,train.shape[0],batchsize):
			x_batch = train[perm[i:i+batchsize]]
			y_batch = target[perm[i:i+batchsize]]

			optimizer.zero_grads()#勾配初期化
			loss = forward(x_batch,y_batch,model)#準伝搬
			loss.backward()#逆伝搬、勾配計算
			optimizer.update()#バイアス更新
			train_loss.append(loss.data)#教師信号との誤差算出
			sum_loss += loss.data * batchsize
		print("\ttest_mean loss:",sum_loss / train.shape[0])

	#学習終了

	#テストデータで結果出力
	#result = []
	#for i in range(0,test.shape[0]):
	#	tmp = test_output(test[i],model)
	#	result.append(tmp)
	result = test_output(test,model)
	result = result.data
	print(result,result.shape)

	#学習結果表示
	resultMat = np.hstack((result,testHorseName))
	print(resultMat)

	#上位３位まで摘出※動作怪しいfrom1227から未修正ß
	#resultMat = np.sort(resultMat,axis=0)
	#print(resultMat)
	#higer3Horse = resultMat[0:3,:]
	#print(higer3Horse)
	print("上位3位:")
	print(selectTop3Horse(result,testHorseName,3))
