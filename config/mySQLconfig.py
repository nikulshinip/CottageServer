import mysql.connector

class SqlConnect():
	"""управление соединением с базой данных"""
	def __init__(self):
		userName = 'YouUsername'
		password = 'YouPassword'
		host = 'localhost'
		dbName = 'cottage'
		self.connect = mysql.connector.connect(user=userName, password=password, host=host, database=dbName)
		self.cursor = self.connect.cursor()
	def close(self):
		self.cursor.close()
		self.connect.close()