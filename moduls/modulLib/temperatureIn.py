import sys, mysql.connector, os
sys.path.append('../../config')
import mySQLconfig

class TempIn() :
	"""простой входной сигнал температуры"""
	def __init__(self, id) :
		self.id = id										#id датчика в базе данных
		zapros = "SELECT `address`, `title` FROM `temperatur` WHERE `id`="+str(self.id)
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros)
		row = dbconnect.cursor.fetchone()
		dbconnect.close()
		self.addres = "/mnt/1wire/"+row[0]+"/temperature"	#адрес датчика
		self.title = row[1]									#коментарий к датчику
		self.state = 9999									#первоначальное состояние
	def getState(self) :
		"""взять температуру с датчика для использования в программе"""
		try:
			file = open(self.addres, "r", encoding="utf-8")
			st = file.read()
			self.state = round(float(st.strip()), 1)
		except:
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