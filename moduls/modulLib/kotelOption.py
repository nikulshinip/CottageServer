import sys, mysql.connector
sys.path.append('../../config')
import mySQLconfig

class Opt() :
	"""класс дополнительных параметров управления котлом"""
	def __init__(self, id) :
		self.id=id			#id опции
		zapros = "SELECT `title` FROM `kotel_addOptions` WHERE `id`="+str(self.id)
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros)
		row = dbconnect.cursor.fetchone()
		dbconnect.close()
		self.title = row[0]	#коментарий опции
		self.state = 0
	def getSQL(self) :
		"""высчитать опцию из базы данных"""
		zapros = "SELECT `state` FROM `kotel_addOptions` WHERE `id`="+str(self.id)
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros)
		row = dbconnect.cursor.fetchone()
		dbconnect.close()
		self.state = row[0]
		return self.state
	def setSQL(self, state) :
		"""записать значение в базу данных(использовать для аварийных случаев)"""
		zapros = "UPDATE `kotel_addOptions` SET `state`=%s WHERE `id`=%s"
		data = (state, self.id)
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros, data)
		dbconnect.connect.commit()
		dbconnect.close()
		self.state = state
		return True