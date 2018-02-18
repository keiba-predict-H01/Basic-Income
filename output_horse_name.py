# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib as plt
import MySQLdb
from sshtunnel import SSHTunnelForwarder

from chainer import cuda,Variable,FunctionSet,optimizers
import chainer.functions as F

import dataMolding as M

def StartSSHSession():
	server = SSHTunnelForwarder(
			('yuruhuwa-bourg.sakura.ne.jp', 22),
			ssh_username="yuruhuwa-bourg",
			ssh_password="eh4uat56gu",
			remote_bind_address=('mysql541.db.sakura.ne.jp', 3306)
			)

	server.start()
	return server


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

def StopSSHSession(server, connection):
	connection.close()
	server.stop()

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

def transPdFrame(tuple):
	tmp = np.array(tuple)
	return pd.DataFrame(tmp)

def forward(x,y,model,train = False):
	x, t = Variable(x),Variable(y)
	h1 = F.dropout(F.sigmoid(model.l1(x)), train=train)
	h2 = F.dropout(F.sigmoid(model.l2(h1)),train=train)
	y = model.l3(h2)
	return F.mean_squared_error(y,t)

def test_output(x,model,train = False):
	x = Variable(x)
	h1 = F.dropout(F.sigmoid(model.l1(x)), train=train)
	h2 = F.dropout(F.sigmoid(model.l2(h1)),train=train)
	y = model.l3(h2)
	return y

if __name__ == "__main__":
	#訓練データ
	sql = "SELECT tkd.horse_year,tkd.basis_weight,tkd.popularity FROM t_keiba_data_result AS tkd "
	train = np.array(getDataFromDB(sql))
	#horse_data = transPdFrame(horse_data)

	#教師データ
	sql = "SELECT tkd.score FROM t_keiba_data_result AS tkd "
	target = np.array(getDataFromDB(sql))

	#馬名取得
	sql = "SELECT * FROM m_horse"
	horse_name = np.array(getDataFromDB(sql))
	print(horse_name)

	pd = pd.DataFrame(horse_name)
	pd.to_csv("horse_name.csv",index=False)
