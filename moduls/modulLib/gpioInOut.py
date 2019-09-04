import sys, mysql.connector
import RPi.GPIO as GPIO
sys.path.append('../../config')
import mySQLconfig
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

class Din() :
	"""простой входной сигнал"""
	def __init__(self, id):
		self.id = id					#id сигнала
		zapros = "SELECT `pin`, `title` FROM `kotel_din` WHERE `din`="+str(self.id)
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros)
		row = dbconnect.cursor.fetchone()
		dbconnect.close()		
		self.pin = int(row[0])			#пин на малине
		self.title = row[1]				#описание сигнала
		GPIO.setup(self.pin, GPIO.IN)	#инициализация GPIO
		self.status = 0					#первоначальное положение
	def getState(self):
		"""Определяет положение сигнала"""
		status = GPIO.input(self.pin)
		status = int(status)
		self.status = status
		return status
	def getStateToSQL(self):
		"""Определяет положение сигнала и записывает его в базу данных"""
		status = self.getState()
		zapros = "UPDATE `kotel_din` SET `state`=%s WHERE `din`=%s"
		data = (status, self.id)
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros, data)
		dbconnect.connect.commit()
		dbconnect.close()
		return True

class Dout():
	"""простой выходной сигнал"""
	def __init__(self, id):
		self.id = id						#id сигнала
		zapros = "SELECT `pin`, `title`, `state`  FROM `kotel_dout` WHERE `dout`="+str(self.id)
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros)
		row = dbconnect.cursor.fetchone()
		dbconnect.close()
		self.pin = int(row[0])				#пин на малине
		self.title = row[1]					#описание сигнала
		self.status = int(row[2])			#состояние из базы данных
		GPIO.setup(self.pin, GPIO.OUT)		#инициализация GPIO
	def setStateTrue(self):
		"""включение контакта без базы данных"""
		self.status = 1
		GPIO.output(self.pin, self.status)
	def setStateFalse(self):
		"""отключение контакта без базы данных"""
		self.status = 0
		GPIO.output(self.pin, self.status)
	def setStateTrueToSQL(self):
		"""включение контакта с базой данных"""
		self.setStateTrue()
		self.getStateToSQL()
	def setStateFalseToSQL(self):
		"""включение контакта с базой данных"""
		self.setStateFalse()
		self.getStateToSQL()
	def setStateToSQL(self):
		"""проверяет положение в базе данных и выставляет его"""
		zapros = "SELECT `state` FROM `kotel_dout` WHERE `dout`="+str(self.id)
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros)
		row = dbconnect.cursor.fetchone()
		dbconnect.close()
		self.status = int(row[0])
		GPIO.output(self.pin, self.status)
	def getStateToSQL(self):
		"""выставляет сигнал в базе данных в соотвествии с текущем состоянием"""
		zapros = "UPDATE `kotel_dout` SET `state`=%s WHERE `dout`=%s"
		data = (self.status, self.id)
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros, data)
		dbconnect.connect.commit()
		dbconnect.close()
		return True