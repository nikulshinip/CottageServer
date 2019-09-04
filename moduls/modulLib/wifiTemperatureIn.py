import sys, mysql.connector, os, socket
sys.path.append('../../config')
import mySQLconfig

class WiFiTempIn() :
	"""WiFi входной сигнал температуры"""
	def __init__(self, id) :
		self.id = id										#id датчика в базе данных
		zapros = "SELECT `address`, `title` FROM `temperatur` WHERE `id`="+str(self.id)
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros)
		row = dbconnect.cursor.fetchone()
		dbconnect.close()
		self.addres = row[0][:13]							#адрес датчика
		self.sensor = row[0][13:]
		self.title = row[1]									#коментарий к датчику
		self.state = 9999									#первоначальное состояние
	def getState(self) :
		"""взять температуру с датчика для использования в программе"""
		try:
			sock = socket.socket()
			sock.connect((self.addres, 80))
			sock.send(self.sensor.encode('utf-8'))
			st = sock.recv(5)
			self.state = round(float(st.strip()), 1)
			sock.close()
		except:
			if sock :
				sock.close()
			self.state = 9999
		return self.state
	def getStateToSQL(self) :
		"""взять температуру с датчика и положить в базу данных"""
		state = self.getState()
		zapros = "UPDATE `temperatur` SET `temperatur`=%s WHERE `id`=%s"
		data = (state, self.id)
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros, data)
		dbconnect.connect.commit()
		dbconnect.close()
		return state