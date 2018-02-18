# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import MySQLdb
from sshtunnel import SSHTunnelForwarder

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


	connection.commit()
	StopSSHSession(server, connection)

	#train by NeuralNet
	test = pd.DataFrame(test_data)
	train = pd.DataFrame(train_data)
