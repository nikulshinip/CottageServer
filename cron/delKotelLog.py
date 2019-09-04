import sys, mysql.connector
sys.path.append('/srv/py/config')
import mySQLconfig
sys.path.append('/srv/py/moduls/modulLib')
import kotelLog

zapros = 'SELECT COUNT(`id`) FROM `kotel_log`'
dbconnect = mySQLconfig.SqlConnect()
dbconnect.cursor.execute(zapros)
size = dbconnect.cursor.fetchone()
if int(size[0]) > 1000 :
	delZapros = 'DELETE FROM `kotel_log` order by `id` asc limit '+str(size[0])+' - 1000;'
	dbconnect.cursor.execute(delZapros)
dbconnect.close()
log = kotelLog.Log
log.addLog('Лог почишен, оставленна последняя 1000 записей')