import sys, mysql.connector, datetime
import smsSend
sys.path.append('../../config')
import mySQLconfig

class Log() :
	"""класс лога сообщений от системы котла"""
	def addLog(message, type="INFO", title="событие котла") :
		date = datetime.datetime.now()
		zapros = "INSERT INTO `kotel_log` (`id`, `type`, `date`, `message`, `title`) VALUES (%(id)s, %(type)s, %(date)s, %(message)s, %(title)s)"
		dbconnect = mySQLconfig.SqlConnect()
		id = dbconnect.cursor.lastrowid
		data = {'id' : id, 'type' : type, 'date' : date, 'message' : message, 'title' : title}
		
		dbconnect.cursor.execute(zapros, data)
		dbconnect.connect.commit()
		dbconnect.close()
		if type=='ERROR' :
			sms = smsSend.SMSSend()
			sms.send(message)
		return True