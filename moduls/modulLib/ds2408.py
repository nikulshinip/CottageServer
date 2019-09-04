import sys, mysql.connector, os
sys.path.append('../../config')
import mySQLconfig

class DS2408() :
	"""устройство на основе ds2408"""
	def __init__(self, id) :
		self.id = id							#id устройства
		zapros = "SELECT `address`, `title` FROM `ds2408` WHERE `id`="+str(self.id)
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros)
		row = dbconnect.cursor.fetchone()
		dbconnect.close()
		self.address = "/mnt/1wire/"+row[0]+"/"	#адрес файлов устройства в системе
		self.title = row[1]						#коментарий к устройству
		self.dinNumber = {1:4, 2:3, 3:1, 4:2}	#словарь адресов Din
		self.doutNumber = {1:5, 2:7, 3:6}		#словарь адресов Dout
		self.din = {1:2, 2:2, 3:2, 4:2}			#первоначальное состояние сигналов Din
		self.dout = {1:2, 2:2, 3:2}				#первоначальное состояние сигналов Dout
		self.connect = 2						#первоначальное состояние связи с устройством
	def checkConnect(self) :
		"""функция для проверки доступности устройства и записи об этом в базу данных"""
		address = self.address+"address"
		try:
			file = open(address, "r", encoding="utf-8")
			st = file.read()
			file.close()
			connect = 1
		except:
			connect = 0
		zapros = "UPDATE `ds2408` SET `connect`=%s WHERE `id`=%s"
		data = (connect, self.id)
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros, data)
		dbconnect.connect.commit()
		dbconnect.close()
		self.connect = connect
		return connect
	def getDin(self, din) :
		"""вычитывание состояния сигнала из файла"""
		address = self.address+"sensed."+str(self.dinNumber[din])
		try:
			file = open(address, "r", encoding="utf-8")
			st = file.read()
			state = int(st.strip())
			file.close()
		except:
			state = 2
		self.din[din] = state
		return state
	def getDinToSQL(self, din) :
		"""вычитывание состояния сигнала из файла и помешение его в базу данных"""
		state = self.getDin(din)
		zapros = "UPDATE `ds2408` SET `din"+str(din)+"`=%s WHERE `id`=%s"
		data = (state, self.id)
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros, data)
		dbconnect.connect.commit()
		dbconnect.close()
		return True
	def setDout(self, dout, state) :
		"""выставление выходного сигнала"""
		try:
			strobe = open(self.address+"strobe", "w")
			strobe.write("1")
			strobe.close()
			file = open(self.address+"PIO."+str(self.doutNumber[dout]), "w")
			file.write(str(state))
			file.close()
			self.dout[dout] = state
			end = True
		except:
			end = False
		return end
	def setDoutStateToSQL(self, dout) :
		"""проверяет положение в базе данных и выставляет его"""
		zapros = "SELECT `dout"+str(dout)+"` FROM `ds2408` WHERE `id`="+str(self.id)
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros)
		row = dbconnect.cursor.fetchone()
		dbconnect.close()
		state = int(row[0])
		return self.setDout(dout, state)
	def setDoutStateAndSQL(self, dout, state):
		"""выставляет сигнал в базе данных и выставление выходного сигнала"""
		if self.setDout(dout, state) :
			zapros = "UPDATE `ds2408` SET `dout"+str(dout)+"`=%s WHERE `id`=%s"
			data = (state, self.id)
			dbconnect = mySQLconfig.SqlConnect()
			dbconnect.cursor.execute(zapros, data)
			dbconnect.connect.commit()
			dbconnect.close()
			return True
		else :
			zapros = "UPDATE `ds2408` SET `dout"+str(dout)+"`=%s WHERE `id`=%s"
			data = (2, self.id)
			dbconnect = mySQLconfig.SqlConnect()
			dbconnect.cursor.execute(zapros, data)
			dbconnect.connect.commit()
			dbconnect.close()
			return False