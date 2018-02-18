# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import MySQLdb
from sshtunnel import SSHTunnelForwarder

class ConnectHttpSession:
	self.sshServerAddress = 'yuruhuwa-bourg.sakura.ne.jp'
	self.sshUsernName = "yuruhuwa-bourg"
	self.sshPassword = "eh4uat56gu"
	self.remotebindAddress = 'mysql541.db.sakura.ne.jp'
	self.sshServerport = 22
	self.sshConnectPort = 3306
	self.host = '127.0.0.1'
	self.userPassword = '1q2w3e4r'
	self.DataBase = 'yuruhuwa-bourg_keiba'

	def __init__(self):
		self.server = SSHTunnelForwarder(
			(self.sshServerport, self.sshServerport),
			self.sshUserName,
			self.sshPassWord,
			remote_bind_address=(self.remotebindAddress, self.sshConnectPort)
		)
		self.server.start()

	def GetConnection(self):
		self.connection = MySQLdb.connect(
			host = self.host,
			port = server.local_bind_port
			passwd = userPassword,
			db = self.DataBase,
			charset = 'utf8'
		)

	def StopSSHSession(self):
		self.connection.close()
		self.server.stop()

	def getData(self,sql):
		self.cursor = connection.cursor()

		try:
			self.cursor.execute(sql)
			self.data = self.cursor.fetchall()

		except MySQLdb.Error as e :
			print('MySQLdb.Error: ', e)
			self.StopSSHSession()
		self.connection.comit()
		self.StopSSHSession()

		return self.data
