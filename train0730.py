# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import MySQLdb
from sshtunnel import SSHTunnelForwarder

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

def transPdFrame(tuple):
	tmp = np.array(tuple)
	return pd.DataFrame(tmp)

def Num(arr2):
    print(len(arr2))
    horse, jokey = np.hsplit(arr2, [1])
    horse2= np.ravel(horse.T)
    jokey2= np.ravel(jokey.T)
    horse_zisyo = np.empty((0,2), float)
    jokey_zisyo = np.empty((0,2), float)

    for i in horse2:
        zisyo =  np.array([])
        zisyo = np.append(zisyo, i)
        zisyo = np.append(zisyo, (len(np.where(horse2==i)[0])*1.0) / (len(arr2)*1.0))
        horse_zisyo = np.append(horse_zisyo, np.array([zisyo]), axis=0)
    for i in jokey2:
        zisyo2 =  np.array([])
        zisyo2 = np.append(zisyo2, i)
        zisyo2 = np.append(zisyo2, (len(np.where(jokey2==i)[0])*1.0) / (len(arr2)*1.0))
        jokey_zisyo = np.append(jokey_zisyo, np.array([zisyo2]), axis=0)

    return horse_zisyo, jokey_zisyo

if __name__ == "__main__":
	server = StartSSHSession()
	connection = GetConnection(server.local_bind_port)
	cursor = connection.cursor()
	#score:３位まで１、それ以外０
	#sql = "SELECT tkd.score, tkd.rank, tkd.horse_name_id, mh.horse_name, tkd.jockey_id, mj.jockey_name "
	#sql += "FROM t_keiba_data AS tkd "
	#sql +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
	#sql +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id"


	sql = "SELECT * FROM t_keiba_info"
	try:
		cursor.execute(sql)
		test_data = cursor.fetchall()
		#for row in test_data:
		#	print(row)

	except MySQLdb.Error as e:
		print('MySQLdb.Error: ', e)
		StopSSHSession(server, connection)

	sql = "SELECT tkd.score, tkd.rank, tkd.horse_name_id, mh.horse_name, tkd.jockey_id, mj.jockey_name "
	sql += "FROM t_keiba_data AS tkd "
	sql +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
	sql +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id"
	try:
		cursor.execute(sql)
		train_data = cursor.fetchall()
		#for row in train_data:
		#print(row)

	except MySQLdb.Error as e:
		print('MySQLdb.Error: ', e)
		StopSSHSession(server, connection)


	horse_name = "マイネルディアベル"
	sql = "SELECT tkd.rank FROM t_keiba_data AS tkd WHERE tkd.horse_name = 'マイネルディアベル' "
	try:
		cursor.execute(sql)
		horse_data = cursor.fetchall()
		#for row in test_data:
		#	print(row)

	except MySQLdb.Error as e:
		print('MySQLdb.Error: ', e)
		StopSSHSession(server, connection)

	connection.commit()
	StopSSHSession(server, connection)

	#train by NeuralNet
	test_data = transPdFrame(test_data)
	train_data = transPdFrame(train_data)
	print(train_data)
	print("horse_data")
	print(horse_data)

	test = M.getValueRace(test_data,9,201704020211)
	print("test")
	print(test)

	#tmp_str = " == " + str(test.iloc[0,1])
	print(train_data.iloc[:,2])
	print(test.iloc[1,1])

	tmp_horse = train_data[train_data[2].isin(str(test.iloc[0,1]))]
	print(tmp_horse)


	vRate_data = test[[1,5]]
	h_vRate, j_vRate = Num(vRate_data)
