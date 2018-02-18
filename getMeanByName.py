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

def getDataFromDB(sql):
	server = StartSSHSession()
	connection = GetConnection(server.local_bind_port)
	cursor = connection.cursor()

	try:
		cursor.execute(sql)
		data = cursor.fetchall()

	except MySQLdb.Error as e:
		print('MySQLdb.Error: ', e)
		StopSSHSession(server, connection)

	connection.commit()
	StopSSHSession(server,connection)

	return data

def transPdFrame(tuple):
	tmp = np.array(tuple)
	return pd.DataFrame(tmp)

if __name__ == "__main__":

	sql = "SELECT tkd.rank, tkd.horse_name_id, mh.horse_name, tkd.jockey_id, mj.jockey_name "
	sql += "FROM t_keiba_data AS tkd "
	sql +=	"LEFT JOIN m_horse as mh ON tkd.horse_name_id = mh.horse_id "
	sql +=	"	LEFT JOIN m_jockey as mj ON tkd.jockey_id = mj.jockey_id"
	#horse_data = transPdFrame(getDataFromDB(sql))
	horse_data = np.array(getDataFromDB(sql),dtype=object)

	sql = "SELECT * FROM t_keiba_info "
	#sql += "WHERE t_keiba_info.date = '201704020211' "
	#test_data = transPdFrame(getDataFromDB(sql))
	test_data = np.array(getDataFromDB(sql),dtype=object)

	print(test_data,test_data.shape,test_data.dtype)
	print(horse_data,horse_data.shape,horse_data.dtype)
	#horse_data = transPdFrame(horse_data)
	mean = []
	for i in range(len(test_data)):
		tmp = np.array(np.where(horse_data[:,1] == test_data[i,1]),dtype=int)
		#print(tmp,tmp.shape,tmp.size)
		print(i,":",horse_data[tmp,2])
		if tmp.shape[1] != 0:
			mean.append(np.mean(horse_data[tmp,0]))
		else:
			mean.append(0)

	print(mean,len(mean))
	print(len(test_data))

	print("finish")
