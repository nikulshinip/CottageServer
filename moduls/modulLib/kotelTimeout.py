import sys, mysql.connector, datetime
sys.path.append('../../config')
import mySQLconfig

class TimeOut() :
	"""класс таймаута котла"""
	def __init__(self) :
		self.timeOut = []	#список всех внесенных в таблицу таймаутов
		self.now = False	#признак что сейчас идет таймаут
	def getSQL(self) :
		"""вычитывает из базы данных таймауты и возврашает True если хоть один из них идет прямо сейчас"""
		zapros = "SELECT `from`, `before` FROM `kotel_timeout`"
		dbconnect = mySQLconfig.SqlConnect()
		dbconnect.cursor.execute(zapros)
		row = dbconnect.cursor.fetchone()
		self.timeOut = []
		while row is not None :
			self.timeOut.append({'from' : row[0], 'before' : row[1]})
			row = dbconnect.cursor.fetchone()
		dbconnect.close()
		dtime=datetime.datetime.now()
		timeNow = dtime.hour*60*60+dtime.minute*60+dtime.second
		now = False
		for values in self.timeOut :
			if values['from'].seconds < timeNow and values['before'].seconds > timeNow :
				now = True;
		if now == True :
			self.now = now
			return True
		else :
			self.now = now
			return False